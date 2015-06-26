import exifread
import sys
import os
import json
import logging
import pprint
import re
import tkFileDialog as tk

logging.basicConfig(level=logging.WARNING,format='%(asctime)s %(name)s %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filename ="trace.log")
logger = logging.getLogger("photon")

def getexifdata(filename):
	"""Get exif data for a file. Note, the input has to be the fully qualified filename"""
	f = open(filename, 'rb')
	try:
		tags = exifread.process_file(f)
	finally:
		f.close()
	return tags

def getoriginaltimeanddate(filename):
	"""returns a string YYYYMMDD_HHMMSS for fully qualified filename"""
	datetime = str(getexifdata(filename)['EXIF DateTimeOriginal'])
	datetime = datetime.replace(":","")
	datetime = datetime.replace(" ","_")
	return datetime

def bringordertochaos(base, target):
	"""create a structure of folders according to the days the photos have been taken"""
	month = {"01":"01_January","02":"02_February","03":"03_March",
				"04":"04_April","05":"05_May","06":"06_June",
				"07":"07_July","08":"08_August","09":"09_September",
				"10":"10_Oktober","11":"11_November","12":"12_December"}

	permittedextensions = ["png","jpg","mov","jpeg","avi","bmp","tiff"]

	for root, dirs, files in os.walk(target):
		for name in files:
			# MISSING: IMPLEMENT SAFTEY SWITCH; ONLY HANDLE JPEG;JPG;TIFF;MOV;AVI;BMP;
			ext = name[len(name)-4:len(name)]
			if ext[0] == "." :ext = ext[1:]
			if ext.lower() in permittedextensions:
				try:
					datetime = getoriginaltimeanddate(root + "\\" + name)
				except:
					oldpath = root + "\\" + name
					newpath = base + "\\" + "Photon" + "\\" + "_unassigned" + "\\"
					if not os.path.exists(newpath): os.makedirs(newpath)
					os.rename(oldpath,newpath + name)
					next
				try:
					oldpath = root + "\\" + name
					newpath = base + "\\" + "Photon" + "\\" + datetime[0:4] + "\\" + month[datetime[4:6]]
					if not os.path.exists(newpath): os.makedirs(newpath)
					# MISSING: FIND OUT ORGINIAL EXTENSION (COULD BE TIFF OR JPEG OR JPG)
					os.rename(oldpath,newpath + "\\" + "IMG_" + datetime + ".JPG" )
				except:
					logger.warning("file: %s, error: %s",name,sys.exc_info()[0:2])
					continue

if __name__ == "__main__":
	base = tk.askdirectory(title="base")
	target = tk.askdirectory(title="target")
#	base = sys.argv[1]
#	target = sys.argv[2]
	bringordertochaos(base,target)
