import cv2
import numpy as np

def clean_and_straighten(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)
    kernel = np.ones((2,2), np.uint8)
    cleaned = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    lines = cv2.HoughLinesP(cleaned, 1, np.pi/180, 80, minLineLength=50, maxLineGap=10)
    straight_points = []
    if lines is not None:
        for line in lines:
            x1,y1,x2,y2 = line[0]
            straight_points.append(((x1,y1),(x2,y2)))
    return cleaned, straight_points