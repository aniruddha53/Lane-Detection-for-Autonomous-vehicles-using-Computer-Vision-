import cv2
import numpy as np
import matplotlib.pyplot as plt

def make_points(image, line):       #Defining coordinates of the line
    slope, intercept = line
    y1 = int(image.shape[0]) # bottom of the image
    y2 = int(y1*3/5)         # slightly lower than the middle
    x1 = int((y1 - intercept)/slope) # obtained after evaluating y = mx + b
    x2 = int((y2 - intercept)/slope) # obtained after evaluating y = mx + b
    return [[x1, y1, x2, y2]]

def average_slope_intercept(image, lines):
    left_fit    = []        #It will contain the coordinates of the line on left side
    right_fit   = []        #It will contain the coordinates of the line on right side
    if lines is None:
        return None
    for line in lines:
        for x1, y1, x2, y2 in line:
            fit = np.polyfit((x1,x2), (y1,y2), 1)   #This function gives us slope and the y-intercept for the given line, Last 1 indicates degree of polynomial
            slope = fit[0]      #Polyfit returns SLope at index 0
            intercept = fit[1]  #Polyfit returns Y-intercept at index 1
            if slope < 0: # y is reversed in image (Thus in our image, lines at the left will have positive slope and lines in the right will have positive slope
                left_fit.append((slope, intercept))
            else:
                right_fit.append((slope, intercept))
    if len(left_fit) and len(right_fit):
        # add more weight to longer lines
        left_fit_average  = np.average(left_fit, axis=0)        # Averaging out all the left side values
        right_fit_average = np.average(right_fit, axis=0)       # Averaging out all the right side values
        left_line  = make_points(image, left_fit_average)       # Function call to obtain new coordinates for averaged left line
        right_line = make_points(image, right_fit_average)      # Function call to obtain new coordinates for averaged right line
        averaged_lines = [left_line, right_line]
        return averaged_lines



def canny(image):       # This function converts RGB to Gray scale then blurring for noise removal and smoothening and at the end Canny for edge detection
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)    #convert color image to RGB image
    blur = cv2.GaussianBlur(gray, (5,5), 0)             #Last element is deviation which is set to 0
    canny = cv2.Canny(blur, 50, 100)        #For edge detection: 50: Lower Threshold and 150: Higher Threshold
    return canny


def display_lines(image, lines):
    line_image = np.zeros_like(image) #image having same size of our original image but with all black pixels
    if lines is not None:             #Checking if array of lines is not empty
        for line in lines:            #For each line in array we will convert it from two dimensional array to one dimensional array
            for x1, y1, x2, y2 in line:  # Just by unpacking array elements into 4 different variables we can convert them from 2-D to 1-D form
                cv2.line(line_image,(x1,y1),(x2,y2),(255,0,0),10)   # line() function draws a line between two points. 1st: Image || 2nd and 3rd: Coordinates of first and second point || 4th: Color (BGR) || 5th: Line Thickness
    return line_image

def region_of_interest(image):
    height = image.shape[0]     # .shape returns rows and columns. Since height equals to number of rows which is 700 in our case, thus index[0] means first value which is rows which is in turn the height
    polygons = np.array([[(200, height), (1100, height), (550, 250)]]) # Defining coordinates of the triangle which is our region of interest
    mask = np.zeros_like(image)     # creating image of same size as od image made up of all zeros (means a black pixeled image)
    cv2.fillPoly(mask, polygons, 255)     # FIlling the mask with the polygon which means our triange's coordinates
    masked_image = cv2.bitwise_and(image, mask) #Anding will display the part of image present in our area of interest
    return masked_image

cap = cv2.VideoCapture("test2.mp4")
while (cap.isOpened()):
    _, frame = cap.read()
    canny_image = canny(frame)
    cropped_image = region_of_interest(canny_image)
    lines = cv2.HoughLinesP(cropped_image, 2, np.pi/180, 100, np.array([]), minLineLength = 40, maxLineGap = 5) # 2nd and 3rd argument are for resolution, they determine the bin size. 2nd argument is rho which is distance resolution and 3rd is theta which is angle resolution Rho = 2 = precision of 2 pixel Theta = 1 = pi/180. This provided us the best result, 100 is the threshold for minimum number of intersections, next is a place holder array and others are self explainatory
    average_lines = average_slope_intercept(frame, lines)
    line_image = display_lines(frame, average_lines)
    combo_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)    # 0.8 and 1 are weights of the respective images, last one doesn't makes any substantial difference
    cv2.imshow('result', combo_image)
    if cv2.waitKey(1) == ord('q'):      # when q is pressed, stop video and close all windows
        break
cap.release()
cv2.destroyAllWindows()
