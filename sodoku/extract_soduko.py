import cv2
import numpy as np
import torch

def empty_cell(cell):
	kernel = np.ones((7,7),np.float32) / 25
	dst = cv2.filter2D(cell, -1, kernel)

	thresh1 = 255 - cv2.adaptiveThreshold(dst, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 21, 2)

	kernel = np.ones((3,3),np.uint8)
	dilate = cv2.erode(thresh1, kernel, iterations = 1)

	dilate_inner = dilate[20:70, 20:70]

	#cv2.imshow("empty_cell", dilate_inner)
	#cv2.waitKey(0)

	return (dilate_inner.flatten() == 0).all()

def process_one(img, global_thresh=False, debug=False):

	im = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

	# Blur image for smoothness

	kernel = np.ones((7, 7), np.float32) / 25
	dst = cv2.filter2D(im, -1, kernel)
	
	if debug:
		cv2.imshow("smoothed", dst)
		cv2.waitKey(0)

	# Binary thresholding and inversion

	if global_thresh:
		ret, thresh1 = cv2.threshold(dst, 127, 255, cv2.THRESH_BINARY)
		thresh1 = 255 - thresh1

	thresh1 = cv2.adaptiveThreshold(dst, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 17, 2)
	thresh1 = 255 - thresh1

	if debug:
		cv2.imshow("thresholded", thresh1)
		cv2.waitKey(0)


	# Dilate activations

	kernel = np.ones((5,5),np.uint8)
	dilate = cv2.dilate(thresh1, kernel, iterations = 1)

	if debug:
		cv2.imshow("dilate", cv2.resize(dilate,(300,300)))

	# Extract contours

	if (cv2.__version__[0] > 3):
	    contours, hierarchy = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
	
	else:
	    dilate, contours, hierarchy = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

	if len(contours) != 0:
	    # Draw in blue the contours that were founded
	    cv2.drawContours(dilate, contours, -1, 255, 3)

	    # Find the biggest countour (c) by the area
	    c = max(contours, key = cv2.contourArea)
	    x,y,w,h = cv2.boundingRect(c)

	    # Draw the biggest contour (c) in green

	    rect = ((x, y), (x + w, y + h))
	    
	    #cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

	return rect

def process_two(img, rect, model, debug=False):

	im = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	sub_image = im[rect[0][1]:rect[1][1], rect[0][0]:rect[1][0]]
	sub_image_rgb = img[rect[0][1]:rect[1][1], rect[0][0]:rect[1][0]]

	#cv2.imshow("sub", sub_image)
	#cv2.waitKey(0)

	kernel = np.ones((7,7),np.float32) / 25
	dst = cv2.filter2D(sub_image, -1, kernel)

	thresh1 = cv2.adaptiveThreshold(sub_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 17, 2)
	thresh1 = 255 - thresh1
	canny = cv2.Canny(thresh1, 100, 255, 1)

	cnts = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if len(cnts) == 2 else cnts[1]

	zero = np.ones_like(sub_image) * 255.0
	val = 0

	rect_dicts = {}
	rect_ids = []

	for c in cnts:
		x,y,w,h = cv2.boundingRect(c)
		if w * h < 5000 or w * h > 20000:
			continue
		

		#cv2.drawContours(zero,[c], 0, (0,255,0), 3)
		rect = ((x, y), (x + w, y + h))

		rect_id = x + y * 10

		if len (rect_ids) == 0:
			rect_ids.append(rect_id)
			rect_dicts[rect_id] = rect
			continue

		if abs(min(np.array(rect_ids) - rect_id)) < 40:
			continue

		val += 1
		rect_ids.append(rect_id)
		rect_dicts[rect_id] = rect

		#cv2.rectangle(zero, (x,y),(x+w,y+h),(0,255,0),2)

		#cell = sub_image[rect[0][1]:rect[1][1], rect[0][0]:rect[1][0]]

		#cv2.imshow("cell", cell)
		#cv2.waitKey(1)

	#print val
	#print len(rect_dicts)
	#print len(rect_ids)

	board = np.ones((9, 9))

	x = 0
	y = 0
	total = 0

	rect_ids = np.sort(rect_dicts.keys())

	for i in rect_ids:
		rect = rect_dicts[i]
		cell = sub_image[rect[0][1]:rect[1][1], rect[0][0]:rect[1][0]]

		if empty_cell(cell):
			board[y][x] = 0

		if not empty_cell(cell):

			kernel = np.ones((3,3),np.float32) / 25
			dst = cv2.filter2D(cell, -1, kernel)

			thresh1 = 255 - cv2.adaptiveThreshold(dst, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, 2)

			if debug:
				cv2.imshow("prep", thresh1)
				cv2.waitKey(0)

			cell_tensor = cv2.resize(thresh1, (28, 28))

			cell_tensor = torch.Tensor(cell_tensor).float().view(1, 1, 28, 28)

			if torch.cuda.is_available():
				cell_tensor = cell_tensor.cuda()

			board[y][x] = torch.argmax(model(cell_tensor)[0]).item()

		x += 1
		total += 1

		if x == 9:
			x = 0
			y += 1

		if debug:
			cv2.imshow("cell", cell)
			cv2.waitKey(5)

	if debug:
		print board

	return board, rect_ids, rect_dicts