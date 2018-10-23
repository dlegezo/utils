
import time, sys

def encode2B():
	hXorKey = 0x7E
	strDecoded1 = "1c_to_kl.txt"
	strDecoded2 = "cmd.exe /C ping 1.1.1.1 -n 1 -w 3000 > Nul & Del \"%s\""
	strDecoded3 = "SYSTEM\CurrentControlSet\services\Disk\Enum"
	strEncoded1 = ""
	strEncoded2 = ""
	strEncoded3 = ""
	for ch in strDecoded1:
		strEncoded1 += chr(ord(ch) ^ hXorKey)
	for ch in strDecoded2:
		strEncoded2 += chr(ord(ch) ^ hXorKey)
	for ch in strDecoded3:
		strEncoded3 += chr(ord(ch) ^ hXorKey)
		print hex(ord(ch) ^ hXorKey)

def decodeNDUstr():
	hKey = 0xE7
	str1 = ( 0x5C, 0x8B, 0x7E, 0x7A, 0x8D, 0x7E, 0x69, 0x8B, 0x88, 0x7C, 0x7E, 0x8C, 0x8C, 0x70 )
	str2 = ( 0x6F, 0x82, 0x8B, 0x8D, 0x8E, 0x7A, 0x85, 0x5A, 0x85, 0x85, 0x88, 0x7C )
	str3 = ( 0x60, 0x7E, 0x8D, 0x6D, 0x81, 0x8B, 0x7E, 0x7A, 0x7D, 0x5C, 0x88, 0x87, 0x8D, 0x7E, 0x91, 0x8D )
	str4 = ( 0x6B, 0x7E, 0x7A, 0x7D, 0x69, 0x8B, 0x88, 0x7C, 0x7E, 0x8C, 0x8C, 0x66, 0x7E, 0x86, 0x88, 0x8B, 0x92 )
	str5 = ( 0x67, 0x8D, 0x6E, 0x87, 0x86, 0x7A, 0x89, 0x6F, 0x82, 0x7E, 0x90, 0x68, 0x7F, 0x6C, 0x7E, 0x7C, 0x8D, 0x82, 0x88, 0x87 )
	str6 = ( 0x6F, 0x82, 0x8B, 0x8D, 0x8E, 0x7A, 0x85, 0x5A, 0x85, 0x85, 0x88, 0x7C, 0x5E, 0x91 )
	str7 = ( 0x70, 0x8B, 0x82, 0x8D, 0x7E, 0x69, 0x8B, 0x88, 0x7C, 0x7E, 0x8C, 0x8C, 0x66, 0x7E, 0x86, 0x88, 0x8B, 0x92 )
	str8 = ( 0x6C, 0x7E, 0x8D, 0x6D, 0x81, 0x8B, 0x7E, 0x7A, 0x7D, 0x5C, 0x88, 0x87, 0x8D, 0x7E, 0x91, 0x8D )
	str9 = ( 0x6B, 0x7E, 0x8C, 0x8E, 0x86, 0x7E, 0x6D, 0x81, 0x8B, 0x7E, 0x7A, 0x7D )
	str10 = ( 0x6F, 0x82, 0x8B, 0x8D, 0x8E, 0x7A, 0x85, 0x5F, 0x8B, 0x7E, 0x7E )
	str11 = "Pw1rIbVvKHrJZY99GIqWcwBLZB7dGzcFWb0kl5TBLIkuwaz107hps4KpDIcydguKUi51B3PDkbxugk9Ez2jYSJ8DzoF22p987zFnCisKAt4a6FeHpLJiUUkF5flAzY8rqEGyq4VKPQTuO7ZboJaWxJGjuviSNlDikm7b4RPwt0pY9hy6JORsiEprQepfUjfo5b7SAylLCW4vNBwfuYZR36bHnZBIzYtFCDJUrBCf2zLav3ZZGsOU7Zj7IvaXyAC3"
	strings = []
	strDecoded = ""
	for ch in str11:
		strDecoded += chr(ord(ch)+hKey-0x100)
	print strDecoded	
	
def signedIntToHex(lst):
	strHash = ""
	for elem in lst:
		if elem >= 0:
			ch = "%0.2X " % elem
			strHash += ch
		else:
			ch = "%0.2X " % (0x100+elem)
			strHash += ch
	print strHash

def decodeXAgentRC4():
	lst = ( 59, -58, 115, 15, -117, 7, -123, -64, 116, 2, -1, -52, -34, -57, 4, 59, -2, 114, -15, 95, 94,\
	    	-61, -117, -1, 86, -72, -40, 120, 117, 7, 80, -24, -79, -47, -6, -2, 89, 93, -61, -117, -1, 85,\
    		-117, -20, -125, -20, 16, -95, 51, 53 )
	ykrop_aes1 = ( -20, -4, 38, -117, 64, 18, 57, -40, -107, 47, -126, -89, 105, 103, -8, 52 )
	ykrop_aes2 = ( 14, -79, 81, -101, -29, -28, -63, 51, 22, 40, -73, 60, 11, -96, 34, -113 )
	signedIntToHex(ykrop_aes2)

def constructURLXAgent():
	intDid = 1123581321
	hex1 = hex(intDid) # 0x42f87d89
	print hex1
	# arrayOfByte[0] = ((byte)(i & 0xFF));
    # arrayOfByte[1] = ((byte)(i >> 8 & 0xFF));
    # arrayOfByte[2] = ((byte)(i >> 16 & 0xFF));
    # arrayOfByte[3] = ((byte)(i >> 24 & 0xFF));

def decodeXorFile(key):
	fileEncoded = open("/home/u/malware/zerot/2_downloader/4cb716dcd888e7ebe4c04c26987416de", "rb")
	fileDecoded = open("/home/u/malware/zerot/2_downloader/4cb716dcd888e7ebe4c04c26987416de_dec", "ab")
	ch1 = fileEncoded.read(1)
	while (ch1):
		fileDecoded.write(chr(ord(ch1)^key))
		ch1 = fileEncoded.read(1)
	fileDecoded.close()
	fileEncoded.close()

def decodeIndigoZebra_2018_02():
	fileEncoded = open("/home/u/malware/indigo_zebra/2018_02/6f8d_drop_content/VSUtract.obj", "rb")
	fileDecoded = open("/home/u/malware/indigo_zebra/2018_02/6f8d_drop_content/VSUtract.dec", "ab")
	ch1 = fileEncoded.read(1)
	while (ch1):
		fileDecoded.write(chr((((ord(ch1)+0x42)^0xFA)-0x7F)&0xFF))
		ch1 = fileEncoded.read(1)
	fileDecoded.close()
	fileEncoded.close()

# len 0x2399, offset 0x045B
def decodePairsMoving():
	fileEncoded = open("/home/u/malware/proj_c/2017_01/igfxsrv/bin2", "rb")
	fileDecoded = open("/home/u/malware/proj_c/2017_01/igfxsrv/bin3", "ab")
	fileEncoded.seek(0x045B)
	ch1 = fileEncoded.read(1)
	ch2 = fileEncoded.read(1)
	while (ch1 and ch2):
		fileDecoded.write(ch2)
		fileDecoded.write(ch1)
		print hex(ord(ch1))
		print hex(ord(ch2))
		ch1 = fileEncoded.read(1)
		ch2 = fileEncoded.read(1)
	fileDecoded.close()
	fileEncoded.close()

def decodeParadirNaikon():
	domain1 = "jp/xhlrhonso/bnl"
	domain2 = "dryiicw746/bnl"
	domain3 = "fe/92icorpel3/nsf"
	domain1_decoded = ""
	domain2_decoded = ""
	domain3_decoded = ""
	for ch in domain1:
		domain1_decoded += chr(ord(ch)^0x01)
	print domain1_decoded

def decodeMinus():
	encoded = "Dpoufou.mfohui;"
	decoded = ""
	for i in range(len(encoded)):
		decoded += chr(ord(encoded[i])-1)
	return decoded

if __name__ == '__main__':
	print decodeMinus()