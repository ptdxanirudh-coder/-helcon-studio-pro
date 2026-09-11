import cv2
import numpy as np

def detect_all_anchors(cleaned_image):
    if len(cleaned_image.shape)==3:
        gray = cv2.cvtColor(cleaned_image, cv2.COLOR_BGR2GRAY)
    else:
        gray = cleaned_image
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    anchors = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < 800: continue
        x,y,w,h = cv2.boundingRect(cnt)
        if w < 20 or h < 20: continue
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
        bends = len(approx)
        if bends <=3: family="V-Type"
        elif bends==4: family="Y-Type"
        elif bends==5: family="L-Type / J-Type"
        elif bends<=7: family="U-Type / C-Type"
        else: family="S-Type / Custom"
        anchors.append({"bbox":(x,y,w,h), "contour":cnt, "bends":bends, "family":family, "points":approx})
    anchors = sorted(anchors, key=lambda a: a["bbox"][0])
    return anchors[:8]
