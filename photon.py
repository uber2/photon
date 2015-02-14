import exifread
import sys
import os
import json
import logging
import pprint
import shutil
import re

logging.basicConfig(level=logging.WARNING,format='%(asctime)s %(name)s %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filename ="trace.log")
logger = logging.getLogger("photon")

def renamephotos(path): 
	'''renames all .JPG according to the date and time the picture was taken'''
	history = {}
	ext2prefix = {".JPG":"IMG_",".MOV":"MOV_"}
	for root, dirs, files in os.walk(path):
		for name in files:
			ext = name[len(name)-4:len(name)]
			if ext == ".JPG":
				filename = root + "\\" +  name
				logger.info("filename: %s",filename)
				try:
					datetime = getoriginaltimeanddate(filename)
					newname = root + "\\" + ext2prefix[ext] + datetime + ext
					os.rename(filename,newname)
					history[filename]=newname
				except: 
					logger.warning("filename: %s; error: %s",filename,sys.exc_info()[0:2])
	
	h = open("hist.log","w")
	history = json.dumps(history)
	h.write(history)

def getsetoffiles(path):
	"""Return set of files within a given path"""
	listing = set()
	for root, dirs, files in os.walk(path):
		for name in files:
			listing.add(name)
	return listing
		
def compare(path1,path2):
	"""Compare content of two folders"""
	set1 = getsetoffiles(path1)
	set2 = getsetoffiles(path2)
	
	f = open("compare.log","w")
	try:
		f.write("These files are unique to folder %s \n" %path1)
		for item in set1-set2:
			f.write(pprint.pformat(item) + "\n")
		
		f.write("These files are unique to folder %s \n" %path2)
		for item in set2-set1:
			f.write(pprint.pformat(item) + "\n")
			
		print("Output written to compare.log")
	finally:
		f.close()
		print("file closed")
		
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
	
def reorder(path):
	"""create a structure of folders according to the days the photos have been taken"""
	for root, dirs, files in os.walk(path):
		for name in files:
			try:
				datetime = getoriginaltimeanddate(root + "\\" + name)
				oldpath = root + "\\" + name
				newpath = path + "\\" + datetime[0:4] + "-" + datetime[4:6] + "-" + datetime[6:8] 
				if not os.path.exists(newpath): os.makedirs(newpath)
				shutil.move(oldpath,newpath)
			except:
				logger.warning("error: %s",sys.exc_info()[0:2])
				continue
	
if __name__ == "__main__":
	path1 = sys.argv[1]
	renamephotos(path1)
	reorder(path1)
	
	#path2 = sys.argv[2]
	#compare(path1,path2)
	

		