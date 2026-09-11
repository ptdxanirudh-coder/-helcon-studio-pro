import cv2
import numpy as np

def clean_and_straighten(img):
    # Convert to gray
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 1. Remove notebook lines (inpaint light gray lines)
    # Threshold for blue/black ink only
    _, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)

    # Clean small noise
    kernel = np.ones((2,2), np.uint8)
    cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    # 2. Try to find angle, but SAFE (no crash if no lines)
    try:
        lines = cv2.HoughLinesP(cleaned, 1, np.pi/180, 100, minLineLength=100, maxLineGap=10)
        if lines is not None and len(lines) > 0:
            angles = []
            for line in lines:
                x1,y1,x2,y2 = line[0]
                angle = np.degrees(np.arctan2(y2-y1, x2-x1))
                # Only near horizontal lines (notebook lines)
                if abs(angle) < 10:
                    angles.append(angle)
            if angles:
                median_angle = np.median(angles)
                (h,w) = img.shape[:2]
                M = cv2.getRotationMatrix2D((w//2, h//2), median_angle, 1.0)
                img = cv2.warpAffine(img, M, (w,h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    except:
        pass # If any error, just skip straightening

    # Return cleaned original and binary
    return img, cleaned
