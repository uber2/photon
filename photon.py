import exifread
import sys
import os
import json
import logging
logging.basicConfig(level=logging.INFO,format='%(asctime)s %(name)s %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filename ="trace.log")
logger = logging.getLogger("photon")

def getlistoffiles(path): 
	history = {}

	for root, dirs, files in os.walk(path):
		for name in files:
			ext = name[len(name)-4:len(name)]
			if ext == ".JPG":
				filename = root + "\\" +  name
				f = open(filename, 'rb')
				try:
					# Return Exif tags
					tags = exifread.process_file(f)
					f.close()
					datetime = str(tags['EXIF DateTimeOriginal'])
					datetime = datetime.replace(":","")
					datetime = datetime.replace(" ","_")
					newname = root + "\\" + datetime + ext
					#print newname
					history[filename]=newname
					os.rename(filename,newname)
				except:
					logger.warning("Problems with file %s",root + "\\" + name)
					f.close()
	
	h = open("hist.log","w")
	history = json.dumps(history)
	h.write(history)



path = sys.argv[1]
listing = getlistoffiles(path)
	



		