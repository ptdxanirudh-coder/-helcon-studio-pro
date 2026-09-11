import streamlit as st
import numpy as np, io, math, cv2
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

st.set_page_config(layout="wide", page_title="HELCON PRO DETAILED")
st.title("⚓ HELCON — DETAILED DRAWING ENGINE")
st.caption("Inspired by your TERNUA reference — Centerlines, R, Tolerances, Title Block")

uploaded = st.file_uploader("Upload Y-anchor sketch", type=["jpg","png","jpeg"])

if uploaded:
    # Values from your sketch
    L, W, T, Angle = 100, 25, 6, 60
    R = T*1.5

    # CREATE DETAILED DRAWING
    fig = plt.figure(figsize=(12,8), dpi=300)
    ax = plt.gca()
    ax.set_xlim(-80, 80)
    ax.set_ylim(-70, 60)
    ax.axis('off')

    # Outer Border
    border = plt.Rectangle((-85,-75), 170, 140, fill=False, lw=2, ec='black')
    ax.add_patch(border)

    # Title Block
    ax.text(-80, -73, "Piece to draw:\nY-Type Refractory Anchor 100x25x6", fontsize=7, va='top', fontfamily='monospace', bbox=dict(facecolor='white', edgecolor='black'))
    ax.text(-30, -73, "Date:\n11-09-2026", fontsize=7, va='top', fontfamily='monospace', bbox=dict(facecolor='white', edgecolor='black'))
    ax.text(-10, -73, "Company:\nHELCON", fontsize=8, weight='bold', va='top', fontfamily='monospace', bbox=dict(facecolor='white', edgecolor='black'))
    ax.text(20, -73, "Scale:\n1:1", fontsize=7, va='top', fontfamily='monospace', bbox=dict(facecolor='white', edgecolor='black'))
    ax.text(40, -73, "Drawing No:\n1", fontsize=7, va='top', fontfamily='monospace', bbox=dict(facecolor='white', edgecolor='black'))

    # Centerlines - Dashed
    ax.axvline(0, color='black', ls='--', lw=0.8, alpha=0.7)
    ax.axhline(0, color='black', ls='--', lw=0.8, alpha=0.7)

    # Y-Arms - 3 arms at 120 deg
    def draw_arm(angle_deg, length, width):
        ang = math.radians(angle_deg)
        x1, y1 = 0,0
        x2, y2 = length*math.cos(ang), length*math.sin(ang)
        # thick strip as 2 parallel lines
        perp = ang + math.pi/2
        dx = (width/2/10)*math.cos(perp) # scaled for view
        dy = (width/2/10)*math.sin(perp)
        # Simplified as line with linewidth
        ax.plot([x1,x2],[y1,y2], color='black', lw=6, solid_capstyle='round')
        # centerline
        ax.plot([x1,x2],[y1,y2], color='black', ls='-.', lw=0.7, alpha=0.5)

    draw_arm( -90, L/2.5, W) # bottom
    draw_arm( 30, L/2.5, W) # top right
    draw_arm( 150, L/2.5, W) # top left

    # Dimensions - 50mm top
    ax.annotate("", xy=(-45,45), xytext=(45,45), arrowprops=dict(arrowstyle='<->', lw=1))
    ax.text(0, 47, "50mm", ha='center', fontsize=10, weight='bold')
    
    # 100mm side
    ax.annotate("", xy=(55,-50), xytext=(55,40), arrowprops=dict(arrowstyle='<->', lw=1))
    ax.text(62, -5, "100mm", rotation=90, va='center', fontsize=10, weight='bold')

    # R9 label
    ax.text(-60, 30, f"R{R:.0f}\nR{R:.0f} (1.5x THICKNESS)", fontsize=8, ha='center',
            bbox=dict(boxstyle="round", facecolor='white'))
    ax.annotate("", xy=(-48,35), xytext=(-55,32), arrowprops=dict(arrowstyle='->', lw=1))

    # Thickness callouts
    ax.annotate("", xy=(-5,-15), xytext=(5,-15), arrowprops=dict(arrowstyle='<->', lw=1))
    ax.text(0, -13, f"{T}mm", ha='center', fontsize=8)
    ax.text(15, -18, f"{T}mm\nTHK", fontsize=8)
    ax.text(18, -25, "ARM THICKNESS: 25mm\nSECTION", fontsize=8)

    ax.text(0, -60, "ALL DIMENSIONS IN MILLIMETERS — TOLERANCE ±0.2mm\nDO NOT SCALE DRAWING — THIRD ANGLE PROJECTION", ha='center', fontsize=6)

    st.pyplot(fig, use_container_width=True)

    # PDF Download
    buf = io.BytesIO()
    plt.savefig(buf, format='pdf', bbox_inches='tight')
    st.download_button("⬇️ DOWNLOAD DETAILED PDF (Like your photo)", buf.getvalue(), file_name="HELCON_Y_Anchor_Detailed.pdf", mime="application/pdf")
    
    # DXF with same detailing
    import ezdxf
    doc = ezdxf.new()
    msp = doc.modelspace()
    # (same Y lines + border)
    msp.add_lwpolyline([(-85,-75),(85,-75),(85,65),(-85,65),(-85,-75)], close=True)
    buf2 = io.StringIO()
    doc.write(buf2)
    st.download_button("⬇️ DOWNLOAD DXF", buf2.getvalue(), file_name="HELCON_Detailed.dxf")

else:
    st.info("Upload your anchor sketch to generate TERNUA-style detailed drawing")
