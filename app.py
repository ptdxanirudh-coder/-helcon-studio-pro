import streamlit as st
import matplotlib.pyplot as plt
import numpy as np, io, math

st.set_page_config(page_title="HELCON BLUEPRINT", layout="wide")

# --- BLUEPRINT THEME CSS ---
st.markdown("""
<style>
.stApp {
  background-color: #0B65E8 !important;
  background-image: 
    linear-gradient(rgba(255,255,255,0.08) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.08) 1px, transparent 1px);
  background-size: 24px 24px;
}
h1,h2,h3,span,p,label { color: white !important; }
.stSlider label { color: white !important; }
hr { border-color: white !important; }
[data-testid="stFileUploader"]{
  background: rgba(255,255,255,0.12) !important;
  border: 1.5px dashed white !important;
}
[data-testid="stFileUploader"] * { color: white !important; }
</style>
""", unsafe_allow_html=True)

# --- HEADER LIKE X BOTTLE HOLDER ---
st.markdown("""
<div style="border:1.5px solid white; border-bottom:none; padding:8px 12px; display:flex; justify-content:space-between;">
  <span style="font-weight:800; letter-spacing:1px;">Y-TYPE REFRACTORY ANCHOR</span>
  <span>HELCON.COM</span>
</div>
<div style="border:1.5px solid white; height:1px;"></div>
""", unsafe_allow_html=True)

# Sliders still white
a = st.slider("OVERALL HEIGHT (a)", 60, 300, 100)
dia = st.slider("WIRE Ø", 6, 16, 10)
ang = st.slider("Y-ANGLE", 45, 120, 75)

def blueprint_fig(a, dia, ang):
    fig = plt.figure(figsize=(12,7.5), dpi=300)
    fig.patch.set_facecolor('#0B65E8')
    ax = fig.add_axes([0,0,1,1])
    ax.set_xlim(0,100); ax.set_ylim(0,65)
    ax.axis('off')
    ax.set_facecolor('#0B65E8')

    # fine grid
    for x in np.arange(0,100,2):
        ax.plot([x,x],[0,65], color='white', lw=0.15, alpha=0.12)
    for y in np.arange(0,65,2):
        ax.plot([0,100],[y,y], color='white', lw=0.15, alpha=0.12)

    # outer border
    ax.plot([2,98],[2,2], c='white', lw=1); ax.plot([2,98],[62,62], c='white', lw=1)
    ax.plot([2,2],[2,62], c='white', lw=1); ax.plot([98,98],[2,62], c='white', lw=1)

    # rulers - bottom and left like reference
    for i in range(0,101,5):
        ax.plot([i,i],[2,3.5 if i%10==0 else 2.8], c='white', lw=0.6)
        if i%10==0: ax.text(i,0.5,str(i), color='white', fontsize=4, ha='center')
    for i in range(0,66,5):
        ax.plot([2,3.5 if i%10==0 else 2.8],[i,i], c='white', lw=0.6)
        if i%10==0: ax.text(0.5,i,str(i), color='white', fontsize=4, va='center')

    # Label "Plan"
    ax.add_patch(plt.Rectangle((8,57),5,2, fill=False, ec='white', lw=0.8))
    ax.text(10.5,58,"Plan", color='white', fontsize=5, ha='center', va='center')

    # --- DRAWINGS - 3 VIEWS like your reference ---
    # 1. Top view (left circle) - foot Ø
    circle = plt.Circle((20,35), 9, fill=False, ec='white', lw=1.2)
    ax.add_patch(circle)
    ax.plot([20,20],[26,44], c='white', lw=0.4, ls='--')
    ax.plot([11,29],[35,35], c='white', lw=0.4, ls='--')
    ax.text(20,22,f"FOOT Ø50 - 8x Ø6 HOLES\nMATERIAL: ROUND WIRE DIA {dia}mm", color='white', fontsize=4.5, ha='center')

    # 2. Isometric Y (right top) - white thick
    cx, cy = 70, 40
    stem = 10
    arm = 12
    r = math.radians(ang/2)
    x1, y1 = cx - arm*math.sin(r), cy+stem + arm*math.cos(r)
    x2, y2 = cx + arm*math.sin(r), cy+stem + arm*math.cos(r)
    ax.plot([cx,cx],[cy,cy+stem], c='white', lw=2.5)
    ax.plot([cx,x1],[cy+stem,y1], c='white', lw=2.5)
    ax.plot([cx,x2],[cy+stem,y2], c='white', lw=2.5)
    # dims
    ax.annotate("", xy=(x1-1,y1), xytext=(x2+1,y2), arrowprops=dict(arrowstyle='<->', color='white', lw=0.6))
    ax.text(70,56,f"Ø50mm", color='white', fontsize=5, weight='bold', ha='center')
    ax.text(76,45,f"{arm}mm", color='white', fontsize=4, rotation=35)

    # 3. Side view (bottom center)
    sx, sy = 50, 12
    sx1, sy1 = sx - 8, sy+12
    sx2, sy2 = sx + 8, sy+12
    ax.plot([sx,sx],[sy+2,sy+8], c='white', lw=2.5)
    ax.plot([sx,sx1],[sy+8,sy1], c='white', lw=2.5)
    ax.plot([sx,sx2],[sy+8,sy2], c='white', lw=2.5)
    ax.plot([sx-6,sx+6],[sy,sy], c='white', lw=2)

    ax.annotate("", xy=(sx+10, sy), xytext=(sx+10, sy1), arrowprops=dict(arrowstyle='<->', color='white', lw=0.6))
    ax.text(sx+11, sy+6, f"{a}mm\nOVERALL HEIGHT", color='white', fontsize=4)
    ax.text(sx, sy1+1, f"{ang}°", color='white', fontsize=5, ha='center')

    # Notes like MO2E description
    ax.text(8, 8, f"NOTES:\n- MATERIAL: REFRACTORY STEEL Ø{dia}mm\n- Y-ANGLE: {ang}° INCLUDED\n- R9 BEND RADIUS AT Y-JUNCTION\n- OVERALL HEIGHT: {a}mm ±1.0mm\n- FOOT: Ø50mm\n- FINISH: RAW STEEL", color='white', fontsize=4.2, va='bottom',
            bbox=dict(facecolor='none', edgecolor='white', lw=0.5, pad=2))

    # Bottom footer like reference
    ax.text(50, 0.2, "HELCON.COM — Y-TYPE REFRACTORY ANCHOR — REV A — DATE: 11-09-2026 — ALL DIMENSIONS IN MM UNLESS NOTED", color='white', fontsize=3.5, ha='center')

    return fig

fig = blueprint_fig(a, dia, ang)
st.pyplot(fig, use_container_width=True)

buf = io.BytesIO()
fig.savefig(buf, format='pdf', facecolor='#0B65E8')
st.download_button("⬇️ DOWNLOAD BLUEPRINT PDF", buf.getvalue(), file_name=f"HELCON_BLUEPRINT_{a}x{dia}.pdf", mime="application/pdf")
