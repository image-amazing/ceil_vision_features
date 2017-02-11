#!/usr/bin/python
from image_undistortion import *
#import image_undistortion as un
import math

def extract_lines(undist,config):	
	
	#canny
	canny_thd1 = config.getint("canny","threshold1")
	canny_thd2 = config.getint("canny","threshold2")
	dst = cv2.Canny(undist, canny_thd1, canny_thd2)
	#hough line
	rho = config.getint("hough_line","rho")
	theta = config.getfloat("hough_line","theta")
	threshold = config.getint("hough_line","threshold")
	if config.getint("hough_line","use_p") == 0:
		lines = cv2.HoughLines(dst, rho, theta, threshold)
	else:
		lines = cv2.HoughLinesP(dst, rho, theta, threshold,0,
								config.getint("hough_line","min_length"),config.getint("hough_line","max_gap"))
	return lines#take care of the array's dim

if __name__ == "__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
		config = ConfigParser.ConfigParser()
		config.read("demo.conf")
		undist = undistort_image(filename,config)
		lines = extract_lines(undist,config)
		if lines is None:
			print 'no line extracted'
			exit()
		print 'lines.size: ',lines.shape
		#show lines
		shape = lines.shape
		lines = lines.reshape(shape[0]*shape[1],shape[2])
		shape = lines.shape
		print 'lines cnt: ',shape[0]
		for i in range(shape[0]):
			if config.getint("hough_line","use_p") == 0: 
				rho = lines[i][0]
				theta = lines[i][1]
				c = math.cos(theta)
				s = math.sin(theta)
				x0 = c * rho
				y0 = s * rho
				pt1 = (int(x0 - 1000*s),int(y0 + 1000*c))
				pt2 = ((int)(x0 + 1000*s),(int)(y0 - 1000*c))
				cv2.line( undist, pt1, pt2, (0,255,0),1)
			else:
				pt1 = (lines[i][0], lines[i][1])
				pt2 = (lines[i][2], lines[i][3])
				cv2.line( undist, pt1, pt2, (0,255,0),2)
		#show optical center
		cx = config.getfloat("image_param","cx")
		cy = config.getfloat("image_param","cy")
		cv2.circle(undist, (int(cx),int(cy)), 3, (0,0,255),3)
		cv2.imshow('lines',undist)
		cv2.waitKey(0) % 0x100
		cv2.destroyAllWindows()
	else:
		print 'no image input'