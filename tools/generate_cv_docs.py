from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"


EN = {
    "filename": "Longlong_Li_CV_EN.docx",
    "pdf_filename": "Longlong_Li_CV_EN.pdf",
    "name": "Longlong Li",
    "title": "Curriculum Vitae",
    "position": "PhD Student, Department of Mechanical Engineering, Chonnam National University",
    "location": "Gwangju, South Korea",
    "email": "lilonglong2000@jnu.ac.kr",
    "homepage": "longlongli.com",
    "research_statement": (
        "Research focus: MEMS, micro/nano sensors, and 3D bioelectronic sensing "
        "platforms for multimodal electromechanical analysis of engineered cardiac tissue."
    ),
    "sections": [
        (
            "Education",
            [
                "2022-Present | PhD in Mechanical Engineering, Chonnam National University, Gwangju, South Korea",
                "2018-2022 | B.S. in Mechanical Engineering, Wenzhou University, Wenzhou, China",
            ],
        ),
        (
            "Research Experience",
            [
                "Developing MEMS-enabled and flexible multimodal sensors for electromechanical monitoring of engineered cardiac tissue.",
                "Building 3D bioelectronic platforms for tissue maturation, cardiotoxicity screening, and in vitro cardiac disease modeling.",
                "Integrating strain, electrical, and structural readouts for real-time characterization of cardiac electromechanical behavior.",
            ],
        ),
        (
            "Research Interests",
            [
                "BioMEMS sensing platforms",
                "Engineered cardiac tissue monitoring",
                "Multimodal electromechanical recording",
                "Drug cardiotoxicity evaluation",
            ],
        ),
        (
            "Projects",
            [
                "2026.03-Present | Biomimetic Cardiac Hypoxia Model and Electromechanical Evaluation Platform, MNTL",
                "2024.03-2026.03 | High-Throughput Drug Toxicity Screening Platform Based on 3D Cardiac Tissue, MNTL",
                "2022.09-2024.03 | Regulatory Mechanisms of Graphene Conductive Microenvironments in Cardiomyocyte Electrophysiological Communication and Maturation, MNTL",
                "2022.01-2022.08 | Smart Trash Bin Development, Cixi Zhuoshang Electric Appliance Co., Ltd.",
                "2021.01-2021.12 | Desktop Customized Food 3D Printer, Wenzhou University",
                "2020.01-2020.12 | Toy Storage Robot Based on Visual Recognition and Navigation, Wenzhou University",
            ],
        ),
        (
            "Publications",
            [
                "2024 | Graphene SU-8 platform for enhanced cardiomyocyte maturation and intercellular communication in cardiac drug screening. ACS Nano 18(49): 33293-33309.",
                "2025 | Harnessing native blueprints for designing bioinks to bioprint functional cardiac tissue. iScience 28(3).",
                "2025 | Development of multifunctional PAA-alginate-carboxymethyl cellulose hydrogel-loaded fiber-reinforced biomimetic scaffolds for controlled release of curcumin. International Journal of Biological Macromolecules 301: 140449.",
                "2025 | Dual-sensitized hollow SnO2 nanospheres with rGO and Pd for highly sensitive detection of acetone in exhaled breath. Applied Surface Science 696: 162959.",
                "2025 | Hydrogel-Integrated Biomimetic Hydroxyapatite Scaffolds with Tunable Porosity for Enhanced Curcumin Delivery. Journal of Drug Delivery Science and Technology, 107572.",
                "2025 | Enhancing cardiomyocyte maturation through PEDOT:PSS-coated surfaces and mechanical stimulation with strain sensors. Journal of Micromechanics and Microengineering 35(4): 045002.",
                "2025 | InGaN-GaN-MQW-ZnO based e-nose sensors for nitrogen dioxide detection using advanced machine learning approaches. Sensors and Actuators B: Chemical, 138650.",
                "2026 | Air-Breakdown Triboelectric Nanogenerator Inspired by Transistor Architecture for Low-Force Human-Machine Interfaces. Nano-Micro Letters 18(1): 251.",
                "2026 | Tilted-angle acoustofluidic separation of live and dead neonatal rat ventricular myocytes using hypotonic cell swelling. Sensors and Actuators B: Chemical.",
            ],
        ),
        (
            "Conferences",
            [
                "2023 | The hybrid cantilever of conductive graphene and su-8 for improving the maturity and electrical coupling of cardiomyocytes. MicroTAS 2023, Katowice, Poland.",
                "2024 | Enhancing Cardiomyocyte Maturation via Mechanical Stimulation of 3D Printed Cardiac Tissue Using a Origami-based 3D Sensor and Magnetic Fields. IEEE NANOMED 2024, Hawaii, USA.",
                "2024 | Polymer Cantilever Integrated with a Full-Bridge Sensor for Continuous Wireless Measurement of Cardiomyocyte Contractility. MicroTAS 2024, Montreal, Canada.",
                "2024 | MONITORING OF DRUG-IMFACTED CARDIOMYOCYTES CONTRACTILITY USING PI MICROCANTILEVER STRUCTURES WITH NANO-SILICON STRAIN SENSOR. MicroTAS 2024, Montreal, Canada.",
                "2025 | A Dual-Detection Approach for Cardiotoxicity Screening: Utilizing Nano Silicon Strain Sensor and Mea to Monitor Contractility and Field Potential in Cardiomyocytes. IEEE MEMS 2025, Kaohsiung, Taiwan.",
                "2025 | Origami-Inspired 3D Sensor Platform for Real-Time Electromechanical Coupling Analysis in Engineered Heart Tissues. IEEE SENSORS 2025, Vancouver, Canada.",
                "2025 | Integrated Bioelectronic Platform Utilizing PEDOT:PSS Strain Sensors for Real-Time Mechanostimulation and Sensing. IEEE SENSORS 2025, Vancouver, Canada.",
                "2025 | Development of a Multi-Channel Wireless Monitoring Platform for Long-Term Cardiomyocyte Contraction Assessment Using a Polymer Cantilever with integrated Sensor. MicroTAS 2025, Adelaide, Australia.",
                "2025 | Enhancement of cardiomyocyte microenvironment and functional assessment using through-hole structures with integrated polymer cantilevers. MicroTAS 2025, Adelaide, Australia.",
                "2026 | Multimodal Microelectrode-Microcantilever Array for Electromechanical Analysis of Cardiomyocyte Tissue in Drug Testing. IEEE MEMS 2026, Salzburg, Austria.",
            ],
        ),
        (
            "Patents",
            [
                "Intelligent dispatch and retrieval management device for UAV swarms, CN216269980U.",
                "Automatic potato harvester, CN216415123U.",
                "Potato digging device, CN216313996U.",
                "Automatic rolling and pressing device for footpoint and acupoint stimulation, CN214278088U.",
                "Kitchen waste collection cart, CN113369827A / CN113369827B.",
                "Ditching and ridging integrated machine, CN112023495A / CN112023495B.",
                "Clothes-folding machine based on longitudinal folding, CN113186699A / CN113186699B.",
            ],
        ),
        (
            "Awards",
            [
                "2025 | BK21 Fellowship Scholarship",
                "2025 | RLRC Outstanding Graduate Student",
                "2021 | China National Scholarship",
                "2019 | Zhejiang Provincial Government Scholarship",
            ],
        ),
        (
            "Technical Skills",
            [
                "Micro/Nanofabrication and Device Development: Proficient in MEMS and flexible sensor micro/nanofabrication processes, device development, and sensor performance characterization.",
                "Tissue Engineering and Cell Culture: Experienced in NRVM and hiPSC-CMs cardiomyocyte culture, 3D engineered heart tissue (EHT) construction, and bioink formulation based on collagen and dECM systems.",
                "Test Systems and Hardware Integration: Capable of independently developing experimental prototypes and building synchronized measurement systems integrating closed-loop control, strain sensors, and microelectrode array (MEA) detection.",
                "Multimodal Signal Processing: Skilled in Python and MATLAB for processing cardiac electromechanical multimodal signals and extracting key electrophysiological and mechanobiological features.",
            ],
        ),
    ],
}


ZH = {
    "filename": "Longlong_Li_CV_ZH.docx",
    "pdf_filename": "Longlong_Li_CV_ZH.pdf",
    "name": "李龙龙",
    "title": "个人简历",
    "position": "全南国立大学 机械工程系 博士研究生",
    "location": "韩国 光州",
    "email": "lilonglong2000@jnu.ac.kr",
    "homepage": "longlongli.com",
    "research_statement": "研究方向：MEMS、微纳传感器、3D 生物电子传感平台，以及工程化心脏组织的多模态机电分析。",
    "sections": [
        (
            "教育经历",
            [
                "2022-至今 | 全南国立大学，机械工程博士，韩国 光州",
                "2018-2022 | 温州大学，机械工程本科，中国 温州",
            ],
        ),
        (
            "科研经历",
            [
                "开展面向工程化心肌组织的 MEMS 与柔性多模态传感器研究。",
                "构建 3D 生物电子平台，用于组织成熟化、药物心脏毒性筛选与体外心脏疾病模型研究。",
                "整合应变、电学与结构读出，实现对心脏组织电机械行为的实时表征。",
            ],
        ),
        (
            "研究兴趣",
            [
                "BioMEMS 传感平台",
                "工程化心脏组织监测",
                "多模态机电记录",
                "药物心脏毒性评估",
            ],
        ),
        (
            "项目经历",
            [
                "2026.03-至今 | 仿生心脏缺氧模型与机电评估平台，MNTL",
                "2024.03-2026.03 | 基于3D心脏组织的高通量药物毒理筛选平台，MNTL",
                "2022.09-2024.03 | 石墨烯导电微环境对心肌细胞电生理通讯与成熟的调控机制，MNTL",
                "2022.01-2022.08 | 智能垃圾桶的开发，慈溪卓尚电器有限公司",
                "2021.01-2021.12 | 桌面级定制食品3D打印机，温州大学",
                "2020.01-2020.12 | 基于视觉识别与导航的玩具收纳机器人，温州大学",
            ],
        ),
        (
            "论文发表",
            [
                "2024 | Graphene SU-8 platform for enhanced cardiomyocyte maturation and intercellular communication in cardiac drug screening. ACS Nano 18(49): 33293-33309.",
                "2025 | Harnessing native blueprints for designing bioinks to bioprint functional cardiac tissue. iScience 28(3).",
                "2025 | Development of multifunctional PAA-alginate-carboxymethyl cellulose hydrogel-loaded fiber-reinforced biomimetic scaffolds for controlled release of curcumin. International Journal of Biological Macromolecules 301: 140449.",
                "2025 | Dual-sensitized hollow SnO2 nanospheres with rGO and Pd for highly sensitive detection of acetone in exhaled breath. Applied Surface Science 696: 162959.",
                "2025 | Hydrogel-Integrated Biomimetic Hydroxyapatite Scaffolds with Tunable Porosity for Enhanced Curcumin Delivery. Journal of Drug Delivery Science and Technology, 107572.",
                "2025 | Enhancing cardiomyocyte maturation through PEDOT:PSS-coated surfaces and mechanical stimulation with strain sensors. Journal of Micromechanics and Microengineering 35(4): 045002.",
                "2025 | InGaN-GaN-MQW-ZnO based e-nose sensors for nitrogen dioxide detection using advanced machine learning approaches. Sensors and Actuators B: Chemical, 138650.",
                "2026 | Air-Breakdown Triboelectric Nanogenerator Inspired by Transistor Architecture for Low-Force Human-Machine Interfaces. Nano-Micro Letters 18(1): 251.",
                "2026 | Tilted-angle acoustofluidic separation of live and dead neonatal rat ventricular myocytes using hypotonic cell swelling. Sensors and Actuators B: Chemical.",
            ],
        ),
        (
            "学术会议",
            [
                "2023 | The hybrid cantilever of conductive graphene and su-8 for improving the maturity and electrical coupling of cardiomyocytes. MicroTAS 2023, Katowice, Poland.",
                "2024 | Enhancing Cardiomyocyte Maturation via Mechanical Stimulation of 3D Printed Cardiac Tissue Using a Origami-based 3D Sensor and Magnetic Fields. IEEE NANOMED 2024, Hawaii, USA.",
                "2024 | Polymer Cantilever Integrated with a Full-Bridge Sensor for Continuous Wireless Measurement of Cardiomyocyte Contractility. MicroTAS 2024, Montreal, Canada.",
                "2024 | MONITORING OF DRUG-IMFACTED CARDIOMYOCYTES CONTRACTILITY USING PI MICROCANTILEVER STRUCTURES WITH NANO-SILICON STRAIN SENSOR. MicroTAS 2024, Montreal, Canada.",
                "2025 | A Dual-Detection Approach for Cardiotoxicity Screening: Utilizing Nano Silicon Strain Sensor and Mea to Monitor Contractility and Field Potential in Cardiomyocytes. IEEE MEMS 2025, Kaohsiung, Taiwan.",
                "2025 | Origami-Inspired 3D Sensor Platform for Real-Time Electromechanical Coupling Analysis in Engineered Heart Tissues. IEEE SENSORS 2025, Vancouver, Canada.",
                "2025 | Integrated Bioelectronic Platform Utilizing PEDOT:PSS Strain Sensors for Real-Time Mechanostimulation and Sensing. IEEE SENSORS 2025, Vancouver, Canada.",
                "2025 | Development of a Multi-Channel Wireless Monitoring Platform for Long-Term Cardiomyocyte Contraction Assessment Using a Polymer Cantilever with integrated Sensor. MicroTAS 2025, Adelaide, Australia.",
                "2025 | Enhancement of cardiomyocyte microenvironment and functional assessment using through-hole structures with integrated polymer cantilevers. MicroTAS 2025, Adelaide, Australia.",
                "2026 | Multimodal Microelectrode-Microcantilever Array for Electromechanical Analysis of Cardiomyocyte Tissue in Drug Testing. IEEE MEMS 2026, Salzburg, Austria.",
            ],
        ),
        (
            "专利",
            [
                "一种无人机集群的智能收发管理装置，CN216269980U。",
                "一种自动马铃薯收获机，CN216415123U。",
                "马铃薯挖掘装置，CN216313996U。",
                "一种脚点穴位自动滚压刺激装置，CN214278088U。",
                "厨余垃圾收集车，CN113369827A / CN113369827B。",
                "开沟起垄一体机，CN112023495A / CN112023495B。",
                "一种基于纵向折叠的衣服折叠机，CN113186699A / CN113186699B。",
            ],
        ),
        (
            "奖励荣誉",
            [
                "2025 | BK21 Fellowship Scholarship",
                "2025 | RLRC Outstanding Graduate Student",
                "2021 | 中国国家奖学金",
                "2019 | 浙江省政府奖学金",
            ],
        ),
        (
            "技术技能",
            [
                "微纳制造与器件开发：熟练掌握 MEMS 与柔性传感器件的微纳加工工艺及传感器性能表征。",
                "组织工程与细胞培养：熟练进行 NRVM / hiPSC-CMs 心肌细胞培养，精通 3D 工程心脏组织（EHT）的构建与生物墨水（胶原 / dECM）体系调配。",
                "测试系统与硬件搭建：具备实验原型机开发能力，能独立搭建集成闭环控制、应变传感器和微电极阵列（MEA）检测的同步测量系统。",
                "多模态信号处理：熟练使用 Python / MATLAB 处理并分析心脏机电多模态信号，提取关键机电生理特征。",
            ],
        ),
    ],
}


def set_page(doc: Document) -> None:
    section = doc.sections[0]
    section.page_width = Inches(8.5)
    section.page_height = Inches(11)
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)
    section.header_distance = Inches(0.492)
    section.footer_distance = Inches(0.492)


def set_paragraph_border(paragraph) -> None:
    p_pr = paragraph._p.get_or_add_pPr()
    p_bdr = p_pr.find(qn("w:pBdr"))
    if p_bdr is None:
        p_bdr = OxmlElement("w:pBdr")
        p_pr.append(p_bdr)
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "6")
    bottom.set(qn("w:space"), "4")
    bottom.set(qn("w:color"), "B6C4D5")
    p_bdr.append(bottom)


def style_document(doc: Document, east_asia_font: str) -> None:
    normal = doc.styles["Normal"]
    normal.font.name = "Calibri"
    normal.font.size = Pt(10.5)
    normal._element.rPr.rFonts.set(qn("w:eastAsia"), east_asia_font)
    pf = normal.paragraph_format
    pf.space_after = Pt(4)
    pf.line_spacing = 1.1

    for style_name, size, color in (
        ("Title", 24, RGBColor(18, 54, 95)),
        ("Heading 1", 13, RGBColor(29, 78, 137)),
        ("Heading 2", 11, RGBColor(29, 78, 137)),
    ):
        style = doc.styles[style_name]
        style.font.name = "Calibri"
        style.font.size = Pt(size)
        style.font.bold = True
        style.font.color.rgb = color
        style._element.rPr.rFonts.set(qn("w:eastAsia"), east_asia_font)
        style.paragraph_format.space_before = Pt(10 if style_name != "Title" else 0)
        style.paragraph_format.space_after = Pt(4 if style_name != "Title" else 2)


def add_header_block(doc: Document, data: dict, east_asia_font: str) -> None:
    p = doc.add_paragraph(style="Title")
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(data["name"])
    run.font.name = "Calibri"
    run._element.rPr.rFonts.set(qn("w:eastAsia"), east_asia_font)

    p2 = doc.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r2 = p2.add_run(f"{data['title']} | {data['position']}")
    r2.bold = True
    r2.font.size = Pt(11)
    r2.font.name = "Calibri"
    r2._element.rPr.rFonts.set(qn("w:eastAsia"), east_asia_font)

    p3 = doc.add_paragraph()
    p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p3.paragraph_format.space_after = Pt(8)
    for idx, text in enumerate([data["location"], data["email"], f"Homepage: {data['homepage']}"]):
        run = p3.add_run(text)
        run.font.size = Pt(9.5)
        run.font.name = "Calibri"
        run._element.rPr.rFonts.set(qn("w:eastAsia"), east_asia_font)
        if idx < 2:
            sep = p3.add_run("  |  ")
            sep.font.size = Pt(9.5)
            sep.font.name = "Calibri"
            sep._element.rPr.rFonts.set(qn("w:eastAsia"), east_asia_font)

    note = doc.add_paragraph()
    note.paragraph_format.space_after = Pt(10)
    note.paragraph_format.left_indent = Inches(0.05)
    note.paragraph_format.right_indent = Inches(0.05)
    set_paragraph_border(note)
    run = note.add_run(data["research_statement"])
    run.italic = True
    run.font.size = Pt(10)
    run.font.name = "Calibri"
    run._element.rPr.rFonts.set(qn("w:eastAsia"), east_asia_font)


def add_section(doc: Document, heading: str, items: list[str], east_asia_font: str) -> None:
    h = doc.add_paragraph(style="Heading 1")
    run = h.add_run(heading)
    run.font.name = "Calibri"
    run._element.rPr.rFonts.set(qn("w:eastAsia"), east_asia_font)

    for item in items:
        p = doc.add_paragraph(style="Normal")
        p.paragraph_format.left_indent = Inches(0.22)
        p.paragraph_format.first_line_indent = Inches(-0.18)
        p.paragraph_format.space_after = Pt(2)
        bullet = p.add_run("- ")
        bullet.bold = True
        bullet.font.name = "Calibri"
        bullet._element.rPr.rFonts.set(qn("w:eastAsia"), east_asia_font)
        body = p.add_run(item)
        body.font.name = "Calibri"
        body._element.rPr.rFonts.set(qn("w:eastAsia"), east_asia_font)


def add_footer(doc: Document, label: str) -> None:
    section = doc.sections[0]
    footer = section.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = footer.add_run(label)
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor(86, 99, 117)


def build_doc(data: dict, east_asia_font: str, footer_label: str) -> Path:
    doc = Document()
    set_page(doc)
    style_document(doc, east_asia_font)
    add_header_block(doc, data, east_asia_font)
    for heading, items in data["sections"]:
        add_section(doc, heading, items, east_asia_font)
    add_footer(doc, footer_label)
    out = ASSETS / data["filename"]
    doc.save(out)
    return out


def build_pdf(data: dict, font_name: str, title_font: str) -> Path:
    out = ASSETS / data["pdf_filename"]
    doc = SimpleDocTemplate(
        str(out),
        pagesize=letter,
        leftMargin=inch,
        rightMargin=inch,
        topMargin=0.9 * inch,
        bottomMargin=0.75 * inch,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "CVTitle",
        parent=styles["Title"],
        fontName=title_font,
        fontSize=20,
        leading=24,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#12365F"),
        spaceAfter=6,
    )
    meta_style = ParagraphStyle(
        "CVMeta",
        parent=styles["BodyText"],
        fontName=font_name,
        fontSize=9.2,
        leading=12,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#334155"),
        spaceAfter=3,
    )
    note_style = ParagraphStyle(
        "CVNote",
        parent=styles["BodyText"],
        fontName=font_name,
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor("#243143"),
        backColor=colors.HexColor("#F4F7FB"),
        borderColor=colors.HexColor("#B6C4D5"),
        borderWidth=0.6,
        borderPadding=6,
        spaceAfter=10,
    )
    heading_style = ParagraphStyle(
        "CVHeading",
        parent=styles["Heading1"],
        fontName=title_font,
        fontSize=12,
        leading=15,
        textColor=colors.HexColor("#1D4E89"),
        spaceBefore=8,
        spaceAfter=4,
    )
    bullet_style = ParagraphStyle(
        "CVBullet",
        parent=styles["BodyText"],
        fontName=font_name,
        fontSize=9.4,
        leading=12,
        leftIndent=12,
        firstLineIndent=-9,
        spaceAfter=2,
        textColor=colors.black,
    )

    story = [
        Paragraph(data["name"], title_style),
        Paragraph(f"{data['title']} | {data['position']}", meta_style),
        Paragraph(f"{data['location']} | {data['email']} | Homepage: {data['homepage']}", meta_style),
        Spacer(1, 4),
        Paragraph(data["research_statement"], note_style),
    ]

    for heading, items in data["sections"]:
        story.append(Paragraph(heading, heading_style))
        for item in items:
            safe = item.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            story.append(Paragraph(f"- {safe}", bullet_style))

    doc.build(story)
    return out


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    build_doc(EN, "Calibri", "Longlong Li CV")
    build_doc(ZH, "SimSun", "李龙龙 简历")
    pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))
    build_pdf(EN, "Helvetica", "Helvetica-Bold")
    build_pdf(ZH, "STSong-Light", "STSong-Light")


if __name__ == "__main__":
    main()
