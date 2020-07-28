import cv2
import matplotlib.pyplot as plt
import numpy as np

# # Reading the image
# image = cv2.imread('test_image.png')

# # Making a copy of a image ( Always do this )
# lane_image = np.copy(image)


def canny(image):
	# Converting the image to a gray scale image
	gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

	# Blurs the image 
	blur = cv2.GaussianBlur(gray, (5,5), 0)

	# Finding the Gradient using Canny method
	canny = cv2.Canny(blur, 50, 150)

	return canny


def make_coordinates(image, line_parameters):
	try:
		slope, intercept = line_parameters
	except TypeError:
 		slope, intercept = 0,0
	y1 = image.shape[0]
	y2 = int(y1 * (3/5))
	x1 = int((y1 - intercept) / slope)
	x2 = int((y2 - intercept) / slope)
	return np.array([x1, y1, x2, y2])


def average_slope_intercept(image, lines):
	left_fit = []
	right_fit = []

	for line in lines:
		x1, y1, x2, y2 = line.reshape(4)
		parameters = np.polyfit((x1, x2), (y1, y2), 1)
		slope = parameters[0]
		intercept = parameters[1]

		if slope < 0:
			left_fit.append((slope, intercept))
		else:
			right_fit.append((slope, intercept))

	left_fit_average = np.average(left_fit, axis=0)
	right_fit_average = np.average(right_fit, axis=0)
	left_line = make_coordinates(image, left_fit_average)
	right_line = make_coordinates(image, right_fit_average)
	return np.array([left_line, right_line])


def display_lines(image, lines):
	line_image = np.zeros_like(image)
	if lines is not None:
		for x1, y1, x2, y2 in lines:

			# Drawing the lines on the image
			cv2.line(line_image, (x1, y1), (x2, y2), (255, 0 , 0), 10)

	return line_image


def region_of_interest(image):
	height = image.shape[0]
	polygons = np.array(
		[[(200, height), (1100, height), (550, 250)]]
		)

	# Creating a mask 
	mask = np.zeros_like(image)

	# Making a polygon on the mask
	cv2.fillPoly(mask, polygons, 255)

	# Creating a masked image 
	masked_image = cv2.bitwise_and(image, mask) 

	return masked_image


# canny_image = canny(lane_image)

# cropped_image = region_of_interest(canny_image)

# # Finding lines in the contour image
# lines = cv2.HoughLinesP(cropped_image, 2, np.pi/180, 100, np.array([]),
# 						minLineLength=40, maxLineGap=5)

# averaged_lines = average_slope_intercept(lane_image, lines)

# line_image = display_lines(lane_image, averaged_lines)

# # Adding lines to the original image
# combo_image = cv2.addWeighted(lane_image, 0.8, line_image, 1, 1)

# # Shows the image 
# cv2.imshow('results', combo_image)

# # Displays the image for infinite time 
# cv2.waitKey(0)


cap = cv2.VideoCapture("test2.mp4")
while (cap.isOpened):
	_, frame = cap.read()
	canny_image = canny(frame)

	cropped_image = region_of_interest(canny_image)

	# Finding lines in the contour image
	lines = cv2.HoughLinesP(cropped_image, 2, np.pi/180, 100, np.array([]),
							minLineLength=40, maxLineGap=5)

	averaged_lines = average_slope_intercept(frame, lines)

	line_image = display_lines(frame, averaged_lines)

	# Adding lines to the original image
	combo_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)

	# Shows the image 
	cv2.imshow('results', combo_image)

	# Displays the image for infinite time 
	if cv2.waitKey(1) == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()
