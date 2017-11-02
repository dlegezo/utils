
import zipfile
import olefile
import xml.etree.ElementTree as et
from swf.movie import SWF

def docxOpen(strDocxFile):
	return zipfile.ZipFile(strDocxFile)

def docxFindActiveX(docx):
	pathActiveX = ()
	xml = docx.read("[Content_Types].xml")
	root = et.fromstring(xml)
	for child in root:
		try:
			if "activeX" in child.attrib["ContentType"]:
				pathActiveX += (child.attrib["PartName"], )
		except Exception as e:
			pass
	return pathActiveX

def docxGetOLE2(docx, activeX, strDocxDir):
	OLE2s = ()
	for elem in activeX:
		ole2_path  = elem[1:]
		ole2_path  = ole2_path [:-4]+".bin"
		OLE2s += (docx.read(ole2_path), )
	return OLE2s

def ole2GetSWF(pathFileOLE2, strDocxDir):
	ole_data = ()
	for i in range(len(pathFileOLE2)):
		ole = olefile.OleFileIO(pathFileOLE2[i])
		content = ole.openstream("Contents")
		data = content.read()
		data = data[8:]
		dropBinToFile(data, strDocxDir + str(i))
		ole_data += (strDocxDir + str(i), )
		ole.close()
	return ole_data

def swfParse(strSWFFile):
	for file in strSWFFile:
		hFile = open(file)
		swf = SWF(hFile)
		print swf.parse()
		hFile.close()

def dropBinToFile(binContent, pathFile):
	f = open(pathFile, "wb")
	f.write(binContent)
	f.close()

if __name__ == '__main__':
	# CDFV2 -> OLE2 -> SWF
	strDocxDir = "dir_here"
	strDocxFile = "file_here"
	# open initial .docx
	docx = docxOpen(strDocxDir + strDocxFile)
	# find ActiveX inside the initial .docx
	pathArchActiveX = docxFindActiveX(docx)
	# get ActiveX == OLE2s on disk
	pathFileOLE2 = docxGetOLE2(docx, pathArchActiveX, strDocxDir)
	# get SWF from OLE2
	swfs = ole2GetSWF(pathFileOLE2, strDocxDir)
	print swfs
	# parse SWF
	swfParse(swfs)
	docx.close()
