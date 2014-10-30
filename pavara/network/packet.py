import struct

FLAG_NEEDS_ACK = 0x0001

# Client-initiated

KIND_PLAYER_JOIN = 0x01
KIND_LOAD_MAP = 0x02
KIND_GAME_START = 0x03

# Server-initiated

KIND_PLAYER_JOINED = 0xA1
KIND_GAME_STARTED = 0xA2
KIND_PLAYER_MOVEMENT = 0xA3
KIND_WORLD_UPDATE = 0xA4


class Packet (object):
    HEADER_FORMAT = '!BHL'

    def __init__(self, kind, sequence, flags=0, payload=b''):
        self.kind = kind # 1 byte
        self.sequence = sequence # 4 bytes
        self.flags = flags # 2 bytes
        self._payload = payload

    @property
    def payload(self):
        return self._payload

    @property
    def needs_ack(self):
        return (self.flags & FLAG_NEEDS_ACK) != 0

    def parse(self, data):
        self._payload = data

    def flatten(self):
        return struct.pack(self.HEADER_FORMAT, self.kind, self.flags, self.sequence) + self.payload


def parse_packet(data):
    header_size = struct.calcsize(Packet.HEADER_FORMAT)
    if len(data) < header_size:
        return None
    kind, flags, sequence = struct.unpack(Packet.HEADER_FORMAT, data[:header_size])
    packet = Packet(kind, sequence, flags=flags)
    packet.parse(data[header_size:])
    return packet
