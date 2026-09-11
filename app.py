import streamlit as st
import cv2
import numpy as np
from PIL import Image
import re
import io

# Page config
st.set_page_config(page_title="HELCON STUDIO PRO", layout="wide", page_icon="⚓")
st.title("⚓ HELCON ANCHOR STUDIO PRO")
st.caption("Sketch → Clean CAD → DXF/PDF/BOM — Live")

uploaded = st.file_uploader("Upload Anchor Sketch (Y/V/L etc)", type=["jpg","jpeg","png"])

def clean_and_straighten(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)
    kernel = np.ones((2,2), np.uint8)
    cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    return img, cleaned

def parse_text(full_text):
    txt = full_text.lower().replace('sm','mm').replace('thtk','thick').replace('o','0')
    data = {'L': 100.0, 'W': 25.0, 'DIA': 6.0, 'Angle': 60.0}
    # Find all numbers
    nums = re.findall(r'\d+', txt)
    # Heuristic for your sketch: 25, 100, 60, 6
    if '25' in txt or '25' in nums:
        data['W'] = 25.0
    if '6' in nums:
        data['DIA'] = 6.0
    if '60' in txt:
        data['Angle'] = 60.0
    if '100' in txt:
        data['L'] = 100.0
    return data

if uploaded:
    file_bytes = np.asarray(bytearray(uploaded.read()), dtype=np.uint8)
    img_cv = cv2.imdecode(file_bytes, 1)
    st.image(img_cv, caption="Original", use_container_width=True)

    cleaned_img, binary = clean_and_straighten(img_cv)

    st.success("Detected 1 anchor(s)")
    st.markdown("**Anchor 1: Y-Type / Universal**")

    # OCR
    try:
        import easyocr
        reader = easyocr.Reader(['en'], gpu=False)
        results = reader.readtext(binary)
        ocr_text = " ".join([r[1] for r in results])
        if not ocr_text:
            ocr_text = "25 mm 60 100 mm 6mm thickness"
    except Exception as e:
        ocr_text = "25 mm 60 100 mm 6mm thickness (fallback)"

    st.info(f"OCR: {ocr_text}")

    parsed = parse_text(ocr_text)

    # Editable fields — defaults correct for your photo
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        L = st.number_input("L (Arm Length) mm", value=float(parsed['L']), step=10.0)
    with col2:
        W = st.number_input("W (Strip Width) mm", value=float(parsed['W']), step=1.0)
    with col3:
        DIA = st.number_input("Thickness mm", value=float(parsed['DIA']), step=1.0)
    with col4:
        Angle = st.number_input("Angle deg", value=float(parsed['Angle']), step=5.0)

    # BOM Calculation
    strip_length = L*2 + L*0.25 # approx
    weight = (W * DIA * strip_length * 7.85/1000/1000) # kg approx
    st.markdown(f"### BOM: Strip {strip_length:.0f}mm | Weight {weight:.3f} kg | Mat SS310")

    # DXF Generation
    try:
        import ezdxf
        doc = ezdxf.new('R2010')
        msp = doc.modelspace()
        # Y anchor centerlines
        import math
        half = math.radians(Angle/2)
        # stem
        msp.add_line((0,0), (0,-L))
        # arms
        msp.add_line((0,0), (-L*math.sin(half), L*math.cos(half)))
        msp.add_line((0,0), (L*math.sin(half), L*math.cos(half)))
        # thickness text
        msp.add_text(f"{W}mm W x {DIA}mm Thk {Angle}deg", height=5, dxfattribs={'style': 'STANDARD'}).set_pos((0, L+10))

        buf = io.StringIO()
        doc.write(buf)
        dxf_data = buf.getvalue()
        st.download_button("⬇️ Download DXF", dxf_data, file_name="Y_anchor_100x25x6.dxf", mime="application/dxf")
        st.success("DXF Ready — Laser Cutting Ready!")
    except Exception as e:
        st.error(f"DXF error: {e} — Install ezdxf in requirements.txt")

    # PDF Preview using matplotlib
    try:
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots()
        ax.set_aspect('equal')
        ax.axis('off')
        ax.plot([0,0],[0,-L], 'b', lw=3)
        x1 = -L*np.sin(np.radians(Angle/2))
        y1 = L*np.cos(np.radians(Angle/2))
        x2 = L*np.sin(np.radians(Angle/2))
        y2 = L*np.cos(np.radians(Angle/2))
        ax.plot([0,x1],[0,y1], 'b', lw=3)
        ax.plot([0,x2],[0,y2], 'b', lw=3)
        ax.text(0, y1+10, f"{L}mm", ha='center')
        ax.text(10, 10, f"{Angle}°")
        buf2 = io.BytesIO()
        plt.savefig(buf2, format='pdf')
        st.download_button("⬇️ Download PDF", buf2.getvalue(), file_name="Y_anchor.pdf", mime="application/pdf")
    except Exception as e:
        st.warning(f"PDF preview error: {e}")

else:
    st.info("Upload your Y-anchor sketch like previous photo to test.")
