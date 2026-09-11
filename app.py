import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np, io, math

st.set_page_config(page_title="HELCON BLUEPRINT", layout="wide")

# BLUEPRINT CSS - Makes whole Streamlit app blue
st.markdown("""
<style>
.stApp { background-color: #0F6FFF !important; background-image: 
linear-gradient(rgba(255,255,255,0.07) 1px, transparent 1px),
linear-gradient(90deg, rgba(255,255,255,0.07) 1px, transparent 1px);
background-size: 20px 20px; }
h1,h2,h3,p,label,div { color: white !important; }
.stSlider > div { color: white; }
[data-testid="stFileUploader"] { border: 2px dashed white; background: rgba(255,255,255,0.1); }
</style>
""", unsafe_allow_html=True)

st.markdown("## Y-TYPE REFRACTORY ANCHOR &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; HELCON.COM")
st.markdown("---")

# PARAMS - Handles infinite
c1, c2, c3 = st.columns(3)
with c1: a = st.slider("a - Overall Height", 40, 300, 100)
with c2: dia = st.slider("Ø - Wire Dia", 6, 16, 10)
with c3: angle = st.slider("Angle", 30, 120, 75)

uploaded = st.file_uploader("Drop any sketch", type=["jpg","png","jpeg"])

def draw_blueprint(a, dia, angle):
    fig = plt.figure(figsize=(16,10), dpi=250)
    fig.patch.set_facecolor('#0F6FFF')
    ax = fig.add_axes([0,0,1,1])
    ax.set_xlim(0, 1000); ax.set_ylim(0, 700)
    ax.axis('off')
    ax.set_facecolor('#0F6FFF')

    # Grid
    for x in range(0,1000,20):
        ax.plot([x,x],[0,700], color='white', lw=0.2, alpha=0.15)
    for y in range(0,700,20):
        ax.plot([0,1000],[y,y], color='white', lw=0.2, alpha=0.15)

    # Outer border + Rulers
    ax.plot([10,990],[680,680], c='white', lw=1.5)
    ax.plot([10,990],[20,20], c='white', lw=1.5)
    ax.plot([20,20],[20,680], c='white', lw=1.5)
    ax.plot([980,980],[20,680], c='white', lw=1.5)

    # Top title like MO2E
    ax.text(30, 690, "Y-TYPE REFRACTORY ANCHOR", color='white', fontsize=14, weight='bold', va='center')
    ax.text(900, 690, "HELCON.COM", color='white', fontsize=10, va='center')
    ax.text(100, 660, "Plan", color='white', fontsize=8, bbox=dict(edgecolor='white', facecolor='none'))

    # --- FIG 3 SIDE VIEW (main like bottle side) ---
    cx, cy = 500, 200
    stem_h = 150
    arm_len = 120
    rad = math.radians(angle/2)
    x1 = cx - arm_len*math.sin(rad); y1 = cy+stem_h + arm_len*math.cos(rad)
    x2 = cx + arm_len*math.sin(rad); y2 = cy+stem_h + arm_len*math.cos(rad)

    # Draw Y
    ax.plot([cx,cx],[cy,cy+stem_h], c='white', lw=dia*0.8)
    ax.plot([cx,x1],[cy+stem_h,y1], c='white', lw=dia*0.8)
    ax.plot([cx,x2],[cy+stem_h,y2], c='white', lw=dia*0.8)
    ax.plot([cx-40,cx+40],[cy,cy+6], c='white', lw=4) # foot

    # Dimensions
    ax.annotate("", xy=(cx+120, cy), xytext=(cx+120, cy+stem_h+arm_len), arrowprops=dict(arrowstyle='<->', color='white'))
    ax.text(cx+130, cy+80, f"{a}mm\nOVERALL HEIGHT", color='white', fontsize=8)

    ax.annotate("", xy=(cx-40, cy-10), xytext=(cx+40, cy-10), arrowprops=dict(arrowstyle='<->', color='white'))
    ax.text(cx, cy-30, "Ø50mm", color='white', ha='center', fontsize=9, weight='bold')

    # Angle
    ax.text(cx, y1-30, f"{angle}°", color='white', ha='center', fontsize=10)
    
    # Callouts 1,2,3,4 like MO2E
    ax.text(130, 420, "Logo", color='white', fontsize=7); ax.plot([130,200],[418,418], c='white', lw=0.5); ax.text(210,416,"1",color='white', weight='bold')
    ax.text(130, 300, 'Letter "O"', color='white', fontsize=7); ax.plot([130,200],[298,298], c='white', lw=0.5); ax.text(210,296,"2",color='white', weight='bold')
    ax.text(350, 400, "Bottle holder", color='white', fontsize=7); ax.text(410,390,"3",color='white', weight='bold')
    ax.text(550, 550, "Bottle", color='white', fontsize=7); ax.text(620,540,"4",color='white', weight='bold')

    # Title block
    ax.text(750, 150, "TITLE: Y-TYPE REFRACTORY ANCHOR\nPART NO: YRA-100-75\nDRAWING NO: HEL-YRA-100-75  SCALE:1:1\nDRAWN: 2024-09-11 | ENG  SHEET:1 OF 1\nMATERIAL: REFRACTORY STEEL WIRE Ø10mm\nHELCON.COM | TECHNICAL DOC", 
            color='black', fontsize=6, bbox=dict(facecolor='white', edgecolor='black', pad=5))

    return fig

if True: # always show
    fig = draw_blueprint(a, dia, angle)
    st.pyplot(fig, use_container_width=True)
    buf = io.BytesIO()
    fig.savefig(buf, format='pdf', facecolor='#0F6FFF')
    st.download_button("⬇️ DOWNLOAD BLUEPRINT PDF", buf.getvalue(), file_name="HELCON_BLUEPRINT.pdf", mime="application/pdf")
    plt.close(fig)
