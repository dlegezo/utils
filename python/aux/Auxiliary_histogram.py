
import pefile
import time
import os
import sys
import matplotlib.pyplot as plt

def getPEFileTimestamp(pathFile):
	try:
		pe = pefile.PE(pathFile)
		return pe.FILE_HEADER.TimeDateStamp
	except pefile.PEFormatError as e:
		return None

def getDirFilesTimestamp(pathDir):
	timestamps = []
	for dirname, dirnames, filenames in os.walk(pathDir):
		for filename in filenames:
			pathFile = os.path.join(dirname, filename)
			timestamp = getPEFileTimestamp(pathFile)
			if (timestamp != None):
				timestamps += (timestamp, )
	return timestamps

def plotHistogramLastYear(timestamps):
	years = []
	months = []
	months_last_year = []
	for timestamp in timestamps:
		stamp = time.gmtime(timestamp)
		years += (stamp.tm_year, )
		months += (stamp.tm_mon, )
	last_year = max(years)
	for i in range(len(years)):
		if (years[i] == last_year):
			months_last_year += (months[i], )
	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.set_ylabel("samples")
	xlabel = "month, " + str(last_year)
	ax.set_xlabel(xlabel)
	plt.hist(months_last_year, bins=12)
	plt.show()

if __name__ == '__main__':
	pathDir = sys.argv[1]
	timestamps = getDirFilesTimestamp(pathDir)
	plotHistogramLastYear(timestamps)
