import socket
from .packet import parse_packet
import struct

class Client (object):

    def __init__(self, server, port):
        self.server = server
        self.port = port
        self.last_seq = 0
        self.pending = {}
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setblocking(0)

    @property
    def nextseq(self):
        self.last_seq += 1
        return self.last_seq

    def tick(self, dt, world):
        # Read in any pending datagrams since last time.
        while True:
            try:
                data, _address = self.socket.recvfrom(512)
                p = parse_packet(data)
                if p.sequence in self.pending:
                    del self.pending[p.sequence]
                pos = 0
                while pos < len(p.payload):
                    idx, px, py, pz, vx, vy, vz = struct.unpack('!L6d', p.payload[pos:pos+52])
                    pos += 52
                    world.objects[idx].position.set(px, py, pz)
                    #world.objects[idx].velocity.set(vx, vy, vz)
            except socket.error:
                break
        # Write any pending packets, either added since last time, or not yet acknowledged.
        for p in self.pending.values():
            self.write(p)

    def write(self, packet):
        self.socket.sendto(packet.flatten(), (self.server, self.port))
        if packet.needs_ack:
            self.pending[packet.sequence] = packet
