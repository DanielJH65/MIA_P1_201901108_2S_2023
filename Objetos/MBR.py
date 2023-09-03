import datetime
import random
import struct

from Objetos.Partition import Partition
from utilidades import encodeStr

codigo = "i i i s"


class MBR:
    def __init__(self) -> None:
        self.size = -1
        self.date_created = -1
        self.disk_signature = -1
        self.fit = b'0'
        self.partitions = [Partition() for i in range(4)]

    def setInfo(self, size, fit):
        self.size = size
        self.date_created = int(datetime.datetime.now().timestamp())
        self.disk_signature = random.randint(0, 2**31 - 1)
        self.fit = encodeStr(fit, 1)

    def getCodigo(self):
        return codigo

    def serialize(self):
        serialize = struct.pack(codigo, self.size, self.date_created, self.disk_signature, self.fit)
        for i in range(4):
            serialize += self.partitions[i].serialize()
        return serialize
    
    def deserialize(self, data):
        sizeMBR = struct.calcsize(codigo)
        sizePart = struct.calcsize(Partition().getCodigo())
        dataMBR = data[:sizeMBR]

        self.size, self.date_created, self.disk_signature, self.fit = struct.unpack(codigo, dataMBR)

        for i in range(4):
            dataPart = data[sizeMBR + i*sizePart:sizeMBR + (i+1)*sizePart]
            self.partitions[i].deserialize(dataPart)