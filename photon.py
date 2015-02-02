import exifread
import sys
import os
import json
import logging

logging.basicConfig(level=logging.WARNING,format='%(asctime)s %(name)s %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filename ="trace.log")
logger = logging.getLogger("photon")

def renamephotos(path): 
	'''renames all .JPG with according to the date and time the picture was taken'''
	history = {}

	for root, dirs, files in os.walk(path):
		for name in files:
			ext = name[len(name)-4:len(name)]
			if ext == ".JPG":
				filename = root + "\\" +  name
				logger.info("filename: %s",filename)
				try:
					f = open(filename, 'rb')
					try:
						tags = exifread.process_file(f)
						f.close()
						logger.info(tags.keys())
						datetime = str(tags['EXIF DateTimeOriginal'])
						logger.info("DateTimeOriginal: %s",datetime)
						datetime = datetime.replace(":","")
						datetime = datetime.replace(" ","_")
						newname = root + "\\" + datetime + ext
						os.rename(filename,newname)
						history[filename]=newname
					except:
						logger.warning("filename: %s; error: %s",filename,sys.exc_info()[0:2])
					finally:
						f.close()
						logger.info("file was closed")
				except: 
					logger.warning("filename: %s; error: %s",filename,sys.exc_info()[0:2])
	
	h = open("hist.log","w")
	history = json.dumps(history)
	h.write(history)

	
path = sys.argv[1]
listing = renamephotos(path)
	



		