from extract_soduko import process_one, process_two, empty_cell
from digit_classifier import Net
from backtrack_solver import solve
import argparse
import torch
import cv2

def draw_solved_board(img, solved_board, rect_ids, rect_dicts):
	"""

	Take a solved board and img and draw numbers onto board
	"""

	img_bw = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	x = 0
	y = 0

	print len(rect_dicts)

	for i in rect_ids:
		rect = rect_dicts[i]
		cell = sub_image[rect[0][1]:rect[1][1], rect[0][0]:rect[1][0]]

		#cv2.imshow("cell", cell)
		#cv2.waitKey(0)

		cv2.putText(img, str(int(board[x][y])), ((rect[0][1] + rect[1][1]) / 2, (rect[0][0] + rect[1][0]) / 2), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

		x += 1

		if x == 9:
			x = 0
			y += 1

	return img

parser = argparse.ArgumentParser(description='Solve soduko')
parser.add_argument('--image_path', '-i', type=str, help='path to input image', required=True)
parser.add_argument('--weight_path', '-w', default='mnist_cnn.pt', type=str, help='path to model weights')
parser.add_argument('--debug', action='store_true', default=False, help='allow debug printing')

args = parser.parse_args()

debug = args.debug

# Build torch model and load pretrained MNIST weights

model = Net()
model.load_state_dict(torch.load(args.weight_path, map_location=torch.device('cpu')))
model.eval()

img = cv2.imread(args.image_path)

cv2.imshow("input image", cv2.resize(img, (500, 500)))

# Step one of image processing
rect = process_one(img, debug=debug)

# Step two of image processing
board, rect_ids, rect_dicts = process_two(img, rect, model)

# Apply vanilla backtracker to solve soduko CSP
board_solved = solve(board)

if board_solved is None:
	print "no solution to input board"
	exit()

# Display solved board numbers atop original image

sub_image = img[rect[0][1]:rect[1][1], rect[0][0]:rect[1][0]]

solved_board_with_numbers = draw_solved_board(sub_image, board_solved, rect_ids, rect_dicts)
cv2.imshow("solved board", cv2.resize(solved_board_with_numbers, (600, 600)))
cv2.waitKey(0)

#cv2.imwrite("solved_" + sys.argv[1], cv2.resize(sub_image_rgb, (600, 600)))