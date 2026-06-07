import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

KAMPUS = "Universitas Muhammadiyah Palu"
PRODI  = "Program Studi Informatika"
OPERATOR = "Nursalim, S.Kom., M.Kom."

PRIMARY   = colors.HexColor("#2563EB")
DARK      = colors.HexColor("#1E293B")
LIGHT_BG  = colors.HexColor("#EFF6FF")
GRAY      = colors.HexColor("#64748B")
WHITE     = colors.white

def _header_style():
    return ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=13, alignment=TA_CENTER, textColor=DARK)

def _sub_style():
    return ParagraphStyle("s", fontName="Helvetica", fontSize=10, alignment=TA_CENTER, textColor=GRAY)

def _info_style():
    return ParagraphStyle("i", fontName="Helvetica", fontSize=10, alignment=TA_LEFT, textColor=DARK)

def _build_header(elements, title):
    styles = getSampleStyleSheet()
    elements.append(Paragraph(KAMPUS, _header_style()))
    elements.append(Paragraph(PRODI,  _sub_style()))
    elements.append(HRFlowable(width="100%", thickness=2, color=PRIMARY))
    elements.append(Spacer(1, 0.3*cm))
    elements.append(Paragraph(title, ParagraphStyle("t", fontName="Helvetica-Bold", fontSize=12, alignment=TA_CENTER, textColor=PRIMARY)))
    elements.append(Spacer(1, 0.2*cm))

def _build_footer_info(elements, operator=OPERATOR):
    now = datetime.now().strftime("%d %B %Y, %H:%M")
    elements.append(Spacer(1, 0.5*cm))
    elements.append(HRFlowable(width="100%", thickness=1, color=GRAY))
    elements.append(Spacer(1, 0.2*cm))
    data = [[
        Paragraph(f"Dicetak oleh: {operator}", _info_style()),
        Paragraph(f"Tanggal: {now}", ParagraphStyle("r", fontName="Helvetica", fontSize=10, alignment=TA_RIGHT, textColor=GRAY))
    ]]
    t = Table(data, colWidths=[10*cm, 8*cm])
    t.setStyle(TableStyle([("VALIGN", (0,0), (-1,-1), "MIDDLE")]))
    elements.append(t)

def cetak_krs(nim, nama, prodi, rows, save_dir="laporan"):
    os.makedirs(save_dir, exist_ok=True)
    filename = os.path.join(save_dir, f"KRS_{nim}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf")
    doc = SimpleDocTemplate(filename, pagesize=A4,
                            leftMargin=2*cm, rightMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)
    elements = []
    _build_header(elements, "KARTU RENCANA STUDI (KRS)")
    elements.append(Spacer(1, 0.3*cm))

    # Info mahasiswa
    info = [
        ["NIM", ":", nim, "Program Studi", ":", prodi],
        ["Nama", ":", nama, "", "", ""],
    ]
    t_info = Table(info, colWidths=[2*cm, 0.3*cm, 6*cm, 3*cm, 0.3*cm, 5*cm])
    t_info.setStyle(TableStyle([
        ("FONTNAME", (0,0), (-1,-1), "Helvetica"),
        ("FONTSIZE", (0,0), (-1,-1), 10),
        ("FONTNAME", (0,0), (0,-1), "Helvetica-Bold"),
        ("FONTNAME", (3,0), (3,-1), "Helvetica-Bold"),
    ]))
    elements.append(t_info)
    elements.append(Spacer(1, 0.4*cm))

    # Tabel data
    header = [["No", "Kode MK", "Nama Mata Kuliah", "SKS", "Kelas", "Ruang", "Hari", "Jam", "Dosen"]]
    total_sks = 0
    table_data = header
    for i, r in enumerate(rows, 1):
        # r: id_krs, nim, nama_mhs, prodi, kode_mk, nama_mk, sks, kelas, ruang, hari, jam, nuptk, nama_dosen
        table_data.append([i, r[4], r[5], r[6], r[7], r[8], r[9], str(r[10])[:5], r[12]])
        total_sks += r[6]
    table_data.append(["", "", Paragraph("<b>Total SKS</b>", ParagraphStyle("b", fontName="Helvetica-Bold", fontSize=10)), total_sks, "", "", "", "", ""])

    col_w = [0.8*cm, 2*cm, 5.5*cm, 1*cm, 1.2*cm, 1.2*cm, 1.5*cm, 1.3*cm, 3.5*cm]
    t = Table(table_data, colWidths=col_w, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), PRIMARY),
        ("TEXTCOLOR",  (0,0), (-1,0), WHITE),
        ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",   (0,0), (-1,-1), 9),
        ("ALIGN",      (0,0), (-1,-1), "CENTER"),
        ("ALIGN",      (2,1), (2,-1), "LEFT"),
        ("ALIGN",      (8,1), (8,-1), "LEFT"),
        ("ROWBACKGROUNDS", (0,1), (-1,-2), [WHITE, LIGHT_BG]),
        ("GRID",       (0,0), (-1,-1), 0.5, GRAY),
        ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
        ("BACKGROUND", (0,-1), (-1,-1), colors.HexColor("#DBEAFE")),
        ("FONTNAME",   (0,-1), (-1,-1), "Helvetica-Bold"),
    ]))
    elements.append(t)
    _build_footer_info(elements)
    doc.build(elements)
    return filename


def cetak_khs(nim, nama, prodi, rows, total_sks, total_mutu, ip_semester, save_dir="laporan"):
    os.makedirs(save_dir, exist_ok=True)
    filename = os.path.join(save_dir, f"KHS_{nim}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf")
    doc = SimpleDocTemplate(filename, pagesize=A4,
                            leftMargin=2*cm, rightMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)
    elements = []
    _build_header(elements, "KARTU HASIL STUDI (KHS)")
    elements.append(Spacer(1, 0.3*cm))

    info = [
        ["NIM", ":", nim, "Program Studi", ":", prodi],
        ["Nama", ":", nama, "", "", ""],
    ]
    t_info = Table(info, colWidths=[2*cm, 0.3*cm, 6*cm, 3*cm, 0.3*cm, 5*cm])
    t_info.setStyle(TableStyle([
        ("FONTNAME", (0,0), (-1,-1), "Helvetica"),
        ("FONTSIZE", (0,0), (-1,-1), 10),
        ("FONTNAME", (0,0), (0,-1), "Helvetica-Bold"),
        ("FONTNAME", (3,0), (3,-1), "Helvetica-Bold"),
    ]))
    elements.append(t_info)
    elements.append(Spacer(1, 0.4*cm))

    header = [["No", "Kode MK", "Nama Mata Kuliah", "SKS", "Nilai Angka", "Nilai Huruf", "Bobot", "Mutu"]]
    table_data = header
    for i, r in enumerate(rows, 1):
        # r: id_nilai, id_krs, nim, nama_mhs, prodi, kode_mk, nama_mk, sks, nilai_angka, nilai_huruf, bobot, mutu
        table_data.append([i, r[5], r[6], r[7], f"{r[8]:.2f}", r[9], f"{r[10]:.2f}", f"{r[11]:.2f}"])
    table_data.append(["", "", Paragraph("<b>Total</b>", ParagraphStyle("b", fontName="Helvetica-Bold", fontSize=9)),
                       total_sks, "", "", "", f"{total_mutu:.2f}"])
    table_data.append(["", "", Paragraph("<b>IP Semester</b>", ParagraphStyle("b", fontName="Helvetica-Bold", fontSize=9, textColor=PRIMARY)),
                       "", "", "", "", Paragraph(f"<b>{ip_semester:.2f}</b>", ParagraphStyle("b2", fontName="Helvetica-Bold", fontSize=11, textColor=PRIMARY, alignment=TA_CENTER))])

    col_w = [0.8*cm, 2*cm, 5.5*cm, 1.2*cm, 2*cm, 2*cm, 1.5*cm, 2*cm]
    t = Table(table_data, colWidths=col_w, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), PRIMARY),
        ("TEXTCOLOR",  (0,0), (-1,0), WHITE),
        ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",   (0,0), (-1,-1), 9),
        ("ALIGN",      (0,0), (-1,-1), "CENTER"),
        ("ALIGN",      (2,1), (2,-1), "LEFT"),
        ("ROWBACKGROUNDS", (0,1), (-1,-3), [WHITE, LIGHT_BG]),
        ("GRID",       (0,0), (-1,-1), 0.5, GRAY),
        ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
        ("BACKGROUND", (0,-2), (-1,-1), colors.HexColor("#DBEAFE")),
        ("FONTNAME",   (0,-2), (-1,-1), "Helvetica-Bold"),
    ]))
    elements.append(t)
    _build_footer_info(elements)
    doc.build(elements)
    return filename
