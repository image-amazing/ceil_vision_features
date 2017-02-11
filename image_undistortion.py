#!/usr/bin/python
import cv2
import sys
import ConfigParser
import numpy as np

def undistort_image(filename,config):
	src = cv2.imread(filename)
	#cv2.imshow('Source',src)
	
	image_fx = config.getfloat("image_param","fx")
	image_fy = config.getfloat("image_param","fy")
	image_cx = config.getfloat("image_param","cx")
	image_cy = config.getfloat("image_param","cy")
	image_p1 = config.getfloat("image_param","p1")
	image_p2 = config.getfloat("image_param","p2")
	dist_k = config.get("image_param","dist_k")
	dist_k = dist_k.split(',')
	distCoeffs = map(lambda x:float(x), dist_k)
	distCoeffs.insert(2,image_p1)
	distCoeffs.insert(3,image_p2)
	distCoeffs = np.array(distCoeffs)
	cameraMatrix = np.array([[image_fx,0.0,image_cx],
					[0.0,image_fy,image_cy],
					[0.0,0.0,1.0]])
	undist = cv2.undistort(src, cameraMatrix, distCoeffs)
	return undist
	
	
	
if __name__ == "__main__":
	if len(sys.argv) > 1:
		config = ConfigParser.ConfigParser()
		config.read("demo.conf")
		undist = undistort_image(sys.argv[1],config)
		cv2.imshow('undist_image',undist)
		cv2.waitKey(0) % 0x100
		cv2.destroyAllWindows()
	else:
		print 'no image input'