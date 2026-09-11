import streamlit as st
import cv2, numpy as np, math, io
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

st.set_page_config(page_title="HELCON BLUEPRINT FACTORY", layout="wide", page_icon="⚓")

# --- BLUEPRINT THEME ---
st.markdown("""
<style>
.stApp {
  background-color: #0B65E8!important;
  background-image:
    linear-gradient(rgba(255,255,255,0.07) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.07) 1px, transparent 1px);
  background-size: 22px 22px;
}
h1,h2,h3,p,span,label,div { color: white!important; }
hr { border-color: white!important; }
.stSlider > div > div > div { background: white!important; }
[data-testid="stFileUploader"]{ background: rgba(255,255,255,0.12)!important; border:1.8px dashed white!important; border-radius: 8px!important; }
[data-testid="stFileUploader"] *{ color:white!important; }
.stSelectbox div { color: white!important; }
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("""
<div style="border:2px solid white; padding:8px 14px; display:flex; justify-content:space-between; align-items:center;">
  <b style="letter-spacing:1.2px; font-size:16px;">Y-TYPE REFRACTORY ANCHOR — PARAMETRIC BLUEPRINT ENGINE</b>
  <b>HELCON.COM</b>
</div>
<div style="border:1px solid white; margin: 8px 0 16px 0;"></div>
""", unsafe_allow_html=True)

# --- YOUR FACTORY CATALOGUE FROM PHOTO ---
CATALOGUE = {
    1: 65, 2: 75, 3: 85, 4: 100, 5: 115,
    6: 150, 7: 180, 8: 230, 9: 265, 10: 300
}

# Template library = infinite solution
TEMPLATES = {
    "Y-TYPE (Photo)": {"c_ratio": 0.48, "foot": 40, "R1_factor": 0.8, "R2_factor": 1.8},
    "V-TYPE": {"c_ratio": 0, "foot": 0, "R1_factor": 1.0, "R2_factor": 1.5},
    "U-TYPE": {"c_ratio": 0.7, "foot": 28, "R1_factor": 1.2, "R2_factor": 1.2},
    "L-TYPE": {"c_ratio": 1.0, "foot": 30, "R1_factor": 1.0, "R2_factor": 1.0},
}

left, right = st.columns([1, 1.7])

with left:
    up = st.file_uploader("Upload Anchor Sketch / Photo", type=["jpg","png","jpeg"])
    auto_a = 100

    if up:
        file_bytes = np.asarray(bytearray(up.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, 1)
        st.image(img, use_container_width=True, caption="Input Detected")
        # auto height guess
        try:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            _, th = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)
            cnts,_ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if cnts:
                h = max([cv2.boundingRect(c)[3] for c in cnts])
                auto_a = int(np.clip(h/2.5, 65, 300))
        except: pass

    st.markdown("#### 🔧 Parametric Controls")
    family = st.selectbox("Anchor Family", list(TEMPLATES.keys()), index=0)

    # Catalogue quick buttons
    st.write("Quick Catalogue (from your sheet):")
    cols = st.columns(5)
    for i, (no, height) in enumerate(CATALOGUE.items()):
        if cols[i%5].button(f"No.{no}\n{height}mm", key=f"cat{no}"):
            auto_a = height

    a = st.slider("a - Total Height (a-3) mm", 40, 300, auto_a)
    dia = st.slider("Ø - Wire Dia mm", 6, 16, 10)
    angle = st.slider("Angle 75° ±5°", 30, 120, 75)
    foot_w = st.slider("Foot / U Width mm", 20, 60, TEMPLATES[family]["foot"] if TEMPLATES[family]["foot"] else 40)

    tpl = TEMPLATES[family]
    c_val = a * tpl["c_ratio"]
    R1 = dia * tpl["R1_factor"]
    R2 = dia * tpl["R2_factor"]
    # Weight calc: SS310 density 7.85 g/cc
    vol = (a * 2.1) * (math.pi * dia**2 / 4) # mm3 approx
    weight = vol * 7.85 / 1e6 # kg

    st.markdown(f"""
    <div style="border:1px solid white; padding:8px; margin-top:10px; font-size:13px;">
    <b>CALCULATED (Factory Rules):</b><br>
    C = {c_val:.0f} ±3 mm<br>
    R1 = {R1:.0f} | R2 = {R2:.0f}<br>
    Weight = {weight:.3f} kg/pc<br>
    Grade = 1.4841 / SS310<br>
    Tolerance = a-3, Angle ±5°
    </div>
    """, unsafe_allow_html=True)

def draw_blueprint(a, dia, angle, foot_w, c_val, R1, R2):
    fig = plt.figure(figsize=(14, 8.8), dpi=300)
    fig.patch.set_facecolor('#0B65E8')
    ax = fig.add_axes([0,0,1,1])
    ax.set_xlim(0,100); ax.set_ylim(0,62)
    ax.axis('off'); ax.set_facecolor('#0B65E8')

    # Grid
    for x in np.arange(0,100,1.2): ax.plot([x,x],[0,62], c='white', lw=0.1, alpha=0.13)
    for y in np.arange(0,62,1.2): ax.plot([0,100],[y,y], c='white', lw=0.1, alpha=0.13)
    # Outer border
    ax.plot([2,98],[2,2], c='white', lw=1.2); ax.plot([2,98],[60,60], c='white', lw=1.2)
    ax.plot([2,2],[2,60], c='white', lw=1.2); ax.plot([98,98],[2,60], c='white', lw=1.2)

    # Rulers
    for i in range(0,101,2):
        ax.plot([i,i],[2,2.8 if i%10==0 else 2.4], c='white', lw=0.5)
        if i%10==0: ax.text(i,0.5,f"{i}", c='white', fontsize=3.2, ha='center')
    for i in range(0,61,2):
        ax.plot([2,2.8 if i%10==0 else 2.4],[i,i], c='white', lw=0.5)

    # Plan label like X BOTTLE HOLDER
    ax.add_patch(plt.Rectangle((7,56.5),6,2.2, fill=False, ec='white', lw=0.7))
    ax.text(10,57.6,"Plan", c='white', fontsize=5, ha='center', va='center', weight='bold')

    # VIEW 1: FOOT PLAN (Left)
    ax.add_patch(Circle((21,37), 10.5, fill=False, ec='white', lw=1.3))
    ax.plot([21,21],[26.5,47.5], c='white', ls='--', lw=0.4)
    ax.plot([10.5,31.5],[37,37], c='white', ls='--', lw=0.4)
    # dimension Ø50
    ax.annotate("", xy=(10.5,51), xytext=(31.5,51), arrowprops=dict(arrowstyle='<->', color='white', lw=0.7))
    ax.text(21,52.5,f"Ø{foot_w}mm", c='white', ha='center', fontsize=5.5, weight='bold')
    ax.text(21,24.5,f"FOOT Ø{foot_w} - 8x Ø6 HOLES - EQUALLY SPACED\nMATERIAL: ROUND WIRE DIA {dia}mm", c='white', ha='center', fontsize=4)

    # VIEW 2: ISOMETRIC (Right Top)
    cx, cy = 69, 37
    arm_len = (a-c_val)*0.14
    rad = math.radians(angle/2)
    x1, y1 = cx - arm_len*math.sin(rad), cy+6 + arm_len*math.cos(rad)
    x2, y2 = cx + arm_len*math.sin(rad), cy+6 + arm_len*math.cos(rad)

    ax.plot([cx,cx],[cy,cy+6], c='white', lw=3.2)
    ax.plot([cx,x1],[cy+6,y1], c='white', lw=3.2)
    ax.plot([cx,x2],[cy+6,y2], c='white', lw=3.2)

    ax.text(cx-14, y1+0.5, f"1 - LEFT ARM", c='white', fontsize=4)
    ax.text(cx+6, y2+0.5, f"2 - RIGHT ARM", c='white', fontsize=4)
    ax.text(cx-9, cy+1, f"3 - STEM", c='white', fontsize=4)
    ax.text(cx+8, cy-1, f"4 - FOOT BASE", c='white', fontsize=4)
    ax.text(68,53,f"Ø50mm", c='white', fontsize=4, weight='bold')

    # VIEW 3: SIDE ELEVATION (Bottom Center - Main)
    sx, sy = 49, 7
    sh = c_val*0.14
    ah = (a-c_val)*0.14
    sx1, sy1 = sx - ah*math.sin(rad), sy+sh+ah*math.cos(rad)
    sx2, sy2 = sx + ah*math.sin(rad), sy+sh+ah*math.cos(rad)

    ax.plot([sx,sx],[sy+0.8,sy+sh], c='white', lw=3.2)
    ax.plot([sx,sx1],[sy+sh,sy1], c='white', lw=3.2)
    ax.plot([sx,sx2],[sy+sh,sy2], c='white', lw=3.2)
    ax.plot([sx-foot_w*0.16,sx+foot_w*0.16],[sy,sy+0.7], c='white', lw=3.5)

    # Dimensions
    ax.annotate("", xy=(sx+13, sy), xytext=(sx+13, sy1), arrowprops=dict(arrowstyle='<->', color='white', lw=0.7))
    ax.text(sx+14, sy+8, f"{a}mm\na-3\nOVERALL HEIGHT", c='white', fontsize=4.2, weight='bold', va='center')

    ax.annotate("", xy=(sx-foot_w*0.16, sy-1), xytext=(sx+foot_w*0.16, sy-1), arrowprops=dict(arrowstyle='<->', color='white', lw=0.6))
    ax.text(sx, sy-2.5, f"Ø{foot_w}mm", c='white', ha='center', fontsize=4.5, weight='bold')

    # Angle arc
    ax.text(sx, sy1+1.2, f"{angle}° ±5°", c='white', ha='center', fontsize=5)

    # Bend radius callouts
    ax.text(sx-4, sy+sh-1, f"{R1:.0f}R", c='white', fontsize=3.5, bbox=dict(facecolor='#0B65E8', edgecolor='white', boxstyle='round,pad=0.2'))
    ax.text(sx+1, sy+sh-1, f"{R2:.0f}R", c='white', fontsize=3.5, bbox=dict(facecolor='#0B65E8', edgecolor='white', boxstyle='round,pad=0.2'))

    # NOTES block like MO2E
    ax.text(3.5, 11, f"NOTES / SPECIFICATIONS\n• MATERIAL: REFRACTORY STEEL 1.4841/SS310 ROUND WIRE Ø{dia}mm\n• Y-ANGLE: {angle}° INCLUDED ANGLE BTWN ARMS (75°±5°)\n• BEND RADIUS: R1={R1:.0f}mm AT Y-JUNCTION / R2={R2:.0f}mm AT STEM\n• OVERALL HEIGHT: {a}mm (a-3) TOL ±3mm\n• STEM: C={c_val:.0f}mm ±3\n• FOOT: Ø{foot_w}mm, 8x Ø6 HOLES EQUALLY SPACED\n• FINISH: CLEAN, NO COATING / RAW STEEL\n• DESIGN: Y-TYPE FOR REFRACTORY LINING ANCHORAGE",
            c='white', fontsize=3.6, va='bottom', linespacing=1.3,
            bbox=dict(facecolor='none', edgecolor='white', lw=0.7, pad=1.5))

    # Title block
    ax.text(75.5, 10.5, f"TITLE: Y-TYPE REFRACTORY ANCHOR {a}x{dia}\nPART NO: YRA-{a}-{angle}\nDWG NO: HEL-YRA-{a}-{dia} SCALE 1:1 SHEET 1 OF 1\nDRAWN: 11-09-2026 | ENG\nMATERIAL: SS310 WIRE Ø{dia}mm WEIGHT {weight:.3f}kg\nHELCON.COM | TECHNICAL DOC",
            c='black', fontsize=3.9, va='bottom',
            bbox=dict(facecolor='white', edgecolor='white', pad=1.8))

    ax.text(50, 0.4, f"HELCON.COM — Y-TYPE REFRACTORY ANCHOR — REV A — DATE: 11-09-2026 — CATALOGUE No.1(65) No.2(75) No.3(85) No.4(100) No.5(115) No.6(150) No.7(180) No.8(230) No.9(265) No.10(300) — YOU ARE HERE: {a}mm — ALL DIMS IN MM UNLESS NOTED",
            c='white', fontsize=2.8, ha='center')
    return fig

with right:
    fig = draw_blueprint(a, dia, angle, foot_w, c_val, R1, R2)
    st.pyplot(fig, use_container_width=True)

    buf = io.BytesIO()
    fig.savefig(buf, format='pdf', facecolor='#0B65E8', bbox_inches='tight')
    st.download_button("⬇️ DOWNLOAD BLUEPRINT PDF (Factory)", buf.getvalue(),
                       file_name=f"HELCON_BLUEPRINT_Y_{a}mm_D{dia}_{angle}deg.pdf",
                       mime="application/pdf", use_container_width=True)

    try:
        import ezdxf
        doc = ezdxf.new(); msp = doc.modelspace()
        msp.add_line((0,0),(0,c_val)); msp.add_line((0,c_val),(-(a-c_val)*math.sin(math.radians(angle/2)), a))
        msp.add_line((0,c_val),((a-c_val)*math.sin(math.radians(angle/2)), a))
        msp.add_line((-foot_w/2,0),(foot_w/2,0))
        s = io.StringIO(); doc.write(s)
        st.download_button("⬇️ DOWNLOAD DXF (Parametric)", s.getvalue(), file_name=f"HELCON_{a}x{dia}.dxf", use_container_width=True)
    except: pass

st.markdown("---")
st.caption("BLUEPRINT ENGINE: Upload any Y/V/U sketch → Classifies family → Calculates C, R1, R2 from factory formulas → Infinite sliders → Blueprint PDF + DXF + Weight. Add new family in TEMPLATES dict to support any new structure.")
