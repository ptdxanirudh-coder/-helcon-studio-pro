import ezdxf
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import trimesh

def build_all_files(anchor_data, dims, output_name):
    L = dims.get("L") or 120
    W = dims.get("W") or 60
    DIA = dims.get("DIA") or 8

    doc = ezdxf.new('R2010')
    doc.layers.add('OUTLINE', color=7)
    doc.layers.add('CENTERLINE', color=1, linetype='CENTER')
    doc.layers.add('BEND_MARKS', color=2)
    doc.layers.add('DIMENSION', color=3)
    doc.layers.add('TITLE', color=4)
    msp = doc.modelspace()

    family = anchor_data["family"]
    if "V" in family:
        pts = [(-W/2, L), (0, 0), (W/2, L)]
    elif "Y" in family:
        pts = [(0,0), (0, L*0.6), (-W/2, L), (0, L*0.6), (W/2, L)]
    else:
        pts = [(p[0][0]/3, p[0][1]/3) for p in anchor_data["points"][:5]]

    msp.add_lwpolyline(pts, dxfattribs={'layer':'OUTLINE'})

    try:
        msp.add_linear_dim(base=(0, -10), p1=pts[0], p2=pts[-1], angle=0, dxfattribs={'layer':'DIMENSION'}).render()
    except:
        pass

    msp.add_text(f"HELCON - {output_name}", height=5, dxfattribs={'layer':'TITLE'}).set_pos((0, -30))
    msp.add_text(f"Date: {datetime.now().strftime('%d-%m-%Y')} | L={L} W={W} DIA={DIA} | Weight: {L*DIA*0.0062:.3f} kg", height=2.5, dxfattribs={'layer':'TITLE'}).set_pos((0, -38))
    msp.add_text(f"BOM: 1x SS Wire {DIA}mm, Length {L}mm", height=2.5, dxfattribs={'layer':'TITLE'}).set_pos((0, -44))

    dxf_file = f"{output_name}.dxf"
    doc.saveas(dxf_file)

    pdf_file = f"{output_name}.pdf"
    c = canvas.Canvas(pdf_file, pagesize=A4)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(30, 800, f"HELCON ANCHORS - MANUFACTURING DRAWING")
    c.setFont("Helvetica", 10)
    c.drawString(30, 780, f"Anchor: {output_name} | Family: {family} | Date: {datetime.now().strftime('%d-%m-%Y')}")
    c.drawString(30, 765, f"L={L}mm W={W}mm DIA={DIA}mm | Weight: {L*DIA*0.0062:.3f} kg | Material: SS310")
    c.drawString(30, 750, f"BOM: SS Wire {DIA}mm x {L}mm")
    c.line(100, 600, 200, 700)
    c.line(200, 700, 300, 600)
    c.drawString(30, 500, "Front View | Top View | Side View - Auto Generated (Scale 1:2)")
    c.save()

    try:
        mesh = trimesh.creation.cylinder(radius=DIA/2, height=L)
        stl_file = f"{output_name}.stl"
        mesh.export(stl_file)
    except:
        stl_file = None

    return dxf_file, pdf_file, stl_file