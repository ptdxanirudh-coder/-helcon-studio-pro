import streamlit as st
import cv2
import numpy as np
from PIL import Image
from anchor_engine.cleaner import clean_and_straighten
from anchor_engine.detector import detect_all_anchors
from anchor_engine.ocr_reader import read_dimensions
from anchor_engine.dxf_builder import build_all_files

@st.cache_resource
def load_ocr():
    from anchor_engine.ocr_reader import get_reader
    return get_reader()

st.set_page_config(page_title="HELCON Studio PRO", layout="wide")
st.title("HELCON Anchor Studio PRO - Universal")
st.caption("Any Shape V,Y,L,U,J,C,S | Auto-Straighten | OCR L=120 Ø8 90° | Multi-Anchor | DXF+PDF+STL+BOM")

left, right = st.columns([1,1])

with left:
    file = st.file_uploader("Upload sketch (1 paper with 4 anchors also works)", type=["jpg","png","jpeg"])
    if file:
        reader = load_ocr()
        img_pil = Image.open(file)
        st.image(img_pil, use_container_width=True)
        img_cv = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
        cleaned, _ = clean_and_straighten(img_cv)
        anchors = detect_all_anchors(cleaned)
        dims_auto, text_read = read_dimensions(np.array(img_pil), reader)
        st.success(f"Detected {len(anchors)} anchor(s)")
        for i,a in enumerate(anchors):
            st.write(f"Anchor {i+1}: {a['family']}")
        st.info(f"OCR: {text_read} -> {dims_auto}")
        L = st.number_input("L", value=float(dims_auto.get("L") or 120))
        W = st.number_input("W", value=float(dims_auto.get("W") or 60))
        DIA = st.number_input("DIA", value=float(dims_auto.get("DIA") or 8))
        ANG = st.number_input("Angle", value=float(dims_auto.get("ANGLE") or 90))
        st.session_state["dims"] = (L,W,DIA,ANG)
        st.session_state["anchors"] = anchors

with right:
    if file and "anchors" in st.session_state:
        if st.button("GENERATE DXF + PDF + STL + BOM"):
            L,W,DIA,ANG = st.session_state["dims"]
            for idx, anchor in enumerate(st.session_state["anchors"]):
                out_name = f"Anchor_{idx+1}_{anchor['family']}_{int(L)}x{int(W)}"
                dxf, pdf, stl = build_all_files(anchor, {"L":L,"W":W,"DIA":DIA,"ANGLE":ANG}, out_name)
                with open(dxf, "rb") as f:
                    st.download_button(f"Download {out_name}.DXF", f, file_name=dxf, key=f"dxf{idx}")
                with open(pdf, "rb") as f:
                    st.download_button(f"Download {out_name}.PDF", f, file_name=pdf, key=f"pdf{idx}")
                if stl:
                    with open(stl, "rb") as f:
                        st.download_button(f"Download {out_name}.STL", f, file_name=stl, key=f"stl{idx}")
            st.balloons()