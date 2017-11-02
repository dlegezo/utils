
import binascii

strHex = ""
listInt = []

def reformatIntToASCII(listInt):
	pass

def reformatHexToBinary(listHex):
	reformated = bytearray(len(listHex))
	for i in range(len(listHex)):
		# print listHex[i]
		reformated[i] = listHex[i]
	return reformated

def reformatStringToHex(strCode):
	reformated = bytearray(len(strCode))
	i = 0
	j = 0
	while i < len(strCode):
		ch = str(strCode[i] + strCode[i+1])
		reformated[j] = int(ch, 16)
		j += 1
		i += 2
	return reformated

if __name__ == '__main__':
	listHex = "encoded_as_str_here"
	# fileBinary.write(reformatHexToBinary(listHex))
	fileBinary = open("./bin.bin","wb")
	binContent = reformatStringToHex(listHex)
	fileBinary.write(binContent)
	fileBinary.close()
	
