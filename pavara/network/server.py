from pavara.world import World
from pavara.vecmath import Vector3
from .packet import *
import socket
import random

class Player (object):
    
    def __init__(self, server, address, pid):
        self.server = server
        self.address = address
        self.pid = pid
        self.last_seq = 0
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setblocking(0)
        self.pending = {}

    @property
    def nextseq(self):
        self.last_seq += 1
        return self.last_seq

    def tick(self, dt):
        # Write any pending packets, either added since last time, or not yet acknowledged.
        for p in self.pending.values():
            self.write(p)

    def handle(self, packet):
        if packet.sequence in self.pending:
            del self.pending[packet.sequence]
        if packet.kind == KIND_LOAD_MAP:
            print('LOADING MAP', packet.payload)
            self.server.world.reset()
            self.server.world.load(packet.payload.decode('utf-8'))
        elif packet.kind == KIND_GAME_START:
            print('MIXING THINGS UP')
            for obj in self.server.world.objects:
                if obj.mass:
                    x = random.uniform(-1.0, 1.0) * 10.0
                    y = random.random() * 0.0
                    z = random.uniform(-1.0, 1.0) * 10.0
                    obj.apply_force(Vector3(x, y, z))

    def write(self, packet):
        packet.sequence = self.nextseq
        self.socket.sendto(packet.flatten(), self.address)
        if packet.needs_ack:
            self.pending[packet.sequence] = packet


class Server (object):

    def __init__(self, port):
        self.port = port
        self.pending = {}
        self.players = {}
        self.last_pid = 0
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('0.0.0.0', port))
        self.socket.setblocking(0)
        self.world = World()

    @property
    def nextpid(self):
        self.last_pid += 1
        return self.last_pid

    def tick(self, dt):
        # Read in any pending datagrams since last time.
        while True:
            try:
                data, address = self.socket.recvfrom(512)
                p = parse_packet(data)
                if address[0] in self.players:
                    self.players[address[0]].handle(p)
                else:
                    self.handle(p, address)
            except socket.error:
                break
        # Let all the Player objects handle writing out pending re-sends.
        for p in self.players.values():
            p.tick(dt)
        # Update the world.
        self.world.tick(dt)
        # Send world updates.
        data = b''
        updates = []
        for obj in self.world.objects:
            if obj.moved:
                data += struct.pack('!L6d', obj.index, obj.position.x, obj.position.y, obj.position.z, obj.velocity.x, obj.velocity.y, obj.velocity.z)
                obj.moved = False
            if len(data) > 450:
                updates.append(Packet(KIND_WORLD_UPDATE, 0, payload=data))
                data = b''
        if data:
            updates.append(Packet(KIND_WORLD_UPDATE, 0, payload=data))
        for p in updates:
            self.broadcast(p)

    def handle(self, packet, address):
        if packet.kind == KIND_PLAYER_JOIN:
            print('PLAYER JOIN FROM', address)
            p = Player(self, address, self.nextpid)
            self.players[address[0]] = p

    def broadcast(self, packet):
        for p in self.players.values():
            p.write(packet)
