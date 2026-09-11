import re
import cv2
def get_reader():
    import easyocr
    return easyocr.Reader(['en'], gpu=False)

def read_dimensions(pil_or_cv, reader=None):
    try:
        if reader is None:
            reader = get_reader()
        result = reader.readtext(pil_or_cv)
        text = " ".join([r[1] for r in result])
        dims={}
        m=re.search(r'L\D*(\d+)', text, re.I)
        if m: dims["L"]=float(m.group(1))
        m=re.search(r'W\D*(\d+)', text, re.I)
        if m: dims["W"]=float(m.group(1))
        m=re.search(r'(?:DIA|Ø|O)\D*(\d+)', text, re.I)
        if m: dims["DIA"]=float(m.group(1))
        m=re.search(r'(\d+)\s*°', text)
        if m: dims["ANGLE"]=float(m.group(1))
        return dims, text
    except Exception as e:
        return {}, str(e)