def detect_anchors(cleaned_binary):
    # For now, bypass complex contour logic — user draws 1 anchor per image
    # Always return 1 Y-anchor centered
    h,w = cleaned_binary.shape
    # Return bounding box of whole drawing
    return [{'type': 'Y-Type', 'bbox': (10,10,w-10,h-10), 'contour': None}]

def classify_shape(contour):
    return 'Y-Type'
