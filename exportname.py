from sc_compression.decompressor import Decompressor
import json
import io
import os


class Reader(io.BytesIO):
     def __init__(self, stream):
        super().__init__(stream)
        self._bytes_left = len(stream)
        self.buff = stream
     def readUInt8(self):
	      	return int.from_bytes(self.read(1), "little")
     def readUInt16(self):
        return int.from_bytes(self.read(2), "little")
     def readUInt32(self):
        return int.from_bytes(self.read(4), "little")
     def readString(self):
        length = self.readUInt8()
        self._bytes_left -= length
        return super().read(length).decode("utf-8")


print("sc export name tool by github.com/DemirCnq")
file = input("Enter file name: ")
sc = open(file, "rb")
decompressed = Decompressor().decompress(sc.read())
read = Reader(decompressed)

shapeCount = read.readUInt16()
animationsCount = read.readUInt16()
texturesCount = read.readUInt16()
textFieldsCount = read.readUInt16()
matricesCount = read.readUInt16()
colorTransformsCount = read.readUInt16()
#print(animationsCount)

read.readUInt32()
read.readUInt8()

export_count = read.readUInt16()
exports = [read.readUInt16() for x in range(export_count)]
exports = {x: read.readString() for x in exports}

newdata = json.dumps(exports,sort_keys=True, indent=4)
print(newdata)

name = os.path.basename(file)
newname = f"{str(name[:-3])}.txt"
print("Saving to new file: " + newname)

save = open(newname, "w")
save.write(newdata)