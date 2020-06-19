import cv2
import numpy as np
import sys
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import pytesseract
from solver import inner_square, solve

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, 3, 1)
        self.conv2 = nn.Conv2d(32, 64, 3, 1)
        self.dropout1 = nn.Dropout2d(0.25)
        self.dropout2 = nn.Dropout2d(0.5)
        self.fc1 = nn.Linear(9216, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = self.conv1(x)
        x = F.relu(x)
        x = self.conv2(x)
        x = F.relu(x)
        x = F.max_pool2d(x, 2)
        x = self.dropout1(x)
        x = torch.flatten(x, 1)
        x = self.fc1(x)
        x = F.relu(x)
        x = self.dropout2(x)
        x = self.fc2(x)
        output = F.log_softmax(x, dim=1)
        return output


def empty_cell(cell):
	kernel = np.ones((7,7),np.float32) / 25
	dst = cv2.filter2D(cell, -1, kernel)

	thresh1 = 255 - cv2.adaptiveThreshold(dst, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 17, 2)

	kernel = np.ones((3,3),np.uint8)
	dilate = cv2.erode(thresh1, kernel, iterations = 1)

	dilate_inner = dilate[20:70, 20:70]

	#cv2.imshow("empty_cell", dilate_inner)
	#cv2.waitKey(0)

	return (dilate_inner.flatten() == 0).all()


def process(img, global_thresh=False):

	# Blur image for smoothness

	kernel = np.ones((7,7),np.float32) / 25
	dst = cv2.filter2D(im,-1,kernel)

	#cv2.imshow("smoothed", dst)

	# Binary thresholding and inversion

	if global_thresh:
		ret,thresh1 = cv2.threshold(dst, 127, 255, cv2.THRESH_BINARY)
		thresh1 = 255 - thresh1

	thresh1 = cv2.adaptiveThreshold(dst, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
	thresh1 = 255 - thresh1

	#cv2.imshow("thresholded", thresh1)


	# Dilate activations

	kernel = np.ones((5,5),np.uint8)
	dilate = cv2.dilate(thresh1, kernel, iterations = 1)

	#cv2.imshow("dilate", cv2.resize(dilate,(300,300)))

	# Extract contours

	if (cv2.__version__[0] > 3):
	    contours, hierarchy = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
	else:
	    dilate, contours, hierarchy = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

	if len(contours) != 0:
	    # draw in blue the contours that were founded
	    cv2.drawContours(dilate, contours, -1, 255, 3)

	    # find the biggest countour (c) by the area
	    c = max(contours, key = cv2.contourArea)
	    x,y,w,h = cv2.boundingRect(c)

	    # draw the biggest contour (c) in green

	    rect = ((x, y), (x + w, y + h))
	    #cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

	#cv2.imshow("raw", cv2.resize(img,(300,300)))

	return rect


# Build torch model

model = Net()

model.load_state_dict(torch.load(sys.argv[2], map_location=torch.device('cpu')))
model.eval()

im_name = sys.argv[1]

img = cv2.imread(im_name)
im = cv2.imread(im_name, 0)

#cv2.imshow("raw", cv2.resize(im,(500,500)))
rect = process(im)

#print rect
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

		#cv2.imshow("prep", thresh1)
		#cv2.waitKey(0)

		cell_tensor = cv2.resize(thresh1, (28, 28))

		cell_tensor = torch.Tensor(cell_tensor).float().view(1, 1, 28, 28)

		board[y][x] = torch.argmax(model(cell_tensor)[0]).item()

	x += 1
	total += 1

	#print y, x, total
	if x == 9:
		x = 0
		y += 1


	#cv2.imshow("cell", cell)
	#cv2.waitKey(5)

#print board

res = solve(board)


# Now draw solved numbers back into image
x = 0
y = 0

for i in rect_ids:
	rect = rect_dicts[i]
	cell = sub_image[rect[0][1]:rect[1][1], rect[0][0]:rect[1][0]]

	#cv2.imshow("cell", cell)
	#cv2.waitKey(0)

	cv2.putText(sub_image_rgb, str(int(board[x][y])), ((rect[0][1] + rect[1][1]) / 2, (rect[0][0] + rect[1][0]) / 2), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

	x += 1

	#print y, x, total
	if x == 9:
		x = 0
		y += 1





if res is None:
	print "no solution"

else:
	print res

cv2.imshow("yes", cv2.resize(sub_image_rgb, (600, 600)))
cv2.waitKey(0)