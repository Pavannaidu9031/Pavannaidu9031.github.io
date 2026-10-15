# All the words on the site live here. Edit this file, then run:  python build.py
#
# Every text is a pair: T("English", "中文").  Leave a value as "" to hide it.
# Lines marked  TODO  still need your real details.


def T(en, zh):
    return {"en": en, "zh": zh}


SITE = {
    # Full public address of the site (used for Open Graph link previews).
    # If the repo is named  Pavannaidu9031.github.io  this becomes https://pavannaidu9031.github.io/
    "url": "https://pavannaidu9031.github.io/",
    "name": "Pavan Kalyan",
    "short": "Pavan",
    "email": "pavankalyannaidu722@gmail.com",
    "linkedin": "https://www.linkedin.com/in/pavankalyan9031",
    "github": "https://github.com/Pavannaidu9031",
    "resume": "assets/Pavan-Kalyan-Resume.pdf",
    "portrait": "assets/img/portrait.webp",  # cut-out made by tools/cutout.py
    "portrait_circle": "assets/img/avatar.webp",
    "timezone": "Asia/Taipei",
    "edition": "2026",
}

IDENTITY = {
    "title": T("Thin-Film & Optical Sensor Engineer", "薄膜與光學感測器工程師"),
    "title_lines": [T("Thin-Film & Optical", "薄膜與光學"), T("Sensor Engineer", "感測器工程師")],
    "degree": T("MS Electrical Engineering", "電機工程碩士"),
    "based": T("Based in", "現居"),
    "country": T("Taiwan", "台灣"),
    "location": T("Tainan, Taiwan", "台灣・臺南"),
    "tagline": T(
        "I work where materials science, photonics and software meet, building sensors in the lab and the tools that help optimize them.",
        "我在材料科學、光子學與軟體的交會處工作——在實驗室裡打造感測器，也開發協助優化它們的工具。",
    ),
    "intro": T(
        "MS student in Electrical Engineering at STUST, researching fiber-optic hydrogen sensors made by magnetron sputtering. Before my master's I was a software engineer, so I build my own data tools to speed up experiments.",
        "南臺科技大學電機工程系碩士生，研究以磁控濺鍍製作的光纖氫氣感測器。攻讀碩士前我是一名軟體工程師，所以我會自己開發資料工具來加速實驗。",
    ),
}

# Order here = order on the site (01, 02 …).
PROJECTS = [
    {
        "slug": "fiber-optic-hydrogen-sensor",
        "title": T("Fiber-Optic Hydrogen Sensor", "光纖氫氣感測器"),
        "subtitle": T("MS Thesis", "碩士論文"),
        "category": T("Research / Photonics", "研究／光子學"),
        "group": "research",
        "year": "2026",
        "role": T("Researcher, MS thesis", "研究者（碩士論文）"),
        "status": T("In progress", "進行中"),
        "color": "#1f2a44",
        "summary": T(
            "A WO₃ + Pd bilayer on chemically etched single-mode fiber that senses hydrogen through the evanescent field at 1310 nm.",
            "在化學蝕刻的單模光纖上鍍製 WO₃ + Pd 雙層膜，於 1310 nm 透過消逝波感測氫氣。",
        ),
        "overview": T(
            "WO₃ + Pd bilayer coated on chemically etched single-mode optical fiber (~9 µm core region), with intensity-based evanescent-wave sensing at 1310 nm. WO₃ is deposited by RF and Pd by DC magnetron sputtering, using a ring-coating approach for uniform coverage around the fiber. The focus is low-temperature crystalline WO₃ without high-temperature annealing.",
            "在化學蝕刻的單模光纖（約 9 µm 纖芯區域）上鍍製 WO₃ + Pd 雙層膜，以 1310 nm 進行強度式消逝波感測。WO₃ 以射頻（RF）磁控濺鍍、Pd 以直流（DC）磁控濺鍍製備，並採用環形鍍膜方式讓光纖四周覆蓋均勻。研究重點是在不經高溫退火的情況下，得到低溫結晶的 WO₃。",
        ),
        "highlights": [
            T("Chemically etched single-mode fiber down to the ~9 µm core region so the guided light reaches the coating", "將單模光纖化學蝕刻至約 9 µm 的纖芯區域，讓導光能與鍍膜作用"),
            T("WO₃ sensing layer by RF magnetron sputtering, Pd catalyst layer by DC magnetron sputtering", "以射頻磁控濺鍍製備 WO₃ 感測層，以直流磁控濺鍍製備 Pd 催化層"),
            T("Ring-coating approach for uniform coverage around the fiber", "採用環形鍍膜方式，使光纖周圍覆蓋均勻"),
            T("Intensity-based evanescent-wave readout at 1310 nm", "於 1310 nm 進行強度式消逝波量測"),
            T("Working toward crystalline WO₃ at low temperature, without high-temperature annealing", "目標是在低溫下獲得結晶 WO₃，不需高溫退火"),
        ],
        "stack": ["RF / DC magnetron sputtering", "Fiber etching", "1310 nm optical power", "XRD", "Microscopy"],
        "links": [],
    },
    {
        "slug": "matrixai",
        "title": T("MatrixAI", "MatrixAI"),
        "subtitle": T("", ""),
        "category": T("Machine Learning / Web App", "機器學習／網頁應用"),
        "group": "software",
        "year": "2026",
        "role": T("Designer & developer", "設計與開發"),
        "status": T("Live", "已上線"),
        "color": "#0f3d3a",
        "summary": T(
            "An ML-guided web app that suggests thin-film sputtering parameters from experiment history.",
            "以機器學習為導向的網頁應用，根據實驗歷史建議薄膜濺鍍參數。",
        ),
        "overview": T(
            "ML-guided web app that suggests thin-film sputtering parameters from experiment history, with an experiment ledger, literature PDF parsing, and multi-material tracks (WO₃, Pd, ITO). I built it to shorten the trial-and-error loop of my own deposition runs.",
            "一個以機器學習為導向的網頁應用，根據實驗歷史建議薄膜濺鍍參數，具備實驗紀錄簿、文獻 PDF 解析，以及多材料追蹤（WO₃、Pd、ITO）。我開發它，是為了縮短自己鍍膜實驗中反覆試誤的循環。",
        ),
        "highlights": [
            T("Bayesian optimization: a Gaussian process model with an acquisition function that balances several process goals at once", "貝氏最佳化：以高斯過程模型搭配採集函數，同時兼顧多個製程目標"),
            T("Cuts the sputtering runs needed from 72 to an estimated 15–20", "將所需的濺鍍實驗次數從 72 次減少到預估 15–20 次"),
            T("Experiment ledger that keeps every deposition and its result", "實驗紀錄簿，保存每一次鍍膜與其結果"),
            T("Parses literature PDFs into comparable process data", "解析文獻 PDF，整理成可比較的製程資料"),
            T("Separate tracks for WO₃, Pd and ITO", "WO₃、Pd、ITO 各自獨立的材料追蹤"),
        ],
        "stack": ["Python", "FastAPI", "scikit-learn", "Gaussian processes", "PostgreSQL / Supabase", "Render"],
        "links": [
            {"label": T("Live site", "線上網站"), "url": "https://rock-ai-optimizer.onrender.com"},
            {"label": T("Source code", "原始碼"), "url": "https://github.com/Pavannaidu9031/matrix-ai-optimizer"},
        ],
    },
    {
        "slug": "fiber-etching-study",
        "title": T("Fiber Etching Study", "光纖蝕刻研究"),
        "subtitle": T("", ""),
        "category": T("Research / Fabrication", "研究／製程"),
        "group": "research",
        "year": "2026",
        "role": T("Researcher", "研究者"),
        "status": T("", ""),  # e.g. T("Accepted at CSME 2026", "獲 CSME 2026 接受") once accepted
        "color": "#3b2f4a",
        "summary": T(
            "Temperature-controlled HF etching of optical fiber from 60 to 110 °C, with optical power characterization.",
            "於 60–110 °C 進行溫控式氫氟酸光纖蝕刻，並量測光功率特性。",
        ),
        "overview": T(
            "Temperature-controlled HF-based etching of optical fiber (60–110 °C) with optical power characterization, the preparation step behind the hydrogen sensor.",
            "溫控式氫氟酸（HF）光纖蝕刻（60–110 °C），並進行光功率特性量測，是氫氣感測器的前置製程。",
        ),
        "highlights": [
            T("HF-based etching with the bath held between 60 and 110 °C", "氫氟酸蝕刻，溶液溫度控制在 60–110 °C"),
            T("Optical power tracked to characterize the etched fiber", "量測光功率以描述蝕刻後光纖的特性"),
            T("Feeds directly into the fiber preparation for the H₂ sensor", "直接用於氫氣感測器的光纖前處理"),
        ],
        "stack": ["HF etching", "Temperature control", "Optical power measurement"],
        "links": [],
    },
    {
        "slug": "maa-restaurant-platform",
        "title": T("Maa Restaurant Web Platform", "Maa 餐廳網路平台"),
        "subtitle": T("", ""),
        "category": T("Full-Stack Development", "全端開發"),
        "group": "software",
        "year": "2026",
        "role": T("Full-stack developer", "全端開發"),
        "status": T("Live", "已上線"),
        "color": "#5a2a12",
        "summary": T(
            "Customer website, restaurant management system and QR table ordering for my family's restaurant in India.",
            "為我家在印度的餐廳打造的顧客網站、餐廳管理系統與 QR 碼桌邊點餐。",
        ),
        "overview": T(
            "Customer website, restaurant management system and QR table ordering for my family's restaurant in Puttur, Andhra Pradesh. Guests browse the menu in English or Telugu and order online or from their table; staff see new orders on a live board.",
            "為我家位於印度安得拉邦普圖爾（Puttur）的餐廳打造的顧客網站、餐廳管理系統與 QR 碼桌邊點餐。客人可用英文或泰盧固語瀏覽菜單，線上或在座位上點餐；店員則在即時訂單看板上接單。",
        ),
        "highlights": [
            T("Bilingual customer site (English / Telugu) with the full menu and photos", "雙語顧客網站（英文／泰盧固語），含完整菜單與照片"),
            T("QR codes on each table for ordering from the seat", "每張桌子都有 QR 碼，可直接在座位點餐"),
            T("Online orders flow into a live order board for staff", "線上訂單即時進入店員的訂單看板"),
            T("Installable as an app on phones", "可安裝在手機上當作 App 使用"),
        ],
        "stack": ["Next.js", "Supabase", "Vercel"],
        "links": [
            {"label": T("Live site", "線上網站"), "url": "https://maa-restaurant.vercel.app"},
        ],
    },
]

ABOUT = {
    "headline": T(
        "Building sensors in the lab, and the software that makes them better",
        "在實驗室裡打造感測器，也寫讓它們更好的軟體",
    ),
    "body": [
        T(
            "I'm an MS student in Electrical Engineering at Southern Taiwan University of Science and Technology in Tainan. My research is a fiber-optic hydrogen sensor: a WO₃ + Pd thin film sputtered onto etched optical fiber.",
            "我是南臺科技大學電機工程系的碩士生，現居臺南。我的研究是光纖氫氣感測器：將 WO₃ + Pd 薄膜濺鍍在蝕刻後的光纖上。",
        ),
        T(
            "Before my master's I worked as a software engineer. That background shapes how I do research: when an experiment is slow to tune, I build a tool for it, like MatrixAI, which suggests sputtering parameters from my own run history.",
            "攻讀碩士之前，我是一名軟體工程師。這段經歷影響了我做研究的方式：當實驗難以調整時，我就為它寫一個工具，例如 MatrixAI，它會根據我過去的實驗紀錄建議濺鍍參數。",
        ),
        T(
            "Outside the lab I'm an English Language Teaching Assistant (ELTA) in Taiwan, creating bilingual English/Chinese lessons for elementary students.",
            "實驗室之外，我在台灣擔任英語教學助理（ELTA），為國小學生設計中英雙語課程。",
        ),
        T(
            "I'm looking for a process or equipment engineering internship, or a full-time role after I graduate in June 2027.",
            "我正在尋找製程或設備工程的實習機會，以及 2027 年 6 月畢業後的正職工作。",
        ),
    ],
    "skills": [
        {
            "title": T("Fabrication", "製程"),
            "items": [
                T("RF / DC magnetron sputtering", "射頻／直流磁控濺鍍"),
                T("Fiber etching", "光纖蝕刻"),
                T("Thin-film deposition", "薄膜沉積"),
                T("Optical power measurement", "光功率量測"),
                T("CMOS fabrication, photolithography (coursework)", "CMOS 製程、微影（課程）"),
            ],
        },
        {
            "title": T("Characterization & analysis", "材料分析與數據"),
            "items": [
                T("Microscopy", "顯微鏡觀察"),
                T("XRD (via NCKU facility)", "X 光繞射 XRD（成大貴儀中心）"),
                T("SPC, DOE", "統計製程管制（SPC）、實驗設計（DOE）"),
                T("JMP, Minitab", "JMP、Minitab"),
                T("TCAD (Sentaurus)", "TCAD（Sentaurus）"),
            ],
        },
        {
            "title": T("Software", "軟體"),
            "items": [
                T("Python, C, SQL, MATLAB", "Python、C、SQL、MATLAB"),
                T("FastAPI", "FastAPI"),
                T("scikit-learn", "scikit-learn"),
                T("Supabase", "Supabase"),
                T("Web development", "網頁開發"),
            ],
        },
    ],
    # Each entry: what, where, when. Leave "where"/"when" as "" if unknown.
    "education": [
        {
            "what": T("MS, Electrical Engineering", "電機工程碩士"),
            "where": T("Southern Taiwan University of Science and Technology", "南臺科技大學"),
            "when": T("2025 – June 2027 (expected)", "2025 – 2027 年 6 月（預計）"),
        },
        {
            "what": T("B.Tech, Electronics & Communication Engineering", "電子與通訊工程學士（B.Tech）"),
            "where": T("Sri Venkatesa Perumal College of Engineering and Technology · First Class", "Sri Venkatesa Perumal 工程技術學院・一等學位"),
            "when": T("2019 – 2023", "2019 – 2023"),
        },
    ],
    "experience": [
        {
            "what": T("English Language Teaching Assistant (ELTA)", "英語教學助理（ELTA）"),
            "where": T("Taiwan", "台灣"),
            "when": T("Now", "現在"),
        },
        {
            "what": T("Junior Software Engineer", "初級軟體工程師"),
            "where": T("Trinite Digital, Pondicherry, India", "Trinite Digital（印度本地治里）"),
            "when": T("2024 – 2025", "2024 – 2025"),
        },
    ],
    "interests": [
        T("Semiconductor process engineering", "半導體製程工程"),
        T("Deep tech", "深科技"),
        T("Education", "教育"),
    ],
}
