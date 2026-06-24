from __future__ import annotations

from pathlib import Path
from typing import Any

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
CV_ASSETS = ASSETS / "CV"


FULL_PUBLICATIONS_EN = [
    "Graphene SU-8 platform for enhanced cardiomyocyte maturation and intercellular communication in cardiac drug screening. ACS Nano 18(49): 33293-33309, 2024.",
    "Harnessing native blueprints for designing bioinks to bioprint functional cardiac tissue. iScience 28(3), 2025.",
    "Development of multifunctional PAA-alginate-carboxymethyl cellulose hydrogel-loaded fiber-reinforced biomimetic scaffolds for controlled release of curcumin. International Journal of Biological Macromolecules 301: 140449, 2025.",
    "Dual-sensitized hollow SnO2 nanospheres with rGO and Pd for highly sensitive detection of acetone in exhaled breath. Applied Surface Science 696: 162959, 2025.",
    "Hydrogel-Integrated Biomimetic Hydroxyapatite Scaffolds with Tunable Porosity for Enhanced Curcumin Delivery. Journal of Drug Delivery Science and Technology, 107572, 2025.",
    "Enhancing cardiomyocyte maturation through PEDOT:PSS-coated surfaces and mechanical stimulation with strain sensors. Journal of Micromechanics and Microengineering 35(4): 045002, 2025.",
    "InGaN-GaN-MQW-ZnO based e-nose sensors for nitrogen dioxide detection using advanced machine learning approaches. Sensors and Actuators B: Chemical, 138650, 2025.",
    "Air-Breakdown Triboelectric Nanogenerator Inspired by Transistor Architecture for Low-Force Human-Machine Interfaces. Nano-Micro Letters 18(1): 251, 2026.",
    "Tilted-angle acoustofluidic separation of live and dead neonatal rat ventricular myocytes using hypotonic cell swelling. Sensors and Actuators B: Chemical, 2026.",
]

FULL_PUBLICATIONS_ZH = [
    "Graphene SU-8 platform for enhanced cardiomyocyte maturation and intercellular communication in cardiac drug screening. ACS Nano 18(49): 33293-33309, 2024。",
    "Harnessing native blueprints for designing bioinks to bioprint functional cardiac tissue. iScience 28(3), 2025。",
    "Development of multifunctional PAA-alginate-carboxymethyl cellulose hydrogel-loaded fiber-reinforced biomimetic scaffolds for controlled release of curcumin. International Journal of Biological Macromolecules 301: 140449, 2025。",
    "Dual-sensitized hollow SnO2 nanospheres with rGO and Pd for highly sensitive detection of acetone in exhaled breath. Applied Surface Science 696: 162959, 2025。",
    "Hydrogel-Integrated Biomimetic Hydroxyapatite Scaffolds with Tunable Porosity for Enhanced Curcumin Delivery. Journal of Drug Delivery Science and Technology, 107572, 2025。",
    "Enhancing cardiomyocyte maturation through PEDOT:PSS-coated surfaces and mechanical stimulation with strain sensors. Journal of Micromechanics and Microengineering 35(4): 045002, 2025。",
    "InGaN-GaN-MQW-ZnO based e-nose sensors for nitrogen dioxide detection using advanced machine learning approaches. Sensors and Actuators B: Chemical, 138650, 2025。",
    "Air-Breakdown Triboelectric Nanogenerator Inspired by Transistor Architecture for Low-Force Human-Machine Interfaces. Nano-Micro Letters 18(1): 251, 2026。",
    "Tilted-angle acoustofluidic separation of live and dead neonatal rat ventricular myocytes using hypotonic cell swelling. Sensors and Actuators B: Chemical, 2026。",
]

FULL_CONFERENCES_EN = [
    "The hybrid cantilever of conductive graphene and SU-8 for improving the maturity and electrical coupling of cardiomyocytes. MicroTAS 2023, Katowice, Poland.",
    "Enhancing Cardiomyocyte Maturation via Mechanical Stimulation of 3D Printed Cardiac Tissue Using a Origami-based 3D Sensor and Magnetic Fields. IEEE NANOMED 2024, Hawaii, USA.",
    "Polymer Cantilever Integrated with a Full-Bridge Sensor for Continuous Wireless Measurement of Cardiomyocyte Contractility. MicroTAS 2024, Montreal, Canada.",
    "Monitoring of drug-impacted cardiomyocytes contractility using PI microcantilever structures with nano-silicon strain sensor. MicroTAS 2024, Montreal, Canada.",
    "A Dual-Detection Approach for Cardiotoxicity Screening: Utilizing Nano Silicon Strain Sensor and MEA to Monitor Contractility and Field Potential in Cardiomyocytes. IEEE MEMS 2025, Kaohsiung, Taiwan.",
    "Origami-Inspired 3D Sensor Platform for Real-Time Electromechanical Coupling Analysis in Engineered Heart Tissues. IEEE SENSORS 2025, Vancouver, Canada.",
    "Integrated Bioelectronic Platform Utilizing PEDOT:PSS Strain Sensors for Real-Time Mechanostimulation and Sensing. IEEE SENSORS 2025, Vancouver, Canada.",
    "Development of a Multi-Channel Wireless Monitoring Platform for Long-Term Cardiomyocyte Contraction Assessment Using a Polymer Cantilever with Integrated Sensor. MicroTAS 2025, Adelaide, Australia.",
    "Enhancement of cardiomyocyte microenvironment and functional assessment using through-hole structures with integrated polymer cantilevers. MicroTAS 2025, Adelaide, Australia.",
    "Multimodal Microelectrode-Microcantilever Array for Electromechanical Analysis of Cardiomyocyte Tissue in Drug Testing. IEEE MEMS 2026, Salzburg, Austria.",
]

FULL_CONFERENCES_ZH = [
    "The hybrid cantilever of conductive graphene and SU-8 for improving the maturity and electrical coupling of cardiomyocytes. MicroTAS 2023, Katowice, Poland。",
    "Enhancing Cardiomyocyte Maturation via Mechanical Stimulation of 3D Printed Cardiac Tissue Using a Origami-based 3D Sensor and Magnetic Fields. IEEE NANOMED 2024, Hawaii, USA。",
    "Polymer Cantilever Integrated with a Full-Bridge Sensor for Continuous Wireless Measurement of Cardiomyocyte Contractility. MicroTAS 2024, Montreal, Canada。",
    "Monitoring of drug-impacted cardiomyocytes contractility using PI microcantilever structures with nano-silicon strain sensor. MicroTAS 2024, Montreal, Canada。",
    "A Dual-Detection Approach for Cardiotoxicity Screening: Utilizing Nano Silicon Strain Sensor and MEA to Monitor Contractility and Field Potential in Cardiomyocytes. IEEE MEMS 2025, Kaohsiung, Taiwan。",
    "Origami-Inspired 3D Sensor Platform for Real-Time Electromechanical Coupling Analysis in Engineered Heart Tissues. IEEE SENSORS 2025, Vancouver, Canada。",
    "Integrated Bioelectronic Platform Utilizing PEDOT:PSS Strain Sensors for Real-Time Mechanostimulation and Sensing. IEEE SENSORS 2025, Vancouver, Canada。",
    "Development of a Multi-Channel Wireless Monitoring Platform for Long-Term Cardiomyocyte Contraction Assessment Using a Polymer Cantilever with Integrated Sensor. MicroTAS 2025, Adelaide, Australia。",
    "Enhancement of cardiomyocyte microenvironment and functional assessment using through-hole structures with integrated polymer cantilevers. MicroTAS 2025, Adelaide, Australia。",
    "Multimodal Microelectrode-Microcantilever Array for Electromechanical Analysis of Cardiomyocyte Tissue in Drug Testing. IEEE MEMS 2026, Salzburg, Austria。",
]

FULL_PATENTS_EN = [
    "Automatic Potato Harvester. Invention Patent Application, CN113875385A / 202111383414.3, filed 2021-11-22, published 2022-01-04.",
    "Vertical-Folding-Based Clothes Folding Machine. Granted Invention Patent, CN113186699B / 202110624021.0, granted 2023-02-07.",
    "Household Intelligent Toy Storage Robot. Granted Invention Patent, CN112407980B / 202011170715.3, granted 2022-01-18.",
    "Zinc Alloy Dross-Skimming Robot and Working Method. Granted Invention Patent, CN111923063B / 202010801270.8, granted 2021-07-16.",
    "Intelligent Launch-and-Recovery Management Device for UAV Swarms. Utility Model Patent, CN216269980U / 202123168608.X, granted 2022-04-12.",
    "Traction Device for Potato Harvesters. Utility Model Patent, CN216232634U / 202122864096.4, granted 2022-04-08.",
    "Potato-Soil Separation Device for Potato Harvesters. Utility Model Patent, CN216253977U / 202122864125.7, granted 2022-04-12.",
    "Potato Digging Device. Utility Model Patent, CN216313996U / 202122864112.X, granted 2022-04-19.",
    "Automatic Potato Harvester. Utility Model Patent, CN216415123U / 202122859852.4, granted 2022-05-03.",
    "Trash Bin Based on Cam-Track Bag Closing and Heat Sealing. Utility Model Patent, CN216234167U / 202122813075.X, granted 2022-04-08.",
    "Telescopic Rotating Arm for Folding and Rolling in a Clothes Folding Machine. Utility Model Patent, CN215163984U / 202121243359.3, granted 2021-12-14.",
    "Cart-Bucket Turning Mechanism for Dumping Objects. Utility Model Patent, CN213443970U / 202022431595.X, granted 2021-06-15.",
    "Synchronous Multi-Scissor Lifting Device for Object Lifting. Utility Model Patent, CN213446006U / 202022431602.6, granted 2021-06-15.",
    "Timing-Belt Toy Collection Mechanism for a Household Intelligent Toy Storage Robot. Utility Model Patent, CN213536204U / 202022431641.6, granted 2021-06-25.",
    "Zinc Alloy Dross-Skimming Robot. Utility Model Patent, CN212763486U / 202021656863.1, granted 2021-03-23.",
]

FULL_PATENTS_ZH = [
    "自动马铃薯收获机。发明专利申请，CN113875385A / 202111383414.3，申请日 2021-11-22，公布日 2022-01-04。",
    "一种基于纵向折叠的叠衣机。授权发明专利，CN113186699B / 202110624021.0，授权公告日 2023-02-07。",
    "一种家用玩具智能收纳机器人。授权发明专利，CN112407980B / 202011170715.3，授权公告日 2022-01-18。",
    "一种锌合金扒渣机器人及其工作方法。授权发明专利，CN111923063B / 202010801270.8，授权公告日 2021-07-16。",
    "一种无人机集群的智能收发管理装置。实用新型专利，CN216269980U / 202123168608.X，授权公告日 2022-04-12。",
    "用于马铃薯收获机的牵引装置。实用新型专利，CN216232634U / 202122864096.4，授权公告日 2022-04-08。",
    "用于马铃薯收获机的薯土分离装置。实用新型专利，CN216253977U / 202122864125.7，授权公告日 2022-04-12。",
    "马铃薯挖掘装置。实用新型专利，CN216313996U / 202122864112.X，授权公告日 2022-04-19。",
    "一种自动马铃薯收获机。实用新型专利，CN216415123U / 202122859852.4，授权公告日 2022-05-03。",
    "基于凸轮轨道收口热封的垃圾桶。实用新型专利，CN216234167U / 202122813075.X，授权公告日 2022-04-08。",
    "一种用于叠衣机的对折打卷伸缩转臂。实用新型专利，CN215163984U / 202121243359.3，授权公告日 2021-12-14。",
    "一种用于倾倒物体的车兜翻转机构。实用新型专利，CN213443970U / 202022431595.X，授权公告日 2021-06-15。",
    "一种用于抬升物体的同步多剪叉式升降机装置。实用新型专利，CN213446006U / 202022431602.6，授权公告日 2021-06-15。",
    "一种家用玩具智能收纳机器人的同步带玩具收集机构。实用新型专利，CN213536204U / 202022431641.6，授权公告日 2021-06-25。",
    "锌合金扒渣机器人。实用新型专利，CN212763486U / 202021656863.1，授权公告日 2021-03-23。",
]


CVS: list[dict[str, Any]] = [
    {
        "filename_base": "Longlong_Li_Academic_CV_EN",
        "language": "en",
        "name": "Longlong Li",
        "title": "Academic CV",
        "position": "PhD Student | BioMEMS / Biosensors / Engineered Cardiac Tissue Monitoring",
        "affiliation": "Department of Mechanical Engineering, Chonnam National University",
        "location": "Gwangju, South Korea",
        "email": "lilonglong2000@jnu.ac.kr",
        "homepage": "longlongli.com",
        "header_note": "Comprehensive academic version for research collaboration, postdoctoral applications, and academic review.",
        "summary": [
            "PhD student specializing in BioMEMS, multimodal biosensors, engineered cardiac tissue monitoring, and drug cardiotoxicity evaluation.",
            "Experienced in MEMS device design, microfabrication, cell and tissue culture, sensing system integration, and multimodal biosignal analysis.",
            "Research focuses on integrating strain sensors, microelectrode arrays, and 3D bioelectronic platforms for synchronized and quantitative assessment of cardiac tissue function.",
        ],
        "sections": [
            {"title": "Education", "items": [
                "2022-Present | Ph.D. in Mechanical Engineering, Chonnam National University, Gwangju, South Korea",
                "2018-2022 | B.Eng. in Mechanical Engineering, Wenzhou University, Wenzhou, China",
            ]},
            {"title": "Research Experience", "items": [
                "Designed and developed BioMEMS-based multimodal sensing platforms for engineered cardiac tissues.",
                "Integrated strain sensors and microelectrode arrays to monitor mechanical contraction and electrical activity in cardiac tissue models.",
                "Established 3D engineered heart tissue culture and drug stimulation workflows for cardiotoxicity screening and disease modeling.",
                "Developed MATLAB / Python-based analysis workflows for extracting contraction amplitude, beating frequency, field potential features, and electromechanical coupling parameters.",
                "Built experimental measurement systems involving low-noise signal acquisition, microscopy, sensor calibration, and hardware integration.",
            ]},
            {"title": "Technical Skills", "items": [
                "Microfabrication: Photolithography, metal deposition, SU-8 / PI processing, MEMS sensor fabrication, device packaging, sensor characterization.",
                "Biosensing: Strain sensors, microelectrode arrays, electromechanical monitoring, low-noise signal acquisition, sensor calibration.",
                "Cell & Tissue Engineering: NRVM / hiPSC-CMs culture, engineered heart tissue construction, collagen / dECM bioinks, drug stimulation experiments, immunostaining.",
                "Data Analysis: MATLAB, Python, cardiac signal processing, feature extraction, visualization, statistical analysis.",
                "System Integration: DAQ systems, amplifier circuits, microscopy, automated measurement platforms, prototype development.",
            ]},
            {"title": "Projects", "items": [
                "2026.03-Present | Bioinspired Hypoxic Cardiac Model and Electromechanical Evaluation Platform, MNTL.",
                "2024.03-2026.03 | High-Throughput Drug Toxicity Screening Platform Based on 3D Cardiac Tissues, MNTL.",
                "2022.09-2024.03 | Graphene-Conductive Microenvironment for Cardiomyocyte Maturation and Electrophysiological Communication, MNTL.",
                "2022.01-2022.08 | Smart Trash Bin Development, Cixi Zhuoshang Electric Appliance Co., Ltd.",
                "2021.01-2021.12 | Desktop Customized Food 3D Printer, Wenzhou University.",
                "2020.01-2020.12 | Toy Storage Robot Based on Visual Recognition and Navigation, Wenzhou University.",
            ]},
            {"title": "Publications", "items": FULL_PUBLICATIONS_EN},
            {"title": "Conferences", "items": FULL_CONFERENCES_EN},
            {"title": "Patents", "items": FULL_PATENTS_EN},
            {"title": "Awards", "items": [
                "2025 | BK21 Fellowship Scholarship",
                "2025 | RLRC Outstanding Graduate Student",
                "2021 | China National Scholarship",
                "2019 | Zhejiang Provincial Government Scholarship",
            ]},
        ],
    },
    {
        "filename_base": "Longlong_Li_Academic_CV_ZH",
        "language": "zh",
        "name": "李龙龙",
        "title": "学术简历",
        "position": "博士研究生 | BioMEMS / 生物传感器 / 工程化心脏组织监测",
        "affiliation": "全南国立大学机械工程系",
        "location": "韩国 光州",
        "email": "lilonglong2000@jnu.ac.kr",
        "homepage": "longlongli.com",
        "header_note": "面向学术合作、博士后申请和成果归档的完整版本。",
        "summary": [
            "博士研究生，研究方向聚焦于 BioMEMS、多模态生物传感器、工程化心脏组织监测和药物心脏毒性评价。",
            "具备 MEMS 器件设计、微纳加工、细胞与组织培养、传感系统搭建和多模态生物信号分析经验。",
            "研究工作围绕应变传感器、微电极阵列和 3D 生物电子平台展开，目标是实现心肌组织机械收缩与电活动的同步、长期和定量检测。",
        ],
        "sections": [
            {"title": "教育经历", "items": [
                "2022-至今 | 全南国立大学，机械工程博士，韩国 光州",
                "2018-2022 | 温州大学，机械工程本科，中国 温州",
            ]},
            {"title": "科研经历", "items": [
                "面向工程化心脏组织设计并开发基于 BioMEMS 的多模态传感平台。",
                "集成应变传感器与微电极阵列，实现心肌组织机械收缩与电活动的同步监测。",
                "建立 3D 工程化心脏组织培养与药物刺激流程，用于药物心脏毒性筛选和疾病模型研究。",
                "开发 MATLAB / Python 信号分析流程，用于提取收缩幅值、搏动频率、场电位特征和机电耦合参数。",
                "搭建包含低噪声信号采集、显微成像、传感器标定和硬件集成在内的实验测量系统。",
            ]},
            {"title": "技术技能", "items": [
                "微纳制造：光刻、金属沉积、SU-8 / PI 工艺、MEMS 传感器制备、器件封装、传感器表征。",
                "生物传感：应变传感器、微电极阵列、机电同步监测、低噪声信号采集、传感器标定。",
                "细胞与组织工程：NRVM / hiPSC-CMs 培养、工程化心脏组织构建、胶原 / dECM 生物墨水、药物刺激实验、免疫染色。",
                "数据分析：MATLAB、Python、心脏信号处理、特征提取、可视化、统计分析。",
                "系统集成：DAQ 系统、放大电路、显微成像、自动化测量平台、实验原型机开发。",
            ]},
            {"title": "项目经历", "items": [
                "2026.03-至今 | 仿生心脏缺氧模型与机电评估平台，MNTL。",
                "2024.03-2026.03 | 基于 3D 心脏组织的高通量药物毒理筛选平台，MNTL。",
                "2022.09-2024.03 | 石墨烯导电微环境对心肌细胞电生理通讯与成熟的调控机制，MNTL。",
                "2022.01-2022.08 | 智能垃圾桶的开发，慈溪卓尚电器有限公司。",
                "2021.01-2021.12 | 桌面级定制食品 3D 打印机，温州大学。",
                "2020.01-2020.12 | 基于视觉识别与导航的玩具收纳机器人，温州大学。",
            ]},
            {"title": "论文发表", "items": FULL_PUBLICATIONS_ZH},
            {"title": "学术会议", "items": FULL_CONFERENCES_ZH},
            {"title": "专利", "items": FULL_PATENTS_ZH},
            {"title": "奖励荣誉", "items": [
                "2025 | BK21 Fellowship Scholarship",
                "2025 | RLRC Outstanding Graduate Student",
                "2021 | 中国国家奖学金",
                "2019 | 浙江省政府奖学金",
            ]},
        ],
    },
    {
        "filename_base": "Longlong_Li_Resume_EN",
        "language": "en",
        "name": "Longlong Li",
        "title": "2-page Resume",
        "position": "PhD Student | BioMEMS / Biosensors / Engineered Cardiac Tissue Monitoring",
        "affiliation": "Department of Mechanical Engineering, Chonnam National University",
        "location": "Gwangju, South Korea",
        "email": "lilonglong2000@jnu.ac.kr",
        "homepage": "longlongli.com",
        "header_note": "Condensed version for HR screening, R&D roles, and industry-facing applications.",
        "summary": [
            "PhD student specializing in BioMEMS, multimodal biosensors, engineered cardiac tissue monitoring, and drug cardiotoxicity evaluation.",
            "Experienced in MEMS device design, microfabrication, cell and tissue culture, sensing system integration, and multimodal biosignal analysis.",
            "Develops strain-sensor / microelectrode-array platforms for synchronized and quantitative assessment of cardiac tissue function.",
        ],
        "sections": [
            {"title": "Education", "items": [
                "2022-Present | Ph.D. in Mechanical Engineering, Chonnam National University, Gwangju, South Korea",
                "2018-2022 | B.Eng. in Mechanical Engineering, Wenzhou University, Wenzhou, China",
            ]},
            {"title": "Research Experience", "items": [
                "Designed BioMEMS-based multimodal sensing platforms for engineered cardiac tissues.",
                "Integrated strain sensors and microelectrode arrays for synchronized monitoring of contraction and electrical activity.",
                "Built 3D cardiac tissue culture, drug stimulation, and signal-analysis workflows for cardiotoxicity screening and disease modeling.",
                "Developed low-noise measurement setups involving microscopy, sensor calibration, DAQ, and multimodal data analysis.",
            ]},
            {"title": "Technical Skills", "items": [
                "Microfabrication: Photolithography, metal deposition, SU-8 / PI processing, MEMS sensor fabrication.",
                "Biosensing: Strain sensors, microelectrode arrays, electromechanical monitoring, sensor calibration.",
                "Cell & Tissue Engineering: NRVM / hiPSC-CMs culture, engineered heart tissue construction, collagen / dECM bioinks.",
                "Data Analysis: MATLAB, Python, cardiac signal processing, feature extraction, visualization.",
                "System Integration: DAQ systems, amplifier circuits, microscopy, automated measurement platforms.",
            ]},
            {"title": "Selected Projects", "items": [
                "Bioinspired Hypoxic Cardiac Model and Electromechanical Evaluation Platform | 2026.03-Present | MNTL | Developed an in vitro cardiac hypoxia model with integrated electromechanical readouts for disease-relevant tissue assessment.",
                "High-Throughput Drug Toxicity Screening Platform Based on 3D Cardiac Tissues | 2024.03-2026.03 | MNTL | Designed a 3D cardiac tissue-based platform integrating mechanical and electrophysiological sensing for cardiotoxicity evaluation.",
                "Graphene-Conductive Microenvironment for Cardiomyocyte Maturation and Electrophysiological Communication | 2022.09-2024.03 | MNTL | Developed graphene/SU-8 platforms and contributed to publication and conference outputs.",
            ]},
            {"title": "Selected Publications", "items": [
                "Graphene SU-8 platform for enhanced cardiomyocyte maturation and intercellular communication in cardiac drug screening. Longlong Li et al. ACS Nano 18(49): 33293-33309, 2024. First author.",
                "Harnessing native blueprints for designing bioinks to bioprint functional cardiac tissue. Mst Zobaida Akter et al.; Longlong Li among co-authors. iScience 28(3), 2025.",
                "Development of multifunctional PAA-alginate-carboxymethyl cellulose hydrogel-loaded fiber-reinforced biomimetic scaffolds for controlled release of curcumin. Kamrun Nahar Fatema, Longlong Li et al. International Journal of Biological Macromolecules 301: 140449, 2025.",
                "Enhancing cardiomyocyte maturation through PEDOT:PSS-coated surfaces and mechanical stimulation with strain sensors. Jongyun Kim, Longlong Li et al. Journal of Micromechanics and Microengineering 35(4): 045002, 2025.",
                "Air-Breakdown Triboelectric Nanogenerator Inspired by Transistor Architecture for Low-Force Human-Machine Interfaces. Karthikeyan Munirathinam, Longlong Li et al. Nano-Micro Letters 18(1): 251, 2026.",
            ]},
            {"title": "Selected Conferences", "items": [
                "IEEE NANOMED 2024 | Enhancing Cardiomyocyte Maturation via Mechanical Stimulation of 3D Printed Cardiac Tissue Using a Origami-based 3D Sensor and Magnetic Fields.",
                "IEEE MEMS 2025 | A Dual-Detection Approach for Cardiotoxicity Screening: Utilizing Nano Silicon Strain Sensor and MEA to Monitor Contractility and Field Potential in Cardiomyocytes.",
                "IEEE SENSORS 2025 | Origami-Inspired 3D Sensor Platform for Real-Time Electromechanical Coupling Analysis in Engineered Heart Tissues.",
                "MicroTAS 2025 | Development of a Multi-Channel Wireless Monitoring Platform for Long-Term Cardiomyocyte Contraction Assessment Using a Polymer Cantilever with Integrated Sensor.",
                "IEEE MEMS 2026 | Multimodal Microelectrode-Microcantilever Array for Electromechanical Analysis of Cardiomyocyte Tissue in Drug Testing.",
            ]},
            {"title": "Patent Summary", "items": [
                "15 patents in total: 4 invention patents, including 3 granted invention patents and 1 published invention patent application.",
                "11 utility model patents spanning agricultural equipment, smart devices, robotics, and electromechanical systems.",
                "Representative patents: Vertical-Folding-Based Clothes Folding Machine (CN113186699B), Household Intelligent Toy Storage Robot (CN112407980B), Automatic Potato Harvester (CN216415123U), Intelligent Launch-and-Recovery Management Device for UAV Swarms (CN216269980U).",
            ]},
            {"title": "Awards", "items": [
                "2025 | BK21 Fellowship Scholarship",
                "2025 | RLRC Outstanding Graduate Student",
                "2021 | China National Scholarship",
                "2019 | Zhejiang Provincial Government Scholarship",
            ]},
        ],
    },
    {
        "filename_base": "Longlong_Li_Resume_ZH",
        "language": "zh",
        "name": "李龙龙",
        "title": "2 页版求职简历",
        "position": "博士研究生 | BioMEMS / 生物传感器 / 工程化心脏组织监测",
        "affiliation": "全南国立大学机械工程系",
        "location": "韩国 光州",
        "email": "lilonglong2000@jnu.ac.kr",
        "homepage": "longlongli.com",
        "header_note": "面向 HR 初筛、研发岗位和产业合作场景的压缩版本。",
        "summary": [
            "博士研究生，研究方向聚焦于 BioMEMS、多模态生物传感器、工程化心脏组织监测和药物心脏毒性评价。",
            "具备 MEMS 器件设计、微纳加工、细胞与组织培养、传感系统搭建和多模态生物信号分析经验。",
            "主要开发集成应变传感器和微电极阵列的 3D 生物电子平台，用于心肌组织功能的同步、长期和定量检测。",
        ],
        "sections": [
            {"title": "教育经历", "items": [
                "2022-至今 | 全南国立大学，机械工程博士，韩国 光州",
                "2018-2022 | 温州大学，机械工程本科，中国 温州",
            ]},
            {"title": "科研经历", "items": [
                "设计面向工程化心脏组织的 BioMEMS 多模态传感平台。",
                "集成应变传感器与微电极阵列，实现机械收缩和电活动的同步监测。",
                "建立 3D 心脏组织培养、药物刺激和信号分析流程，用于药物心脏毒性筛选与疾病模型研究。",
                "搭建包含显微成像、传感器标定、DAQ 和低噪声采集在内的实验测量系统。",
            ]},
            {"title": "技术技能", "items": [
                "微纳制造：光刻、金属沉积、SU-8 / PI 工艺、MEMS 传感器制备。",
                "生物传感：应变传感器、微电极阵列、机电同步监测、传感器标定。",
                "细胞与组织工程：NRVM / hiPSC-CMs 培养、工程化心脏组织构建、胶原 / dECM 生物墨水。",
                "数据分析：MATLAB、Python、心脏信号处理、特征提取、可视化。",
                "系统集成：DAQ 系统、放大电路、显微成像、自动化测量平台。",
            ]},
            {"title": "代表项目", "items": [
                "仿生心脏缺氧模型与机电评估平台 | 2026.03-至今 | MNTL | 构建结合多模态机电读出的体外心脏缺氧模型，用于疾病相关组织评估。",
                "基于 3D 心脏组织的高通量药物毒理筛选平台 | 2024.03-2026.03 | MNTL | 设计集成机械和电生理读出的 3D 心脏组织平台，用于药物心脏毒性评价。",
                "石墨烯导电微环境对心肌细胞电生理通讯与成熟的调控机制 | 2022.09-2024.03 | MNTL | 开发 graphene / SU-8 平台并支撑论文和国际会议成果输出。",
            ]},
            {"title": "代表论文", "items": [
                "Graphene SU-8 platform for enhanced cardiomyocyte maturation and intercellular communication in cardiac drug screening. Longlong Li et al. ACS Nano 18(49): 33293-33309, 2024。第一作者。",
                "Harnessing native blueprints for designing bioinks to bioprint functional cardiac tissue. Mst Zobaida Akter et al.; Longlong Li 为共同作者。iScience 28(3), 2025。",
                "Development of multifunctional PAA-alginate-carboxymethyl cellulose hydrogel-loaded fiber-reinforced biomimetic scaffolds for controlled release of curcumin. Kamrun Nahar Fatema, Longlong Li et al. International Journal of Biological Macromolecules 301: 140449, 2025。",
                "Enhancing cardiomyocyte maturation through PEDOT:PSS-coated surfaces and mechanical stimulation with strain sensors. Jongyun Kim, Longlong Li et al. Journal of Micromechanics and Microengineering 35(4): 045002, 2025。",
                "Air-Breakdown Triboelectric Nanogenerator Inspired by Transistor Architecture for Low-Force Human-Machine Interfaces. Karthikeyan Munirathinam, Longlong Li et al. Nano-Micro Letters 18(1): 251, 2026。",
            ]},
            {"title": "代表会议", "items": [
                "IEEE NANOMED 2024 | Enhancing Cardiomyocyte Maturation via Mechanical Stimulation of 3D Printed Cardiac Tissue Using a Origami-based 3D Sensor and Magnetic Fields。",
                "IEEE MEMS 2025 | A Dual-Detection Approach for Cardiotoxicity Screening: Utilizing Nano Silicon Strain Sensor and MEA to Monitor Contractility and Field Potential in Cardiomyocytes。",
                "IEEE SENSORS 2025 | Origami-Inspired 3D Sensor Platform for Real-Time Electromechanical Coupling Analysis in Engineered Heart Tissues。",
                "MicroTAS 2025 | Development of a Multi-Channel Wireless Monitoring Platform for Long-Term Cardiomyocyte Contraction Assessment Using a Polymer Cantilever with Integrated Sensor。",
                "IEEE MEMS 2026 | Multimodal Microelectrode-Microcantilever Array for Electromechanical Analysis of Cardiomyocyte Tissue in Drug Testing。",
            ]},
            {"title": "专利概览", "items": [
                "共 15 项专利：4 项发明专利，其中 3 项为授权发明专利，1 项为公开发明专利申请。",
                "另有 11 项实用新型专利，覆盖农业装备、智能装置、机器人和机电系统。",
                "代表专利：一种基于纵向折叠的叠衣机（CN113186699B）、一种家用玩具智能收纳机器人（CN112407980B）、一种自动马铃薯收获机（CN216415123U）、一种无人机集群的智能收发管理装置（CN216269980U）。",
            ]},
            {"title": "奖励荣誉", "items": [
                "2025 | BK21 Fellowship Scholarship",
                "2025 | RLRC Outstanding Graduate Student",
                "2021 | 中国国家奖学金",
                "2019 | 浙江省政府奖学金",
            ]},
        ],
    },
]


def set_page(doc: Document) -> None:
    section = doc.sections[0]
    section.page_width = Inches(8.5)
    section.page_height = Inches(11)
    section.top_margin = Inches(0.78)
    section.bottom_margin = Inches(0.7)
    section.left_margin = Inches(0.75)
    section.right_margin = Inches(0.75)
    section.header_distance = Inches(0.35)
    section.footer_distance = Inches(0.35)


def add_bottom_rule(paragraph) -> None:
    p_pr = paragraph._p.get_or_add_pPr()
    p_bdr = p_pr.find(qn("w:pBdr"))
    if p_bdr is None:
        p_bdr = OxmlElement("w:pBdr")
        p_pr.append(p_bdr)
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "4")
    bottom.set(qn("w:space"), "2")
    bottom.set(qn("w:color"), "B6C4D5")
    p_bdr.append(bottom)


def style_document(doc: Document, east_asia_font: str, compact: bool) -> None:
    normal = doc.styles["Normal"]
    normal.font.name = "Arial"
    normal.font.size = Pt(9.5 if compact else 10)
    normal._element.rPr.rFonts.set(qn("w:eastAsia"), east_asia_font)
    normal.paragraph_format.space_after = Pt(2)
    normal.paragraph_format.line_spacing = 1.08 if compact else 1.12

    title = doc.styles["Title"]
    title.font.name = "Arial"
    title.font.size = Pt(22 if compact else 24)
    title.font.bold = True
    title.font.color.rgb = RGBColor(18, 54, 95)
    title._element.rPr.rFonts.set(qn("w:eastAsia"), east_asia_font)

    heading = doc.styles["Heading 1"]
    heading.font.name = "Arial"
    heading.font.size = Pt(11.5)
    heading.font.bold = True
    heading.font.color.rgb = RGBColor(29, 78, 137)
    heading._element.rPr.rFonts.set(qn("w:eastAsia"), east_asia_font)
    heading.paragraph_format.space_before = Pt(8 if compact else 10)
    heading.paragraph_format.space_after = Pt(3)


def add_header(doc: Document, data: dict[str, Any], east_asia_font: str, compact: bool) -> None:
    title = doc.add_paragraph(style="Title")
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = title.add_run(data["name"])
    run.font.name = "Arial"
    run._element.rPr.rFonts.set(qn("w:eastAsia"), east_asia_font)

    p2 = doc.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p2.paragraph_format.space_after = Pt(1)
    for text in (data["position"], data["affiliation"]):
        r = p2.add_run(text + "  ")
        r.bold = True
        r.font.size = Pt(10 if compact else 10.5)
        r.font.name = "Arial"
        r._element.rPr.rFonts.set(qn("w:eastAsia"), east_asia_font)

    p3 = doc.add_paragraph()
    p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p3.paragraph_format.space_after = Pt(4)
    meta = [data["location"], data["email"], f"Homepage: {data['homepage']}"]
    for idx, text in enumerate(meta):
        r = p3.add_run(text)
        r.font.size = Pt(8.8 if compact else 9.2)
        r.font.name = "Arial"
        r._element.rPr.rFonts.set(qn("w:eastAsia"), east_asia_font)
        if idx < len(meta) - 1:
            sep = p3.add_run(" | ")
            sep.font.size = Pt(8.8 if compact else 9.2)
            sep.font.name = "Arial"
            sep._element.rPr.rFonts.set(qn("w:eastAsia"), east_asia_font)

    note = doc.add_paragraph()
    note.paragraph_format.space_after = Pt(8)
    note.paragraph_format.left_indent = Inches(0.03)
    note.paragraph_format.right_indent = Inches(0.03)
    add_bottom_rule(note)
    r = note.add_run(data["header_note"])
    r.italic = True
    r.font.size = Pt(9 if compact else 9.4)
    r.font.name = "Arial"
    r._element.rPr.rFonts.set(qn("w:eastAsia"), east_asia_font)


def add_bullet_group(doc: Document, title: str, items: list[str], east_asia_font: str, compact: bool) -> None:
    h = doc.add_paragraph(style="Heading 1")
    r = h.add_run(title)
    r.font.name = "Arial"
    r._element.rPr.rFonts.set(qn("w:eastAsia"), east_asia_font)

    for item in items:
        p = doc.add_paragraph(style="Normal")
        p.paragraph_format.left_indent = Inches(0.18)
        p.paragraph_format.first_line_indent = Inches(-0.14)
        p.paragraph_format.space_after = Pt(1 if compact else 2)
        bullet = p.add_run("- ")
        bullet.bold = True
        bullet.font.name = "Arial"
        bullet._element.rPr.rFonts.set(qn("w:eastAsia"), east_asia_font)
        body = p.add_run(item)
        body.font.name = "Arial"
        body._element.rPr.rFonts.set(qn("w:eastAsia"), east_asia_font)


def add_footer(doc: Document, label: str) -> None:
    footer = doc.sections[0].footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = footer.add_run(label)
    run.font.size = Pt(8)
    run.font.color.rgb = RGBColor(86, 99, 117)


def build_docx(data: dict[str, Any]) -> Path:
    east_asia_font = "SimSun" if data["language"] == "zh" else "Arial"
    compact = "Resume" in data["filename_base"] or "求职简历" in data["title"]
    doc = Document()
    set_page(doc)
    style_document(doc, east_asia_font, compact)
    add_header(doc, data, east_asia_font, compact)
    profile_title = "Profile" if data["language"] == "en" else "个人简介"
    add_bullet_group(doc, profile_title, data["summary"], east_asia_font, compact)
    for section in data["sections"]:
        add_bullet_group(doc, section["title"], section["items"], east_asia_font, compact)
    add_footer(doc, data["filename_base"])
    path = CV_ASSETS / f"{data['filename_base']}.docx"
    doc.save(path)
    return path


def build_pdf(data: dict[str, Any]) -> Path:
    out = CV_ASSETS / f"{data['filename_base']}.pdf"
    compact = "Resume" in data["filename_base"] or "求职简历" in data["title"]
    font_name = "STSong-Light" if data["language"] == "zh" else "Helvetica"
    title_font = "STSong-Light" if data["language"] == "zh" else "Helvetica-Bold"

    doc = SimpleDocTemplate(
        str(out),
        pagesize=letter,
        leftMargin=0.72 * inch,
        rightMargin=0.72 * inch,
        topMargin=0.64 * inch,
        bottomMargin=0.58 * inch,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Title"],
        fontName=title_font,
        fontSize=18 if compact else 20,
        leading=21 if compact else 24,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#12365F"),
        spaceAfter=4,
    )
    meta_style = ParagraphStyle(
        "MetaStyle",
        parent=styles["BodyText"],
        fontName=font_name,
        fontSize=8.4 if compact else 8.8,
        leading=10.5 if compact else 11.5,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#334155"),
        spaceAfter=2,
    )
    note_style = ParagraphStyle(
        "NoteStyle",
        parent=styles["BodyText"],
        fontName=font_name,
        fontSize=8.6 if compact else 9,
        leading=11 if compact else 12,
        textColor=colors.HexColor("#243143"),
        backColor=colors.HexColor("#F4F7FB"),
        borderColor=colors.HexColor("#B6C4D5"),
        borderWidth=0.4,
        borderPadding=5,
        spaceAfter=7,
    )
    heading_style = ParagraphStyle(
        "HeadingStyle",
        parent=styles["Heading1"],
        fontName=title_font,
        fontSize=10.4 if compact else 11.2,
        leading=12.5 if compact else 13.8,
        textColor=colors.HexColor("#1D4E89"),
        spaceBefore=5 if compact else 7,
        spaceAfter=2,
    )
    bullet_style = ParagraphStyle(
        "BulletStyle",
        parent=styles["BodyText"],
        fontName=font_name,
        fontSize=8.5 if compact else 9,
        leading=10.5 if compact else 11.5,
        leftIndent=12,
        firstLineIndent=-9,
        spaceAfter=1,
        textColor=colors.black,
    )

    story = [
        Paragraph(data["name"], title_style),
        Paragraph(data["position"], meta_style),
        Paragraph(data["affiliation"], meta_style),
        Paragraph(f"{data['location']} | {data['email']} | Homepage: {data['homepage']}", meta_style),
        Spacer(1, 2),
        Paragraph(data["header_note"], note_style),
    ]

    profile_title = "Profile" if data["language"] == "en" else "个人简介"
    story.append(Paragraph(profile_title, heading_style))
    for item in data["summary"]:
        safe = item.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        story.append(Paragraph(f"- {safe}", bullet_style))

    for section in data["sections"]:
        story.append(Paragraph(section["title"], heading_style))
        for item in section["items"]:
            safe = item.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            story.append(Paragraph(f"- {safe}", bullet_style))

    doc.build(story)
    return out


def main() -> None:
    CV_ASSETS.mkdir(parents=True, exist_ok=True)
    pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))
    for data in CVS:
        build_docx(data)
        build_pdf(data)


if __name__ == "__main__":
    main()
