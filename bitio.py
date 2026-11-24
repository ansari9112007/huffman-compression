"""Bit-level reading and writing."""


class BitWriter:
    def __init__(self):
        self.out = bytearray()
        self.cur = 0
        self.n = 0

    def bit(self, b):
        self.cur = (self.cur << 1) | b
        self.n += 1
        if self.n == 8:
            self.out.append(self.cur)
            self.cur, self.n = 0, 0

    def byte(self, value):
        for i in range(7, -1, -1):
            self.bit((value >> i) & 1)

    def bits(self, code):
        for ch in code:
            self.bit(1 if ch == "1" else 0)

    def finish(self):
        if self.n:
            self.out.append(self.cur << (8 - self.n))
            self.cur, self.n = 0, 0
        return bytes(self.out)


class BitReader:
    def __init__(self, data, start=0):
        self.data = data
        self.pos = start * 8

    def bit(self):
        byte_index, offset = divmod(self.pos, 8)
        self.pos += 1
        return (self.data[byte_index] >> (7 - offset)) & 1

    def byte(self):
        v = 0
        for _ in range(8):
            v = (v << 1) | self.bit()
        return v