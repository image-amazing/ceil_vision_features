#!/usr/bin/python
from image_undistortion import *
#import image_undistortion as un
import math

def extract_harris(gray,config):	
	blockSize = config.getint("corner","harris_blocksize")
	ksize = config.getint("corner","harris_ksize")
	k = config.getfloat("corner","harris_k")
	threshold = config.getfloat("corner","harris_thd")
	response = cv2.cornerHarris(gray,blockSize,ksize,k)
	dilated = cv2.dilate(response,None)
	local_max = cv2.compare(response,dilated,0)
	h,w = gray.shape
	corners = []
	for y in range(10,h-10):
		for x in range(10,w-10):
			if local_max[y][x] == 255 and abs(response[y][x]) > threshold :
				corners.append([x,y])
	
	return np.array(corners)
	
def extract_Shi_Tomasi(gray,cofig):
	nbest = config.getint("corner","ST_nbest")
	level = config.getfloat("corner","ST_qualitylevel")
	mindistance = config.getfloat("corner","ST_mindistance")
	corners = cv2.goodFeaturesToTrack(gray,nbest,level,mindistance)
	shape = corners.shape
	corners = corners.reshape(shape[0]*shape[1],shape[2])
	return corners

def extract_FAST(gray,config):
	fast = cv2.FastFeatureDetector()
	#print "Threshold: ", fast.getInt('threshold')
	#print "nonmaxSuppression: ", fast.getBool('nonmaxSuppression')
	kp = fast.detect(gray,None)
	return kp
	
	

def draw_corner(undist,corners):
	shape = corners.shape
	for i in range(shape[0]):
		cv2.circle(undist, (int(corners[i][0]),int(corners[i][1])), 1, (0,0,255),2)
	return undist

def getCornerFromKeyPoint(kp):
	corners = []
	for i in range(len(kp)):
		corners.append(kp[i].pt)
	return np.array(corners)
	
if __name__ == "__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
		config = ConfigParser.ConfigParser()
		config.read("demo.conf")
		undist = undistort_image(filename,config)
		gray = cv2.cvtColor(undist, cv2.COLOR_BGR2GRAY)
		method = config.getint("corner","method")
		if method == 0:
			corners = extract_harris(gray,config)
		elif method == 1:
			corners = extract_Shi_Tomasi(gray,config)
		else:
			kp = extract_FAST(gray,config)
			corners = getCornerFromKeyPoint(kp)
		print 'corners.size: ',corners.shape,' method is:',method
		
		undist = draw_corner(undist,corners)	
		cv2.imshow('corners',undist)
		cv2.waitKey(0) % 0x100
		cv2.destroyAllWindows()
	else:
		print 'no image input'