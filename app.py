import streamlit as st
import numpy as np, math, io
import matplotlib.pyplot as plt

st.set_page_config(layout="wide", page_title="HELCON B&W RESULTS")

# --- BLUE UI ---
st.markdown("""
<style>
.stApp { background: #0B5CE0 !important; }
h1,h2,h3,p,span,label { color: white !important; }
[data-testid="stFileUploader"]{ background: rgba(255,255,255,0.15)!important; border:2px dashed white!important; border-radius:10px!important; }
[data-testid="stFileUploader"] *{ color:white!important; }
.stSlider label { color: white !important; font-weight: bold !important; }
.stButton button { background: white !important; color: #0B5CE0 !important; font-weight: 900 !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("<div style='border:3px solid white; padding:12px; display:flex; justify-content:space-between;'><b style='font-size:20px; letter-spacing:1px;'>Y-TYPE REFRACTORY ANCHOR — BLUE UI / B&W RESULTS</b><b>HELCON.COM</b></div>", unsafe_allow_html=True)
st.write("")

left, right = st.columns([1, 2])

with left:
    st.markdown("### 📤 Upload Sketch")
    up = st.file_uploader("Drop Y-sketch", type=["jpg","png","jpeg"])
    if up:
        st.image(up, use_container_width=True, caption="Input")

    st.markdown("### 🔧 Controls")
    a = st.slider("Overall Height (mm)", 60, 300, 100)
    dia = st.slider("Wire Ø (mm)", 6, 16, 10)
    ang = st.slider("Angle °", 30, 120, 60)
    foot = st.slider("Foot Width (mm)", 20, 60, 40)
    R = dia * 0.9

    st.markdown(f"""
    <div style='border:2px solid white; padding:12px; background: rgba(255,255,255,0.1);'>
    <b>BOLD SPECS:</b><br>
    • Height: {a}mm (a-3)<br>
    • Foot: {foot}mm<br>
    • Angle: {ang}° ±5°<br>
    • R: {R:.0f}<br>
    • Ø: {dia}mm<br>
    • Grade: SS310 / 1.4841
    </div>
    """, unsafe_allow_html=True)

def draw_bw_bold(a, dia, ang, foot, R):
    fig = plt.figure(figsize=(11,8), dpi=300)
    fig.patch.set_facecolor('white')
    ax = fig.add_axes([0,0,1,1])
    ax.set_xlim(0,100); ax.set_ylim(0,70)
    ax.axis('off'); ax.set_facecolor('white')

    # BOLD BLACK BORDER like first photo
    ax.plot([2,98],[2,2], c='black', lw=2.5)
    ax.plot([2,98],[62,62], c='black', lw=2.5)
    ax.plot([2,2],[2,62], c='black', lw=2.5)
    ax.plot([98,98],[2,62], c='black', lw=2.5)

    # Title
    ax.text(50, 59, "ENGINEERING DRAWING - Y-TYPE REFRACTORY ANCHOR", c='black', ha='center', fontsize=11, weight='900')
    ax.text(50, 56.5, f"ALL DIMENSIONS IN MILLIMETERS - TOLERANCE ±0.2mm - SCALE 1:1", c='black', ha='center', fontsize=6, weight='bold')

    # SINGLE BOLD Y - BLACK
    sx, sy = 50, 15
    sh = 20
    arm_len = 22
    rad = math.radians(ang)
    x1 = sx - arm_len*math.sin(rad)
    y1 = sy+sh + arm_len*math.cos(rad)
    x2 = sx + arm_len*math.sin(rad)
    y2 = sy+sh + arm_len*math.cos(rad)

    # Thick black Y
    ax.plot([sx,sx],[sy+1.5,sy+sh], c='black', lw=6, solid_capstyle='round')
    ax.plot([sx,x1],[sy+sh,y1], c='black', lw=6, solid_capstyle='round')
    ax.plot([sx,x2],[sy+sh,y2], c='black', lw=6, solid_capstyle='round')
    ax.plot([sx-foot/2.2, sx+foot/2.2],[sy,sy+1.2], c='black', lw=6, solid_capstyle='round')

    # Centerlines - dashed
    ax.plot([sx,sx],[sy+1.5,sy+sh], c='black', lw=0.8, ls='--', alpha=0.5)
    ax.plot([sx,x1],[sy+sh,y1], c='black', lw=0.8, ls='--', alpha=0.5)
    ax.plot([sx,x2],[sy+sh,y2], c='black', lw=0.8, ls='--', alpha=0.5)
    ax.axvline(50, ls='--', lw=0.6, c='black', alpha=0.4)
    ax.axhline(sy+sh, ls='--', lw=0.6, c='black', alpha=0.4)

    # BOLD DIMENSIONS - 100mm Overall Height
    ax.annotate("", xy=(18, sy), xytext=(18, y1), arrowprops=dict(arrowstyle='<->', color='black', lw=1.2))
    ax.plot([16,24],[sy,sy], c='black', lw=1); ax.plot([16,24],[y1,y1], c='black', lw=1)
    ax.text(10, (sy+y1)/2, f"{a}mm\nOVERALL HEIGHT\na-3", c='black', fontsize=11, weight='900', ha='center', va='center')

    # Foot width 40mm
    ax.annotate("", xy=(sx-foot/2.2, sy-2), xytext=(sx+foot/2.2, sy-2), arrowprops=dict(arrowstyle='<->', color='black', lw=1.2))
    ax.text(sx, sy-4.5, f"{foot}mm - FOOT WIDTH", c='black', fontsize=10, weight='900', ha='center')

    # Angle
    ax.text(sx-12, sy+sh+6, f"{ang}°", c='black', fontsize=10, weight='900', ha='center',
            bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.2'))
    ax.text(sx+12, sy+sh+6, f"{ang}°", c='black', fontsize=10, weight='900', ha='center',
            bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.2'))

    # R Radius
    ax.text(x1-3, y1-3, f"R{R:.0f}", c='black', fontsize=8, weight='900',
            bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.2'))
    ax.text(x2+1, y2-3, f"R{R:.0f}", c='black', fontsize=8, weight='900',
            bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.2'))

    # Dia
    ax.text(sx+4, sy+8, f"Ø{dia}", c='black', fontsize=8, weight='900')

    # NOTES
    ax.text(4, 9, f"NOTES:\n• MAT: SS310 / 1.4841 Ø{dia}mm\n• ANGLE: {ang}° ±5°\n• BEND R: R{R:.0f}\n• FINISH: RAW",
            c='black', fontsize=5.5, weight='bold', va='bottom',
            bbox=dict(facecolor='white', edgecolor='black', lw=1, pad=2))

    # TITLE BLOCK - like first carabiner photo - BOLD
    # Row 1 headers
    yb = 3
    ax.plot([3,97],[yb+6,yb+6], c='black', lw=1)
    ax.plot([3,97],[yb,yb], c='black', lw=1)
    ax.plot([25,25],[yb,yb+6], c='black', lw=1)
    ax.plot([45,45],[yb,yb+6], c='black', lw=1)
    ax.plot([65,65],[yb,yb+6], c='black', lw=1)
    ax.plot([78,78],[yb,yb+6], c='black', lw=1)

    ax.text(4, yb+4.5, "Piece to draw:", fontsize=5, weight='bold', c='black')
    ax.text(4, yb+1.5, f"Y-Type Anchor\n{a}x{foot}x{dia}", fontsize=6, weight='900', c='black', va='center')

    ax.text(26, yb+4.5, "Date:", fontsize=5, weight='bold', c='black')
    ax.text(26, yb+1.5, "11-09-2026", fontsize=6, weight='900', c='black')

    ax.text(46, yb+4.5, "Company:", fontsize=5, weight='bold', c='black')
    ax.text(46, yb+1.5, "HELCON", fontsize=7, weight='900', c='black')

    ax.text(66, yb+4.5, "Scale:", fontsize=5, weight='bold', c='black')
    ax.text(66, yb+1.5, "1:1", fontsize=6, weight='900', c='black')

    ax.text(79, yb+4.5, "Drawing No:", fontsize=5, weight='bold', c='black')
    ax.text(79, yb+1.5, "1", fontsize=6, weight='900', c='black')

    return fig

with right:
    st.markdown("<div style='background:white; padding:8px; border-radius:8px;'><p style='color:black!important; text-align:center; font-weight:900; margin:0;'>BLACK & WHITE BOLD RESULT</p></div>", unsafe_allow_html=True)
    st.write("")
    fig = draw_bw_bold(a, dia, ang, foot, R)
    st.pyplot(fig, use_container_width=True)

    buf = io.BytesIO()
    fig.savefig(buf, format='pdf', facecolor='white', bbox_inches='tight')
    st.download_button("⬇️ DOWNLOAD B&W PDF (BOLD)", buf.getvalue(), file_name=f"HELCON_BW_BOLD_{a}x{foot}.pdf", mime="application/pdf", use_container_width=True)

    try:
        import ezdxf
        doc = ezdxf.new(); msp = doc.modelspace()
        sx, sy = 0,0; sh=20; arm_len=22; rad=math.radians(ang)
        x1 = -arm_len*math.sin(rad); y1 = sh+arm_len*math.cos(rad)
        x2 = arm_len*math.sin(rad); y2 = sh+arm_len*math.cos(rad)
        msp.add_line((0,0),(0,sh)); msp.add_line((0,sh),(x1,y1)); msp.add_line((0,sh),(x2,y2))
        s = io.StringIO(); doc.write(s)
        st.download_button("⬇️ DOWNLOAD DXF", s.getvalue(), file_name=f"HELCON_{a}x{foot}.dxf", use_container_width=True)
    except: pass
