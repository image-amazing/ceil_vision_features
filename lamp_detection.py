from image_undistortion import *
import math

def check_circular(contour):
	shape = contour.shape
	#points
	pts = []
	print 'this contour\'s shape: ',shape[0]
	step = 4
	if shape[0] > 40:
		step = shape[0] / 10
	for i in range(0,shape[0],step):
		pt = [contour[i][0][0],contour[i][0][1]]
		pts.append(pt)
	print 'pts:',len(pts)
	#lines
	lines = []
	distance_thd = 10
	for i in range(len(pts)-1):
		x1,y1 = pts[i]
		for j in range(i,len(pts)):
			x2,y2 = pts[j]
			if abs(x1-x2) < distance_thd or abs(y1-y2) < distance_thd:
				continue
			#perpendicular bisector
			#
			#a = y1 - y2
			#b = x1 - x2
			#c = x1*y2 - x2*y1
			a = x2 - x1
			b = y2 - y1
			c = (x1-x2)*(x1+x2)*.5 + (y1-y2)*(y1+y2)*.5
			
			lines.append([a,b,c])
	print 'lines:',len(lines)
	if len(lines) <= 4:
		return False
	#intersections
	intersections = []
	for i in range(len(lines)-1):
		a1,b1,c1 = lines[i]
		for j in range(i,len(lines)):
			a2,b2,c2 = lines[j]
			cos_angle = (a1*a2+b1*b2)/(math.sqrt(a1*a1+b1*b1)*math.sqrt(a2*a2+b2*b2))
			#angle_threshold (30~150)&(-150~-30)
			if abs(cos_angle) >0.865:
				continue
			d = a1*b2 - a2*b1
			x = (b1*c2 - b2*c1) / d
			y = (c1*a2 - c2*a1) / d
			intersections.append([x,y])
	print 'intersections:',len(intersections)
	if len(intersections) <= 3:
		return False
	intersections = np.array(intersections)
	print 'shape:',intersections.shape
	print intersections
	#print 'col:',intersections[1:10,0],'and',intersections[:][1]
	minx = np.min(intersections[:,0])
	maxx = np.max(intersections[:,0])
	miny = np.min(intersections[:,1])
	maxy = np.max(intersections[:,1])
	print 'region: ','x~[',minx,',',maxx,']'
	print 'y~[',miny,',',maxy,']'
	CIRCULAR_REGION_THD = 15
	if maxx - minx <= CIRCULAR_REGION_THD and maxy - miny <= CIRCULAR_REGION_THD:
		return True
	return False
	

def detect_lamp(undist,config,SHOW = 0):
	USE_CANNY = 0
	gray = cv2.cvtColor(undist, cv2.COLOR_BGR2GRAY)
	#\TODO remove little group bright
	bin_thd = config.getint("lamp","canny_thd2")
	#bin image
	retval,bin_img = cv2.threshold(gray,230,255,cv2.THRESH_BINARY)
	USE_CV_CONTOURS = 1
	CONTOUR_LENGTH_THD = 20
	if USE_CV_CONTOURS:
		contours, hierarchy = cv2.findContours( bin_img, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
		contours = np.array(contours)
		for contour in contours:
			#test
			# print 'two shape: ',contour.shape,' ',contours[0].shape
			# if contour.shape[0] != contours[8].shape[0]:
				# continue
			shape = contour.shape
			if shape[0] < CONTOUR_LENGTH_THD:
				continue
			
			if check_circular(contour):
				for i in range(shape[0]):
					cv2.circle(undist, (contour[i][0][0],contour[i][0][1]), 1, (0,0,255),1)
			else:
				for i in range(shape[0]):
					cv2.circle(undist, (contour[i][0][0],contour[i][0][1]), 1, (255,0,0),1)
					
		
	else:
		if not USE_CANNY:
			#distance image
			dis_img = cv2.distanceTransform(bin_img,cv2.cv.CV_DIST_L1,3)
			dis_img = dis_img.astype('uint8')
			edge_img = (dis_img==1)
			edge_img = edge_img.astype('uint8')
			edge_img = edge_img*255
		else:
			canny_thd1 = config.getint("lamp","canny_thd1")
			canny_thd2 = config.getint("lamp","canny_thd2")
			edge_img = cv2.Canny(bin_img, canny_thd1, canny_thd2)
		if SHOW:
			cv2.imshow('edge',edge_img)
		pass
	#group them
	
	
if __name__ == "__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
		config = ConfigParser.ConfigParser()
		config.read("demo.conf")
		undist = undistort_image(filename,config)
		#lines = extract_lines
		detect_lamp(undist,config,1)
		
		cv2.imshow('undist',undist)
		cv2.waitKey(0) % 0x100
		cv2.destroyAllWindows()
	else:
		print 'no image input'