
import struct

from utilidades import encodeStr


codigo = "s s s i i 16s"


class Partition:
    def __init__(self) -> None:
        self.status = b'\0'
        self.type = b'\0'
        self.fit = b'\0'
        self.start = -1
        self.size = -1
        self.name = b'\0'*16

    def setInfo(self, status, type, fit, start, size, name):
        self.status = encodeStr(status, 1)
        self.type = encodeStr(type, 1)
        self.fit = encodeStr(fit, 1)
        self.start = start
        self.size = size
        self.name = encodeStr(name, 16)

    def getCodigo(self):
        return codigo

    def serialize(self):
        serialize = struct.pack(
            codigo, self.status, self.type, self.fit, self.start, self.size, self.name)
        return serialize

    def deserialize(self, data):
        self.status, self.type, self.fit, self.start, self.size, self.name = struct.unpack(
            codigo, data)
