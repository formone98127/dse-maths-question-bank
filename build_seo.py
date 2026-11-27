#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build on-page SEO assets for hkdse.exampaper.cloud (run from this folder)."""
from __future__ import annotations

import html
import json
import re
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path
from urllib.parse import quote, urlencode

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent / "docs"
SITE = "https://hkdse.exampaper.cloud"
BRAND = "DSE 數學題庫"
# Cache-busting 版本字串：build 時間自動 bump（行為有變都唔會派 7 日舊 asset）。
VER = datetime.now().strftime("%Y%m%d%H%M")
# 英文卷問題頁（paper-N-en/qN/）開關：False 可以只出中文頁分段上線
EMIT_EN_PAGES = True
TODAY = date.today().isoformat()
BANK = f"{SITE}/"
HUB = f"{SITE}/hub/"
OG = f"{SITE}/og-image.png"

SUBJECTS = [
    {
        "id": "math",
        "slug": "math",
        "name": "數學（必修部分）",
        "short": "數學",
        "en": "Mathematics (Compulsory Part)",
        "blurb": "免費 DSE 數學 past paper 集中喺呢度：按年份開卷，或者按課題（例如函數與圖像、三角、圓形幾何）集中操。涵蓋數學必修卷一、卷二，部分年份有中文或英文卷，適合考前操卷同對題。",
        "title": "DSE 數學必修歷屆試題免費 Past Paper（2012–2023）｜DSE 數學題庫",
        "description": "免費查閱 DSE 數學必修部分 2012 至 2023 年歷屆試題，按年份或課題溫習卷一、卷二。DSE 數學題庫 提供題目索引同課題標籤，方便操卷。",
        "h1": "DSE 數學必修歷屆試題",
    },
    {
        "id": "econ",
        "slug": "econ",
        "name": "經濟",
        "short": "經濟",
        "en": "Economics",
        "blurb": "免費 DSE 經濟 past paper：而家有 2015、2017、2020 年卷一（英文卷）。可按課題溫習供求、市場結構、GDP、貨幣銀行同國際貿易，適合想集中操某一類題嘅同學。",
        "title": "DSE 經濟歷屆試題免費 Past Paper（2015、2017、2020）｜DSE 數學題庫",
        "description": "免費查閱 DSE 經濟科歷屆試題，現有 2015、2017、2020 年卷一。可按課題溫習供求、市場、GDP、貨幣同國際貿易等。",
        "h1": "DSE 經濟歷屆試題",
    },
    {
        "id": "chem",
        "slug": "chem",
        "name": "化學",
        "short": "化學",
        "en": "Chemistry",
        "blurb": "免費 DSE 化學 past paper：2012 至 2025 年卷一甲、卷一乙同卷二（中文卷）都有索引。可按年份開卷，亦可按課題例如酸鹼、有機化學、氧化還原集中溫習。",
        "title": "DSE 化學歷屆試題免費 Past Paper（2012–2025）｜DSE 數學題庫",
        "description": "免費查閱 DSE 化學 2012 至 2025 年歷屆試題，包括卷一甲、卷一乙同卷二。DSE 數學題庫 提供題目索引，方便按年份操卷。",
        "h1": "DSE 化學歷屆試題",
    },
    {
        "id": "bio",
        "slug": "bio",
        "name": "生物",
        "short": "生物",
        "en": "Biology",
        "blurb": "免費 DSE 生物 past paper：而家已有 2023 年卷一同卷二（中文卷），可喺手機或電腦直接開題溫習；之後會繼續加其他年份。",
        "title": "DSE 生物歷屆試題免費 Past Paper（2023）｜DSE 數學題庫",
        "description": "免費查閱 DSE 生物歷屆試題。現已提供 2023 年卷一同卷二，可喺 DSE 數學題庫 直接檢視題目。",
        "h1": "DSE 生物歷屆試題",
    },
    {
        "id": "phys",
        "slug": "phys",
        "name": "物理",
        "short": "物理",
        "en": "Physics",
        "blurb": "免費 DSE 物理 past paper：而家已有 2024 年卷一同卷二（中文卷），方便按卷操練同對答案；之後會繼續加其他年份。",
        "title": "DSE 物理歷屆試題免費 Past Paper（2024）｜DSE 數學題庫",
        "description": "免費查閱 DSE 物理歷屆試題。現已提供 2024 年卷一同卷二，可喺 DSE 數學題庫 直接檢視題目。",
        "h1": "DSE 物理歷屆試題",
    },
]

# One landing page per curriculum strand (not per keyword).
STRANDS = [
    {
        "subject_id": "math",
        "name": "數與代數",
        "slug": "number-and-algebra",
        "title": "免費 DSE 數學 數與代數 歷屆試題｜DSE 數學題庫",
        "description": "免費查閱 DSE 數學「數與代數」歷屆試題，按百分法、函數與圖像、數列、變分等課題溫習。DSE 數學題庫 提供題目索引，方便操卷。",
        "h1": "DSE 數學：數與代數",
        "blurb": "集中溫習 DSE 數學必修「數與代數」，包括百分法、指數與對數、方程、函數與圖像、數列同變分等課題。",
        "guide": [
            "「數與代數」係數學必修三大範疇之一，卷一好多代數長題，同卷二前半選擇題，都屬於呢度。內容包括指數對數、多項式、方程不等式、百分法、函數圖像、數列同變分。",
            "溫習時唔好只操單一公式，要留意課題會互相連結，例如函數圖像配不等式，或者百分法配數列增長。",
            "下面先按課題標籤睇呢個範疇嘅覆蓋範圍，再由各課題專頁進入更細嘅題目索引。",
        ],
    },
    {
        "subject_id": "math",
        "name": "度量、圖形與空間",
        "slug": "measures-shape-space",
        "title": "免費 DSE 數學 度量、圖形與空間 歷屆試題｜DSE 數學題庫",
        "description": "免費查閱 DSE 數學「度量、圖形與空間」歷屆試題，按求積法、軌跡等課題溫習三角、坐標同圖形題。DSE 數學題庫 提供題目索引，方便操卷。",
        "h1": "DSE 數學：度量、圖形與空間",
        "blurb": "集中溫習 DSE 數學必修「度量、圖形與空間」，包括三角、求積法、坐標幾何、圓形幾何、軌跡同幾何變換。",
        "guide": [
            "「度量、圖形與空間」包括三角、坐標幾何、圓形幾何、求積法、平面幾何同幾何變換。卷一較後嘅長題成日跨兩個課題，例如相似三角形配三角比，或者直線同圓一齊出。",
            "整體最常見弱項係圖畫完冇標已知邊同角，證明同計算就容易斷節。先標圖再列式，會穩陣得多。",
            "下面按課題列出相關題目，建議先鞏固三角同相似三角形，再做坐標幾何同求積法。",
        ],
    },
    {
        "subject_id": "math",
        "name": "數據處理",
        "slug": "data-handling",
        "title": "免費 DSE 數學 數據處理 歷屆試題｜DSE 數學題庫",
        "description": "免費查閱 DSE 數學「數據處理」歷屆試題，按概率、排列與組合等課題集中溫習統計題。DSE 數學題庫 提供題目索引，方便操卷。",
        "h1": "DSE 數學：數據處理",
        "blurb": "集中溫習 DSE 數學必修「數據處理」，包括統計圖表、集中趨勢與離差、概率同排列與組合。",
        "guide": [
            "「數據處理」包括統計圖表、集中趨勢與離差、概率同排列組合。卷二後半好多讀圖同計算題，卷一亦可能有短統計或概率。",
            "溫習重點係分清兩類思路：一類係讀圖描述數據，另一類係先計數再求概率。見到數字就代入標準差，好易用錯方法。",
            "下面課題標籤可以幫你由圖表讀法練起，再進入概率同排列組合。",
        ],
    },
    {
        "subject_id": "econ",
        "name": "基本經濟概念",
        "slug": "basic-concepts",
        "title": "免費 DSE 經濟 基本經濟概念 歷屆試題｜DSE 數學題庫",
        "description": "免費查閱 DSE 經濟「基本經濟概念」歷屆試題，按機會成本、稀少性、經濟制度等課題溫習。DSE 數學題庫 提供題目索引，方便操卷。",
        "h1": "DSE 經濟：基本經濟概念",
        "blurb": "集中溫習 DSE 經濟「基本經濟概念」，包括機會成本、稀少性、基本經濟問題、經濟制度同價格機制。",
        "guide": [
            "基本經濟概念考稀少性、機會成本、生產可能性曲線（PPC）、基本經濟問題，同唔同經濟制度。選擇題常見陷阱係把會計成本當成機會成本，忽略隱含成本。",
            "PPC 題要分清沿曲線移動同整條曲線向外或向內移，前者係選擇，後者先至係生產力或資源改變。",
            "題庫而家收錄嘅係已有年份嘅經濟卷一題。下面按課題標籤可以重溫機會成本同制度比較點樣問，再由索引打開對應題目。",
        ],
    },
    {
        "subject_id": "econ",
        "name": "生產與企業",
        "slug": "production-firms",
        "title": "免費 DSE 經濟 生產與企業 歷屆試題｜DSE 數學題庫",
        "description": "免費查閱 DSE 經濟「生產與企業」歷屆試題，按成本、規模經濟、公司種類、勞動生產力等課題溫習。DSE 數學題庫 方便按課題操卷。",
        "h1": "DSE 經濟：生產與企業",
        "blurb": "集中溫習 DSE 經濟「生產與企業」，包括公司種類、成本、規模經濟、利潤同勞動生產力。",
        "guide": [
            "生產與企業包括公司種類（獨資、合夥、有限公司）、成本概念、規模經濟、利潤同勞動生產力。會計利潤同經濟利潤要分清；規模經濟亦唔等於「生產愈多平均成本一定下跌」。",
            "題型多數係概念判斷，加少量簡單計算，例如平均成本或勞動生產力。",
            "下面索引按成本、規模經濟同公司種類分類，方便對照同一個概念喺唔同年份嘅問法。",
        ],
    },
    {
        "subject_id": "econ",
        "name": "市場與價格",
        "slug": "market-and-price",
        "title": "免費 DSE 經濟 市場與價格 歷屆試題｜DSE 數學題庫",
        "description": "免費查閱 DSE 經濟「市場與價格」歷屆試題，按供求、彈性、價格上限、補貼同稅負等課題溫習。DSE 數學題庫 方便按課題操卷。",
        "h1": "DSE 經濟：市場與價格",
        "blurb": "集中溫習 DSE 經濟「市場與價格」，包括供求、彈性、價格管制、稅同補貼。",
        "guide": [
            "供求同價格機制係經濟卷一出題大戶，包括需求或供給移動、彈性、價格上限同下限、從量稅同補貼。沿曲線移動唔等於整條曲線移動；稅負歸宿同彈性嘅關係亦經常記反。",
            "計彈性時要分清用邊對價格同數量，同埋講緊漲價定跌價。",
            "下面可以先操供求移動，再集中彈性、價格管制同稅、補貼題。",
        ],
    },
    {
        "subject_id": "econ",
        "name": "市場結構與競爭",
        "slug": "market-structure",
        "title": "免費 DSE 經濟 市場結構與競爭 歷屆試題｜DSE 數學題庫",
        "description": "免費查閱 DSE 經濟「市場結構與競爭」歷屆試題，按完全競爭、壟斷性競爭、寡頭壟斷同價格歧視等課題溫習。",
        "h1": "DSE 經濟：市場結構與競爭",
        "blurb": "集中溫習 DSE 經濟「市場結構與競爭」，包括完全競爭、壟斷性競爭、寡頭壟斷同價格歧視。",
        "guide": [
            "呢部分比較完全競爭、壟斷性競爭、寡頭壟斷同壟斷，以及價格歧視。考生常把「賣家數目」同「產品有冇差異」配錯結構；完全競爭亦只係喺長期先趨向零經濟利潤，短期唔一定。",
            "價格歧視要記條件：市場可以分隔，同唔同市場嘅價格彈性唔一樣。",
            "下面索引適合用嚟對照唔同市場結構特徵，再做情景判斷題。",
        ],
    },
    {
        "subject_id": "econ",
        "name": "效率、公平與政府角色",
        "slug": "efficiency-equity-government",
        "title": "免費 DSE 經濟 效率、公平與政府角色 歷屆試題｜DSE 數學題庫",
        "description": "免費查閱 DSE 經濟「效率、公平與政府角色」歷屆試題，按外部性、堅尼系數、稅制同收入不均等課題溫習。",
        "h1": "DSE 經濟：效率、公平與政府角色",
        "blurb": "集中溫習 DSE 經濟「效率、公平與政府角色」，包括外部性、公營物品、收入不均、堅尼系數同稅制。",
        "guide": [
            "效率、公平同政府角色考外部性、公營物品、市場失靈、收入不均、堅尼系數同稅制。公營物品（非敵對、非排他）唔等於任何由公營機構提供嘅物品；正負外部性該用補貼定稅亦常混淆。",
            "堅尼系數愈接近 1，代表收入分配愈不平均。講政策時要同時交代效率同公平影響。",
            "下面題目可以幫你練習辨識市場失靈類型，再睇政府干預同公平量度點樣出題。",
        ],
    },
    {
        "subject_id": "econ",
        "name": "經濟表現量度",
        "slug": "measuring-performance",
        "title": "免費 DSE 經濟 經濟表現量度 歷屆試題｜DSE 數學題庫",
        "description": "免費查閱 DSE 經濟「經濟表現量度」歷屆試題，按 GDP、名義同實質 GDP、人均 GDP、國民收入等課題溫習。",
        "h1": "DSE 經濟：經濟表現量度",
        "blurb": "集中溫習 DSE 經濟「經濟表現量度」，包括 GDP、名義同實質 GDP、人均 GDP、國民收入同產業結構。",
        "guide": [
            "呢個課題核心係 GDP：生產法、收入法、支出法，名義同實質 GDP、人均 GDP，以及呢啲指標嘅限制。中間產品唔應重複計入 GDP；名義增長亦唔等於生活水平一定提升。",
            "人均 GDP 高，唔代表收入分配均勻，亦量唔到家務、地下經濟或環境代價。",
            "下面索引集中 GDP 相關標籤，建議先分清名義同實質，再做「GDP 量唔到咩」嘅概念題。",
        ],
    },
    {
        "subject_id": "econ",
        "name": "國民收入與價格水平",
        "slug": "national-income-price-level",
        "title": "免費 DSE 經濟 國民收入與價格水平 歷屆試題｜DSE 數學題庫",
        "description": "免費查閱 DSE 經濟「國民收入與價格水平」歷屆試題，按總需求、總供給、AD-AS、產出缺口等課題溫習。",
        "h1": "DSE 經濟：國民收入與價格水平",
        "blurb": "集中溫習 DSE 經濟「國民收入與價格水平」，包括總需求、總供給、AD-AS、潛在產出同產出缺口。",
        "guide": [
            "國民收入同價格水平用 AD–AS 模型，考總需求、總供給移動、短期同長期、潛在產出同產出缺口。價格水平上升唔等於總需求增加，好多時只係沿 AD 曲線移動。",
            "成本推動同需求拉動通脹要分清來源；講產出缺口時，要對住潛在產出嚟描述。",
            "下面索引可以按總需求、總供給嚟操圖形移動題，解釋時講清橫軸係實質產出。",
        ],
    },
    {
        "subject_id": "econ",
        "name": "貨幣與銀行",
        "slug": "money-and-banking",
        "title": "免費 DSE 經濟 貨幣與銀行 歷屆試題｜DSE 數學題庫",
        "description": "免費查閱 DSE 經濟「貨幣與銀行」歷屆試題，按貨幣供應、銀行乘數、聯繫匯率同利率等課題溫習。",
        "h1": "DSE 經濟：貨幣與銀行",
        "blurb": "集中溫習 DSE 經濟「貨幣與銀行」，包括貨幣供應、存款創造、銀行乘數、聯繫匯率同利率。",
        "guide": [
            "貨幣與銀行考貨幣功能、貨幣供應量定義、存款創造同銀行乘數；香港卷亦會出聯繫匯率。超额準備同法定準備容易混淆，乘數公式用錯就成條數唔啱。",
            "聯匯制度下，匯率目標會制約貨幣政策空間，唔好假設金管局可以任意調息而不顧聯匯。",
            "下面索引適合重溫存款創造步驟，再睇聯繫匯率同貨幣供應定義題。",
        ],
    },
    {
        "subject_id": "econ",
        "name": "宏觀經濟問題與政策",
        "slug": "macro-problems-policy",
        "title": "免費 DSE 經濟 宏觀經濟問題與政策 歷屆試題｜DSE 數學題庫",
        "description": "免費查閱 DSE 經濟「宏觀經濟問題與政策」歷屆試題，按通脹、失業、財政政策、貨幣政策等課題溫習。",
        "h1": "DSE 經濟：宏觀經濟問題與政策",
        "blurb": "集中溫習 DSE 經濟「宏觀經濟問題與政策」，包括通脹、失業、財政政策、貨幣政策同貨幣數量理論。",
        "guide": [
            "通脹、失業、財政政策同貨幣政策係宏觀政策題主軸，有時會用到貨幣數量理論。結構性失業同周期性失業要分清；財政擴張係增開支或減稅，方向寫反就會全題錯。",
            "討論政策時，除咗即時方向，都要考慮滯後、擠出效應或通脹代價。",
            "下面可以先做通脹同失業定義題，再對照財政政策同貨幣政策嘅情景判斷。",
        ],
    },
    {
        "subject_id": "econ",
        "name": "國際貿易與金融",
        "slug": "international-trade-finance",
        "title": "免費 DSE 經濟 國際貿易與金融 歷屆試題｜DSE 數學題庫",
        "description": "免費查閱 DSE 經濟「國際貿易與金融」歷屆試題，按比較優勢、貿易得益、匯率、經常帳同國際收支等課題溫習。",
        "h1": "DSE 經濟：國際貿易與金融",
        "blurb": "集中溫習 DSE 經濟「國際貿易與金融」，包括比較優勢、貿易得益、匯率、經常帳同國際收支。",
        "guide": [
            "國際貿易考比較優勢、貿易得益同限制貿易；金融部分包括匯率、經常帳同國際收支。把比較優勢當成絕對優勢，係最常見概念錯；匯率升值或貶值對出口嘅影響亦經常講反。",
            "經常帳同資本／金融帳要分開記錄，睇清楚題目講緊邊一項交易。",
            "下面索引可先操比較優勢嘅數例，再做匯率同國際收支記錄題。",
        ],
    },
]

SID_TO_SUBJECT = {"math": "數學", "econ": "經濟", "chem": "化學", "bio": "生物", "phys": "物理"}
# 純數學站：生成層面只處理 math（econ/chem/bio/phys 檔案留 disk 但 noindex）
SUBJECTS = [s for s in SUBJECTS if s["id"] == "math"]
STRANDS = [s for s in STRANDS if s["subject_id"] == "math"]
SUBJECT_PREFIX = {"數學": "", "經濟": "econ", "化學": "chem", "生物": "bio", "物理": "phys"}
SAMPLE_Q = 3
VISUAL_TUTOR = "https://dsemaths.canonlessons.com"
VISUAL_TUTOR_LABEL = "免費 DSE 數學視覺教程"
SUBJECT_TO_SID = {v: k for k, v in SID_TO_SUBJECT.items()}
SITEMAP_URLS = []
# 手維護、唔經呢個 build 產生嘅 landing 頁：手動列入 sitemap（檔案存在先會加）
EXTRA_SITEMAP_PATHS = [
    "/math/2020/paper-1/",      # 2020 中文卷一（手製頁，data.js 仲未有卷一題目）
    "/math/2024/paper-2-zh/",   # 舊中文卷路徑（同 paper-2 內容重複，保留過渡）
]

PAPER_CODE = {
    "卷一": "paper-1",
    "卷二": "paper-2",
    "卷一甲": "paper-1a",
    "卷一乙": "paper-1b",
    "卷一（M1）": "paper-1m",
    "卷二（M2）": "paper-2m",
    "Paper 1": "paper-1",
    "Paper 2": "paper-2",
    "Paper 1A": "paper-1a",
    "Paper 1B": "paper-1b",
    "Paper 1M": "paper-1m",
    "Paper 2M": "paper-2m",
}
PAPER_ZH = {
    "paper-1": "卷一",
    "paper-2": "卷二",
    "paper-1a": "卷一甲",
    "paper-1b": "卷一乙",
    "paper-1m": "卷一（M1）",
    "paper-2m": "卷二（M2）",
}

# 英文卷頁 chrome 用嘅固定字串（唔好喺模板入面 hardcode 兩次）
PAPER_EN = {
    "paper-1": "Paper 1",
    "paper-2": "Paper 2",
    "paper-1a": "Paper 1A",
    "paper-1b": "Paper 1B",
    "paper-1m": "Paper 1 (M1)",
    "paper-2m": "Paper 2 (M2)",
}


def strip_latex_delims(s):
    """去掉 $ / \\( \\) / \\[ \\] 分隔符，保留內文（供 JSON-LD 純文字）。"""
    for d in ("$", "\\(", "\\)", "\\[", "\\]"):
        s = str(s or "").replace(d, "")
    return s


def paper_en_label(paper):
    return PAPER_EN.get(paper_code_of(paper), str(paper or "Paper 1"))

# Curriculum labels → actual tags in data.js (do not invent tags).
KW_TAG_MAP = {
    "指數與對數": ["指數定律", "對數", "指數函數", "對數方程", "指數方程"],
    "比、率與比例": ["比率與比例", "比與比例", "比", "比例"],
    "多項式（續）": ["多項式", "因式分解", "因式定理", "三次多項式", "多項式展開"],
    "數系": ["複數", "數制", "虛數", "二進制", "進制轉換"],
    "方程與不等式": [
        "不等式", "一元二次方程", "一元方程", "一元一次不等式", "線性規劃",
        "聯立方程", "二次方程", "不等式組", "複合不等式", "線性不等式",
        "分式方程", "二元一次方程組",
    ],
    "三角學與解三角形": [
        "三角比", "三角學", "三角比／角", "三角恆等式", "三角形面積",
        "餘弦定理", "正弦定理", "正弦函數", "三角方程", "誘導公式",
    ],
    "坐標幾何：直線": ["直線方程", "斜率", "點到直線距離", "中點坐標", "直角坐標", "平面坐標"],
    "坐標幾何：圓": ["圓的方程", "圓方程", "直線與圓相交", "直線與圓", "圓心與半徑"],
    "圓形幾何": ["圓的幾何", "圓的性質", "圓周角", "相交弦"],
    "幾何變換": ["變換與對稱", "變換／對稱", "旋轉", "旋轉對稱", "平移", "反射變換", "對稱與變換"],
    "統計圖表": ["統計", "框線圖", "幹葉圖", "棒形圖", "樹狀圖"],
    "集中趨勢與離差": ["集中趨勢", "標準差", "標準分", "離差", "中位數", "平均值", "眾數", "四分位數間距", "方差"],
    # 百分法 has only 1 exact tag hit; map to the real bank tags.
    "百分法": [
        "百分數／利息", "百分比", "百分數", "百分變化", "利息與增長",
        "百分法", "百分之一", "百分之一增長", "盈利虧損", "複利", "本利和",
    ],
}

# High-intent topic landings (clusters of real tags). Tight set, not one URL per rare tag.
TOPIC_PAGES = [
    # math — 數與代數
    {"subject_id": "math", "name": "指數與對數", "slug": "exponents-logarithms", "strand": "number-and-algebra",
     "tags": KW_TAG_MAP["指數與對數"],
     "title": "免費 DSE 數學 指數與對數 歷屆試題｜DSE 數學題庫",
     "description": "免費查閱 DSE 數學「指數與對數」歷屆試題，按指數定律、對數同指數函數等課題操練。DSE 數學題庫 真正完全免費。",
     "h1": "DSE 數學：指數與對數",
     "blurb": "集中溫習指數定律、對數、指數函數同相關方程題。",
     "guide": [
         "DSE 數學卷一、卷二都成日出指數定律、對數換底同指數／對數方程。常見陷阱係唔記得真數要大於 0、底數限制，或者把對數嘅商誤當成差。",
         "卷二選擇題多數考公式變形；卷一就要解方程再驗根，唔好未檢查就作答。",
         "下面題目索引可以按年份同標籤分開操，建議先揀「對數方程」同「指數方程」，再做要把定律同換底一齊用嘅題。",
     ]},
    {"subject_id": "math", "name": "比、率與比例", "slug": "ratio-rate-proportion", "strand": "number-and-algebra",
     "tags": KW_TAG_MAP["比、率與比例"],
     "title": "免費 DSE 數學 比、率與比例 歷屆試題｜DSE 數學題庫",
     "description": "免費查閱 DSE 數學「比、率與比例」歷屆試題，按比率與比例等課題操練。DSE 數學題庫 真正完全免費。",
     "h1": "DSE 數學：比、率與比例",
     "blurb": "集中溫習比率、比例同相關應用題。",
     "guide": [
         "比、率與比例題通常包喺應用情境，例如地圖比例、混合比例或者分速。考生常犯嘅錯係兩邊單位未統一，或者把「比」直接當分數加減。",
         "卷二多數係一條短計；卷一或會同百分法、圖像一齊出現，列式時要寫清對應量。",
         "用下面索引可以按年份重做同一類應用題，對照自己係咪每次都先統一單位再列比例式。",
     ]},
    {"subject_id": "math", "name": "多項式與因式分解", "slug": "polynomials-factorization", "strand": "number-and-algebra",
     "tags": KW_TAG_MAP["多項式（續）"],
     "title": "免費 DSE 數學 多項式與因式分解 歷屆試題｜DSE 數學題庫",
     "description": "免費查閱 DSE 數學「多項式與因式分解」歷屆試題，涵蓋多項式、因式分解同因式定理。DSE 數學題庫 真正完全免費。",
     "h1": "DSE 數學：多項式與因式分解",
     "blurb": "集中溫習多項式、因式分解、因式定理等課題，對應課程「多項式（續）」。",
     "guide": [
         "呢個課題對應課程「多項式（續）」。卷一長題成日要因式分解，或者用因式定理、餘式定理搵未知係數；三次式試根唔齊、展開漏交叉項都好常見。",
         "卷二則多考因式同餘式關係嘅判斷，記得餘式係代入值而唔一定係因式本身。",
         "下面索引集中多項式相關題，建議先做有「因式定理」標籤嘅題，再做要自己展開或比較係數嘅題。",
     ]},
    {"subject_id": "math", "name": "數系", "slug": "number-systems", "strand": "number-and-algebra",
     "tags": KW_TAG_MAP["數系"],
     "title": "免費 DSE 數學 數系 歷屆試題｜DSE 數學題庫",
     "description": "免費查閱 DSE 數學「數系」歷屆試題，按複數、數制同進制轉換等課題操練。DSE 數學題庫 真正完全免費。",
     "h1": "DSE 數學：數系",
     "blurb": "集中溫習複數、數制、進制轉換等數系課題。",
     "guide": [
         "數系題多數圍繞複數運算、虛數單位 i 嘅冪次，以及進制轉換（例如二進制）。把 i² 記錯、或者進制位值對錯，係卷二選擇題好典型嘅失分位。",
         "卷一較少長篇專攻數系，但轉換步驟同複數運算仍然要寫清楚，唔好跳步。",
         "下面索引可以按「複數」同「進制轉換」標籤分開練，先鞏固 i 嘅四次循環，再處理進制。",
     ]},
    {"subject_id": "math", "name": "方程與不等式", "slug": "equations-inequalities", "strand": "number-and-algebra",
     "tags": KW_TAG_MAP["方程與不等式"],
     "title": "免費 DSE 數學 方程與不等式 歷屆試題｜DSE 數學題庫",
     "description": "免費查閱 DSE 數學「方程與不等式」歷屆試題，按一元二次方程、不等式同線性規劃等課題操練。DSE 數學題庫 真正完全免費。",
     "h1": "DSE 數學：方程與不等式",
     "blurb": "集中溫習方程、不等式、聯立方程同線性規劃。",
     "guide": [
         "方程同不等式係卷一必備基本功，由一元二次、聯立方程，到不等式組同線性規劃都會出。",
         "常見陷阱包括：不等式乘負數忘記調轉符號、分式方程漏查分母為零、線性規劃可行域畫錯或頂點代入唔齊。",
         "下面索引題目較多，可以先由「一元二次方程」同「線性規劃」兩條標籤入手，再補複合不等式同聯立方程。",
     ]},
    {"subject_id": "math", "name": "百分法與利息", "slug": "percentages-interest", "strand": "number-and-algebra",
     "tags": KW_TAG_MAP["百分法"],
     "title": "免費 DSE 數學 百分法與利息 歷屆試題｜DSE 數學題庫",
     "description": "免費查閱 DSE 數學「百分法與利息」歷屆試題，按百分數、百分比同利息增長等課題操練。DSE 數學題庫 真正完全免費。",
     "h1": "DSE 數學：百分法與利息",
     "blurb": "集中溫習百分法、百分比、利息同增長題。",
     "guide": [
         "百分法好大機會同利息、增長、盈利虧損一齊出，單利同複利最容易撈亂。連續上升再下跌要用倍率相乘，唔可以當成一次加減。",
         "卷二多係短計；卷一或要列出本利和步驟，百分比變更要寫清「以邊個量做基準」。",
         "下面索引有百分變化、複利同本利和等標籤，建議先拎複利題計熟，再對增長／減少混合題。",
     ]},
    {"subject_id": "math", "name": "函數與圖像", "slug": "functions-graphs", "strand": "number-and-algebra",
     "tags": ["二次函數", "函數與圖像", "函數", "二次函數圖像", "圖像"],
     "title": "免費 DSE 數學 函數與圖像 歷屆試題｜DSE 數學題庫",
     "description": "免費查閱 DSE 數學「函數與圖像」歷屆試題，按二次函數同函數圖像等課題操練。DSE 數學題庫 真正完全免費。",
     "h1": "DSE 數學：函數與圖像",
     "blurb": "集中溫習函數、二次函數同圖像題。",
     "guide": [
         "函數與圖像以二次函數為主，考頂點、對稱軸、與兩軸交點，同圖像平移。配方時符號搞錯，或者把開口方向同判別式用途混淆，都好常見。",
         "卷二常要你睇圖揀式；卷一就要寫出函數，並解釋圖像特徵，唔好只靠心算。",
         "下面索引可以先按「二次函數圖像」操識圖題，再補函數式變形同平移。",
     ]},
    {"subject_id": "math", "name": "數列", "slug": "sequences", "strand": "number-and-algebra",
     "tags": ["數列", "等比數列", "等差數列", "公比"],
     "title": "免費 DSE 數學 數列 歷屆試題｜DSE 數學題庫",
     "description": "免費查閱 DSE 數學「數列」歷屆試題，按等比數列、等差數列等課題操練。DSE 數學題庫 真正完全免費。",
     "h1": "DSE 數學：數列",
     "blurb": "集中溫習數列、等比數列同等差數列。",
     "guide": [
         "等差同等比數列喺卷一、卷二都常見，考通項同前 n 項和，有時要先判斷數列類型。把公差當成公比、或者求和時 n 用錯，係典型失誤；公比為負時符號亦容易漏。",
         "列式前先寫出首項、公差或公比，再代入公式，會穩陣得多。",
         "用下面索引分開「等差數列」同「等比數列」兩類嚟做，對照自己有冇每次先定性再求和。",
     ]},
    {"subject_id": "math", "name": "變分", "slug": "variations", "strand": "number-and-algebra",
     "tags": ["變分", "正變", "部分正變"],
     "title": "免費 DSE 數學 變分 歷屆試題｜DSE 數學題庫",
     "description": "免費查閱 DSE 數學「變分」歷屆試題，按正變等課題操練。DSE 數學題庫 真正完全免費。",
     "h1": "DSE 數學：變分",
     "blurb": "集中溫習變分同正變題。",
     "guide": [
         "變分題主要考正變、反變，同部分正變（例如 y = kx + c 呢類形式）。考生常把部分正變寫成純正變，或者未用已知點就求唔到常數 k。",
         "題目多數係短應用題，只要先寫對變分關係再求常數，已經贏一半。",
         "下面索引數量唔算多，建議逐條列式對照，檢查自己係咪每次都先寫關係、再代入求 k。",
     ]},
    # math — 度量、圖形與空間
    {"subject_id": "math", "name": "三角學與解三角形", "slug": "trigonometry", "strand": "measures-shape-space",
     "tags": KW_TAG_MAP["三角學與解三角形"],
     "title": "免費 DSE 數學 三角學與解三角形 歷屆試題｜DSE 數學題庫",
     "description": "免費查閱 DSE 數學「三角學與解三角形」歷屆試題，按三角比、三角恆等式同正弦／餘弦定理等課題操練。DSE 數學題庫 真正完全免費。",
     "h1": "DSE 數學：三角學與解三角形",
     "blurb": "集中溫習三角比、解三角形、三角恆等式同相關定理。",
     "guide": [
         "三角學喺卷二選擇題好密，卷一亦會有解三角形或求面積。常見題型包括三角比、誘導公式、三角恆等式，以及正弦定理同餘弦定理。",
         "易錯位係 SSA 情況可能有兩解、角度所在象限，同餘弦定理入面嘅符號。未畫圖就代入，好容易用錯角。",
         "下面索引可以先操「正弦定理」同「餘弦定理」標籤，再補恆等式同三角方程。",
     ]},
    {"subject_id": "math", "name": "坐標幾何：直線", "slug": "coordinate-geometry-line", "strand": "measures-shape-space",
     "tags": KW_TAG_MAP["坐標幾何：直線"],
     "title": "免費 DSE 數學 坐標幾何（直線）歷屆試題｜DSE 數學題庫",
     "description": "免費查閱 DSE 數學「坐標幾何：直線」歷屆試題，按直線方程、斜率同點到直線距離等課題操練。DSE 數學題庫 真正完全免費。",
     "h1": "DSE 數學：坐標幾何（直線）",
     "blurb": "集中溫習直線方程同坐標平面上嘅直線問題。",
     "guide": [
         "直線坐標幾何考斜率、兩點式或點斜式、中點、點到直線距離，同平行、垂直條件。垂直線斜率乘積應為 −1，呢個最常記錯。",
         "用一般式 Ax + By + C = 0 計點到直線距離時，係數同常數項容易代入混亂；卷二多短計，卷一或要結合圖形寫方程。",
         "下面索引可按「斜率」同「點到直線距離」分批練習，先寫方程再計距離。",
     ]},
    {"subject_id": "math", "name": "坐標幾何：圓", "slug": "coordinate-geometry-circle", "strand": "measures-shape-space",
     "tags": KW_TAG_MAP["坐標幾何：圓"],
     "title": "免費 DSE 數學 坐標幾何（圓）歷屆試題｜DSE 數學題庫",
     "description": "免費查閱 DSE 數學「坐標幾何：圓」歷屆試題，按圓的方程、直線與圓相交等課題操練。DSE 數學題庫 真正完全免費。",
     "h1": "DSE 數學：坐標幾何（圓）",
     "blurb": "集中溫習圓的方程同直線與圓嘅關係。",
     "guide": [
         "圓嘅坐標幾何集中圓方程、圓心同半徑，以及直線與圓相交。交點數目用判別式判斷；切線對應判別式等於 0，唔好當成普通相交。",
         "未配方就讀圓心，係好常見嘅錯。呢類題圖形感重要，先畫草圖再代入會穩陣啲。",
         "下面索引可以先做「圓的方程」，再專門操「直線與圓相交」。",
     ]},
    {"subject_id": "math", "name": "圓形幾何", "slug": "circle-geometry", "strand": "measures-shape-space",
     "tags": KW_TAG_MAP["圓形幾何"],
     "title": "免費 DSE 數學 圓形幾何 歷屆試題｜DSE 數學題庫",
     "description": "免費查閱 DSE 數學「圓形幾何」歷屆試題，按圓的性質、圓的幾何同圓周角等課題操練。DSE 數學題庫 真正完全免費。",
     "h1": "DSE 數學：圓形幾何",
     "blurb": "集中溫習圓的性質、圓周角同相關幾何題。",
     "guide": [
         "圓形幾何考圓周角、圓心角、切弦定理、相交弦等性質，好多時要寫簡短理由。把圓周角同圓心角所對應嘅弧搞錯，或者相交弦乘積用錯線段，都會失分。",
         "卷二選擇題偏重性質判斷；卷一就要逐步標角度，寫出用咗邊條定理。",
         "下面索引可沿「圓周角」同「相交弦」標籤，睇同一條定理喺唔同年份點樣問。",
     ]},
    {"subject_id": "math", "name": "幾何變換", "slug": "geometric-transformations", "strand": "measures-shape-space",
     "tags": KW_TAG_MAP["幾何變換"],
     "title": "免費 DSE 數學 幾何變換 歷屆試題｜DSE 數學題庫",
     "description": "免費查閱 DSE 數學「幾何變換」歷屆試題，按變換與對稱、平移、旋轉同反射等課題操練。DSE 數學題庫 真正完全免費。",
     "h1": "DSE 數學：幾何變換",
     "blurb": "集中溫習變換、對稱、平移、旋轉同反射。",
     "guide": [
         "幾何變換包括平移、反射、旋轉同旋轉對稱。旋轉中心、旋轉方向（順時針定逆時針），同反射軸認錯，都係典型陷阱。",
         "題目多數配圖，先標原點同像點，再描述變換規則，會少失分。",
         "下面索引可以按「旋轉」同「平移」分開睇，對照圖像自己講一次點樣變過去。",
     ]},
    {"subject_id": "math", "name": "求積法", "slug": "mensuration", "strand": "measures-shape-space",
     "tags": ["求積法", "立體圖形", "立體幾何", "梯形面積", "體積", "曲面面積", "總表面積", "圓錐", "圓錐體", "圓柱體", "直立角柱體", "直立角錐體"],
     "title": "免費 DSE 數學 求積法 歷屆試題｜DSE 數學題庫",
     "description": "免費查閱 DSE 數學「求積法」歷屆試題，按面積、體積同立體圖形等課題操練。DSE 數學題庫 真正完全免費。",
     "h1": "DSE 數學：求積法",
     "blurb": "集中溫習求積法、立體圖形同面積體積題。",
     "guide": [
         "求積法涵蓋平面面積同立體體積、表面積，例如梯形、圓柱、圓錐同角柱、角錐。公式記錯或單位唔統一最易失分；圓錐仲要分清斜高同垂直高。",
         "卷二多直接代公式；卷一或要先拆件，再求總表面積或組合體體積。",
         "下面索引按立體類型標籤分類，建議由圓柱同圓錐先打好公式底，再做組合圖形。",
     ]},
    {"subject_id": "math", "name": "平面幾何與相似三角形", "slug": "plane-geometry-similar-triangles", "strand": "measures-shape-space",
     "tags": ["平面幾何", "相似三角形", "相似圖形", "全等三角形", "等腰三角形", "畢氏定理", "直角三角形"],
     "title": "免費 DSE 數學 平面幾何與相似三角形 歷屆試題｜DSE 數學題庫",
     "description": "免費查閱 DSE 數學「平面幾何與相似三角形」歷屆試題，按相似、全等等課題操練。DSE 數學題庫 真正完全免費。",
     "h1": "DSE 數學：平面幾何與相似三角形",
     "blurb": "集中溫習平面幾何、相似三角形同相關證明題。",
     "guide": [
         "平面幾何常要證明全等或相似，再用比例求邊，或者用畢氏定理處理直角三角形。相似比同面積比要分清，面積比係相似比嘅平方。",
         "等腰三角形底角用錯、證明條件寫唔清，係卷一常見失分；卷二則多快速判斷夠唔夠條件。",
         "下面索引有相似、全等同畢氏定理標籤，可以先操識揀定理，再寫完整證明步驟。",
     ]},
    # math — 數據處理
    {"subject_id": "math", "name": "統計圖表", "slug": "statistical-graphs", "strand": "data-handling",
     "tags": KW_TAG_MAP["統計圖表"],
     "title": "免費 DSE 數學 統計圖表 歷屆試題｜DSE 數學題庫",
     "description": "免費查閱 DSE 數學「統計圖表」歷屆試題，按統計、框線圖、幹葉圖同棒形圖等課題操練。DSE 數學題庫 真正完全免費。",
     "h1": "DSE 數學：統計圖表",
     "blurb": "集中溫習統計圖表，包括框線圖、幹葉圖同棒形圖。",
     "guide": [
         "統計圖表題要識讀框線圖、幹葉圖、棒形圖，有時亦會用樹狀圖。框線圖嘅中位數、四分位數同離群值好易讀錯；幹葉圖亦常漏咗位值。",
         "呢類題多數喺卷二，重點係讀圖同描述數據特徵，而唔係死記公式。",
         "下面索引可以按圖表類型逐種睇，練習由圖直接讀出中位數、範圍或眾數。",
     ]},
    {"subject_id": "math", "name": "集中趨勢與離差", "slug": "central-tendency-dispersion", "strand": "data-handling",
     "tags": KW_TAG_MAP["集中趨勢與離差"],
     "title": "免費 DSE 數學 集中趨勢與離差 歷屆試題｜DSE 數學題庫",
     "description": "免費查閱 DSE 數學「集中趨勢與離差」歷屆試題，按平均、中位數、標準差同標準分等課題操練。DSE 數學題庫 真正完全免費。",
     "h1": "DSE 數學：集中趨勢與離差",
     "blurb": "集中溫習平均值、中位數、眾數、標準差、標準分同離差。",
     "guide": [
         "平均值、中位數、眾數、標準差、方差、四分位數間距同標準分都會考。有極端值時仍用平均代表集中趨勢，或者把標準差同方差單位混淆，都係常見陷阱。",
         "標準分題要分清該數值係高過定低過平均值，計完之後要講返具體意義。",
         "下面索引建議先做「中位數」同「四分位數間距」，再做「標準差」同「標準分」，對照邊種量度啱用喺邊種數據。",
     ]},
    {"subject_id": "math", "name": "概率", "slug": "probability", "strand": "data-handling",
     "tags": ["概率", "期望值", "幾何概率"],
     "title": "免費 DSE 數學 概率 歷屆試題｜DSE 數學題庫",
     "description": "免費查閱 DSE 數學「概率」歷屆試題，按概率同期望值等課題操練。DSE 數學題庫 真正完全免費。",
     "h1": "DSE 數學：概率",
     "blurb": "集中溫習概率同期望值題。",
     "guide": [
         "概率題包括簡單古典概率、幾何概率同期望值。樹狀圖同「有放回／冇放回」最容易亂；幾何概率要用長度或面積比，唔好胡亂數點。",
         "期望值題要睇清單位，同「每次試驗」指緊乜。列樣本空間或樹狀圖再計，會少漏情況。",
         "下面索引集中概率同期望值，可以先純計概率，再做要一併求期望值嘅應用題。",
     ]},
    {"subject_id": "math", "name": "排列與組合", "slug": "permutations-combinations", "strand": "data-handling",
     "tags": ["排列與組合", "計數原理"],
     "title": "免費 DSE 數學 排列與組合 歷屆試題｜DSE 數學題庫",
     "description": "免費查閱 DSE 數學「排列與組合」歷屆試題，按排列、組合同計數原理操練。DSE 數學題庫 真正完全免費。",
     "h1": "DSE 數學：排列與組合",
     "blurb": "集中溫習排列與組合同計數原理。",
     "guide": [
         "排列與組合考計數原理，分別在乎有次序定冇次序。最常見錯誤係用錯 nPr 同 nCr，或者重複元素、限制條件（例如某人要相鄰）未處理。",
         "有時會同概率一齊出：先計總方法數，再計符合條件嘅方法數。",
         "下面索引適合專門操計數題。建議每條先問自己「排定組」，列清情況再計，唔好一看到數字就代入公式。",
     ]},
    # chem — clustered curriculum topics
    {"subject_id": "chem", "name": "化學計量", "slug": "stoichiometry", "strand": None,
     "tags": ["摩爾計算", "實驗式", "濃度", "滴定"],
     "title": "免費 DSE 化學 化學計量 歷屆試題｜DSE 數學題庫",
     "description": "免費查閱 DSE 化學「化學計量」歷屆試題，按摩爾計算、實驗式、濃度同滴定等課題操練。DSE 數學題庫 真正完全免費。",
     "h1": "DSE 化學：化學計量",
     "blurb": "集中溫習摩爾計算、實驗式、濃度同滴定。",
     "guide": [
         "化學計量係化學卷一計算核心，包括摩爾、濃度、實驗式同滴定。未配平就用摩爾比、濃度單位 mol dm⁻³ 混亂，同滴定時分唔清邊樣係標準溶液，都好常見。",
         "實驗式同分子式唔可以直接當成同一樣嘢；要有摩爾質量或倍數關係先至可以由實驗式推分子式。",
         "下面索引可以先做摩爾計算同濃度，再集中操滴定數值題，核對自己有冇先寫平衡方程式。",
     ]},
    {"subject_id": "chem", "name": "酸鹼", "slug": "acids-bases", "strand": None,
     "tags": ["酸鹼", "pH", "中和", "酸"],
     "title": "免費 DSE 化學 酸鹼 歷屆試題｜DSE 數學題庫",
     "description": "免費查閱 DSE 化學「酸鹼」歷屆試題，按 pH、中和同酸等課題操練。DSE 數學題庫 真正完全免費。",
     "h1": "DSE 化學：酸鹼",
     "blurb": "集中溫習酸鹼、pH 同中和題。",
     "guide": [
         "酸鹼題考 pH、強酸弱酸、中和同指示劑。稀釋對 pH 嘅影響好易算錯；中和時若只用體積比而唔用摩爾，答案會偏。弱酸弱鹼唔可以當完全電離。",
         "見到指示劑或滴定曲線，要先判斷等當點附近嘅酸鹼性，先至揀合適指示劑。",
         "下面索引涵蓋酸鹼、pH 同中和，建議先搞清楚強酸強鹼計算，再睇中和同指示劑題。",
     ]},
    {"subject_id": "chem", "name": "有機化學", "slug": "organic-chemistry", "strand": None,
     "tags": ["有機化合物", "醇", "官能基", "聚合物", "有機轉化", "烯", "烯烴", "加成聚合", "酯", "裂解", "單體", "系統命名", "對映異構", "旋光性", "水解", "分餾"],
     "title": "免費 DSE 化學 有機化學 歷屆試題｜DSE 數學題庫",
     "description": "免費查閱 DSE 化學「有機化學」歷屆試題，按官能基、醇、烯、聚合物同有機轉化等課題操練。DSE 數學題庫 真正完全免費。",
     "h1": "DSE 化學：有機化學",
     "blurb": "集中溫習有機化合物、官能基、聚合物同有機轉化。",
     "guide": [
         "有機化學覆蓋面廣：官能基辨認、系統命名、烯嘅加成、醇同酯、聚合物同加成聚合，以至對映異構同旋光性。命名編號、把裂解同分餾攪亂、立體化學未標手性碳，都係常見失分。",
         "卷一同卷二都可能出現轉化圖，先由官能基反應對號入座，再補試劑同條件。",
         "下面索引標籤分得比較細，可以按「官能基」「酯」「聚合物」分條路線嚟操，唔好一次過由頭掃到落。",
     ]},
    {"subject_id": "chem", "name": "氧化還原", "slug": "redox", "strand": None,
     "tags": ["氧化還原", "氧化數", "還原", "氧化"],
     "title": "免費 DSE 化學 氧化還原 歷屆試題｜DSE 數學題庫",
     "description": "免費查閱 DSE 化學「氧化還原」歷屆試題，按氧化數、氧化同還原等課題操練。DSE 數學題庫 真正完全免費。",
     "h1": "DSE 化學：氧化還原",
     "blurb": "集中溫習氧化還原、氧化數同相關反應。",
     "guide": [
         "氧化還原重點係氧化數升降、邊種物質被氧化或還原，以及配平氧化还原方程式。過氧化物同單質嘅氧化數規則最常記漏，電子得失方向亦容易寫反。",
         "配平時先寫半方程再合併，會比憑感覺加減係數穩陣。",
         "下面索引可先用「氧化數」標籤打好基本功，再做要指出氧化劑同還原劑嘅題。",
     ]},
    {"subject_id": "chem", "name": "化學鍵與分子結構", "slug": "bonding-structure", "strand": None,
     "tags": ["分子間引力", "氫鍵", "分子形狀", "電子排佈", "離子化合物", "極性", "分子結構", "電子圖", "結構"],
     "title": "免費 DSE 化學 化學鍵與分子結構 歷屆試題｜DSE 數學題庫",
     "description": "免費查閱 DSE 化學「化學鍵與分子結構」歷屆試題，按分子形狀、氫鍵、電子排佈同極性等課題操練。DSE 數學題庫 真正完全免費。",
     "h1": "DSE 化學：化學鍵與分子結構",
     "blurb": "集中溫習化學鍵、分子結構、分子間引力同電子排佈。",
     "guide": [
         "呢部分考離子鍵同共價鍵、電子圖、分子形狀（VSEPR）、極性，以及分子間引力（包括氫鍵）。把分子間引力當成化學鍵，或者分唔清電子對排佈同分子形狀，都係典型混淆。",
         "畫電子圖時記得標孤對電子；講極性要同時考慮鍵極性和分子形狀。",
         "下面索引可以由「分子形狀」同「氫鍵」入手，對照電子圖題有冇畫齊結構。",
     ]},
    {"subject_id": "chem", "name": "反應速率", "slug": "reaction-rate", "strand": None,
     "tags": ["反應速率", "催化劑"],
     "title": "免費 DSE 化學 反應速率 歷屆試題｜DSE 數學題庫",
     "description": "免費查閱 DSE 化學「反應速率」歷屆試題，按反應速率同催化劑等課題操練。DSE 數學題庫 真正完全免費。",
     "h1": "DSE 化學：反應速率",
     "blurb": "集中溫習反應速率同催化劑題。",
     "guide": [
         "反應速率題多數圍繞濃度、溫度、表面面積、催化劑等影響因素，同埋速率圖像。催化劑唔會改反應焓變，只會改到達平衡或完成反應嘅途徑同時間；瞬間速率同平均速率亦要分清。",
         "讀圖時要認清楚縱軸係濃度定速率，先至解釋斜率或切線。",
         "下面索引相對集中速率概念同催化劑，適合短時間重溫實驗設計同讀圖。",
     ]},
    {"subject_id": "chem", "name": "化學平衡", "slug": "chemical-equilibrium", "strand": None,
     "tags": ["平衡常數", "平衡", "化學平衡", "勒沙特列原理", "勒沙特列"],
     "title": "免費 DSE 化學 化學平衡 歷屆試題｜DSE 數學題庫",
     "description": "免費查閱 DSE 化學「化學平衡」歷屆試題，按平衡常數同勒沙特列原理等課題操練。DSE 數學題庫 真正完全免費。",
     "h1": "DSE 化學：化學平衡",
     "blurb": "集中溫習化學平衡、平衡常數同勒沙特列原理。",
     "guide": [
         "化學平衡考平衡常數 K、濃度商，同勒沙特列原理。加催化劑只改到達平衡嘅時間，唔會改平衡位置；改變溫度先至會改 K 值。寫 K 時唔好把純固體或純液體寫入錯誤位置。",
         "預測平衡移動時，要逐項講清楚濃度、壓強定溫度點樣變，避免只寫「向右」就收工。",
         "下面索引可以先做勒沙特列原理預測，再操要寫平衡常數式嘅計算題。",
     ]},
    {"subject_id": "chem", "name": "電解與電化學", "slug": "electrolysis-electrochemistry", "strand": None,
     "tags": ["電解", "化學電池", "燃料電池", "電鍍", "導電性", "鏽蝕"],
     "title": "免費 DSE 化學 電解與電化學 歷屆試題｜DSE 數學題庫",
     "description": "免費查閱 DSE 化學「電解與電化學」歷屆試題，按電解、化學電池、燃料電池同電鍍等課題操練。DSE 數學題庫 真正完全免費。",
     "h1": "DSE 化學：電解與電化學",
     "blurb": "集中溫習電解、化學電池、燃料電池同電鍍。",
     "guide": [
         "電解、化學電池、燃料電池、電鍍同鏽蝕經常一齊出。陽極、陰極同氧化、還原最常對調；惰性電極同活性電極嘅產物亦容易混淆。",
         "燃料電池同原電池要分清能量轉換方向；電鍍題要同時講陽極溶解同陰極析出。",
         "下面索引可按「電解」同「化學電池」分開練，每次先標電極，再寫半方程。",
     ]},
    {"subject_id": "chem", "name": "熱化學", "slug": "thermochemistry", "strand": None,
     "tags": ["焓變", "赫斯定律", "生成焓", "燃燒焓", "量熱法", "燃燒"],
     "title": "免費 DSE 化學 熱化學 歷屆試題｜DSE 數學題庫",
     "description": "免費查閱 DSE 化學「熱化學」歷屆試題，按焓變、赫斯定律、生成焓同量熱法等課題操練。DSE 數學題庫 真正完全免費。",
     "h1": "DSE 化學：熱化學",
     "blurb": "集中溫習焓變、赫斯定律、燃燒焓同量熱法。",
     "guide": [
         "熱化學考焓變、生成焓、燃燒焓、赫斯定律同量熱法。符號係最大陷阱：放熱過程焓變為負。量熱法亦容易用錯質量（溶液定溶質）或比熱。",
         "用赫斯定律時，先畫清循環再決定邊條方程要反轉或乘倍數，單位要統一為 kJ mol⁻¹。",
         "下面索引建議先做赫斯定律同生成焓，再做量熱法實驗計算。",
     ]},
    {"subject_id": "chem", "name": "金屬與周期表", "slug": "metals-periodic-table", "strand": None,
     "tags": ["周期表", "過渡金屬", "金屬活性序", "同位素", "鋁", "鐵", "金屬", "銅"],
     "title": "免費 DSE 化學 金屬與周期表 歷屆試題｜DSE 數學題庫",
     "description": "免費查閱 DSE 化學「金屬與周期表」歷屆試題，按金屬活性序、過渡金屬、同位素同周期表等課題操練。DSE 數學題庫 真正完全免費。",
     "h1": "DSE 化學：金屬與周期表",
     "blurb": "集中溫習周期表、金屬活性序、過渡金屬同同位素。",
     "guide": [
         "呢類題圍繞周期表趨勢、金屬活性序、過渡金屬特性、同位素，以及鋁、鐵、銅等常見金屬。把原子序同相對原子質量用途混淆，或者活性序同提取方法配錯，都好常見。",
         "過渡金屬題要記得有色離子同可變氧化態；同位素則考質子數相同、中子數唔同。",
         "下面索引可以按「金屬活性序」同「過渡金屬」分組，再對照周期表趨勢題。",
     ]},
]

# 純數學站：TOPIC_PAGES 只保留 math（econ/chem 條目留喺 literal 會令 rebuild 復活舊頁）
TOPIC_PAGES = [tp for tp in TOPIC_PAGES if tp["subject_id"] == "math"]

# Map a curriculum / topic name to its landing slug (same subject).
TOPIC_SLUG_BY_NAME = {}
for _tp in TOPIC_PAGES:
    TOPIC_SLUG_BY_NAME[(_tp["subject_id"], _tp["name"])] = _tp["slug"]
# 多項式（續） lands on the polynomials cluster page
TOPIC_SLUG_BY_NAME[("math", "多項式（續）")] = "polynomials-factorization"
TOPIC_SLUG_BY_NAME[("math", "百分法")] = "percentages-interest"

HUB_TITLE = "免費 DSE 數學歷屆試題 Past Paper（Core／M1／M2）｜DSE 數學題庫"
HUB_DESC = "免費查閱香港中學文憑試（DSE）數學歷屆試題：必修 Core 卷一卷二，仲有延伸 M1、M2。按年份或課題溫習，中英文卷、即時核對選擇題答案。唔使報名，即時喺 DSE 數學題庫開卷。"
HUB_H1 = "香港中學文憑（DSE）數學歷屆試題庫（必修＋延伸）"


def esc(s):
    return html.escape(str(s), quote=True)


def parse_catalog():
    text = (ROOT / "hub/data.js").read_text(encoding="utf-8")
    rows = re.findall(
        r'\{\s*id:\s*"(\w+)",\s*name:\s*"([^"]+)",\s*year:\s*(\d+),\s*paper:\s*"([^"]+)",\s*lang:\s*"([^"]+)",\s*hash:\s*"([^"]+)"'
        r'(?:\s*,\s*path:\s*"([^"]+)")?\s*\}',
        text,
    )
    catalog = []
    skipped = 0
    for i, n, y, p, lg, h, path in rows:
        if i not in SID_TO_SUBJECT:
            # m1/m2 等科目頁由 scripts/gen_m1_pages.py / gen_m2_pages.py 專責生成，呢個 build 跳過
            skipped += 1
            continue
        row = {"id": i, "name": n, "year": int(y), "paper": p, "lang": lg, "hash": h}
        if path:
            row["path"] = path
        catalog.append(row)
    if len(catalog) < 10:
        raise SystemExit(f"catalog parse too small: {len(catalog)}")
    if skipped:
        print("catalog skipped (other-subject rows):", skipped)
    return catalog


def short_name(name):
    return re.sub(r"（.*?）", "", name).replace("\s", " ").strip()


def year_span(rows):
    years = sorted({str(r["year"]) for r in rows}, key=year_sort_key)
    if not years:
        return ""
    ints = [int(y) for y in years if y.isdigit()]
    if len(ints) == len(years):
        if len(years) == 1:
            return years[0]
        if ints == list(range(ints[0], ints[-1] + 1)):
            return f"{ints[0]}–{ints[-1]}"
        if len(years) <= 4:
            return "、".join(years)
        return f"{ints[0]}–{ints[-1]}"
    return "、".join(years)


GA4_ID = "G-LTB27V0RGW"
GA4_TAG = """<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-LTB27V0RGW"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-LTB27V0RGW');
</script>"""


def seo_head(
    title,
    description,
    canonical,
    og_type="website",
    extra="",
    lang="zh-Hant-HK",
    og_locale="zh_HK",
    alternates=None,
    og_image=None,
):
    # alternates: [(hreflang, url), ...]；無 twin 時只出自身語言宣告，唔出同名 URL 嘅假 pair。
    if alternates is None:
        alternates = [(lang, canonical)]
    alt_html = "\n".join(
        f'<link rel="alternate" hreflang="{esc(hl)}" href="{esc(u)}">' for hl, u in alternates
    )
    og_img = og_image or OG
    return f"""<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<meta name="keywords" content="DSE, 香港中學文憑, 歷屆試題, past paper, DSE 數學, DSE 數學題庫, DSE M1, DSE M2, 數學延伸單元, 免費題庫, 按課題">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="googlebot" content="index, follow">
<meta name="author" content="{BRAND}">
<link rel="canonical" href="{esc(canonical)}">
{alt_html}
<meta property="og:type" content="{esc(og_type)}">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:locale" content="{esc(og_locale)}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{esc(canonical)}">
<meta property="og:image" content="{esc(og_img)}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{esc(title)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(description)}">
<meta name="twitter:image" content="{esc(og_img)}">
<meta name="theme-color" content="#0b1220">
<link rel="manifest" href="/manifest.webmanifest">
<link rel="icon" type="image/png" sizes="32x32" href="/icons/favicon-32.png">
<link rel="icon" type="image/png" sizes="192x192" href="/icons/icon-192.png">
<link rel="apple-touch-icon" sizes="180x180" href="/icons/apple-touch-icon.png">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black">
<meta name="apple-mobile-web-app-title" content="{BRAND}">
<meta name="application-name" content="{BRAND}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/hub/style.css?v={VER}">
<link rel="alternate" type="application/rss+xml" title="DSE 數學題庫 最新題目分析" href="{SITE}/feed.xml">
{GA4_TAG}
<script defer src="/js/track.js?v={VER}"></script>
{extra}"""


def ld_json(obj):
    return '<script type="application/ld+json">\n' + json.dumps(obj, ensure_ascii=False, indent=2) + "\n</script>"


def paper_href(row):
    return BANK.rstrip("/") + row["hash"]


def attach_paths(catalog, papers):
    """Copy resolved landing paths (and corrected lang) onto catalog rows."""
    by_hash = {p["hash"]: p for p in papers}
    out = []
    for r in catalog:
        rr = dict(r)
        p = by_hash.get(r["hash"])
        if p:
            rr["path"] = p["path"]
            rr["lang"] = p["lang"]
            rr["paper"] = p["paper"]
            rr["n_questions"] = p.get("n_questions")
        else:
            code = paper_code_of(r["paper"])
            rr["path"] = paper_landing_path(r["id"], r["year"], code, r["lang"])
        out.append(rr)
    return out


def paper_row_html(r):
    sn = short_name(r["name"])
    landing = r.get("path")
    href = landing or paper_href(r)
    nq = r.get("n_questions")
    title = f"文憑試 DSE {sn} {r['year']} · {r['paper']}（{r['lang']}）"
    # 唔再重覆科目名（tag／title 已有）；只保留額外資訊
    extra = []
    if nq:
        extra.append(f"{nq} 題索引")
    elif landing:
        extra.append("目錄已收錄")
    sub_html = (
        f'\n          <div class="paper-sub">{esc(" · ".join(extra))}</div>'
        if extra
        else ""
    )
    return f"""    <article class="paper-row">
      <a class="paper-main" href="{esc(href)}" title="開啟卷頁">
        <div class="paper-year">{r['year']}</div>
        <div class="paper-body">
          <div class="paper-tags">
            <span class="tag subj">{esc(sn)}</span>
            <span class="tag cat">{esc(r['paper'])}</span>
            <span class="tag lang">{esc(r['lang'])}</span>
          </div>
          <div class="paper-title">{esc(title)}</div>{sub_html}
        </div>
      </a>
    </article>"""


def subject_nav(catalog, current=None):
    counts = defaultdict(int)
    for r in catalog:
        counts[r["id"]] += 1
    bits = ['<nav class="subj-nav" aria-label="科目">']
    for s in SUBJECTS:
        n = counts[s["id"]]
        cls = ' class="on"' if current == s["id"] else ""
        bits.append(
            f'<a href="/{s["slug"]}/"{cls}>{esc(s["short"])}<span class="n">{n} 卷</span></a>'
        )
    bits.append("</nav>")
    return "\n        ".join(bits)


_OG_FONT_CANDIDATES = [
    (
        Path("/home/box/.fonts/NotoSansCJKtc-Black.otf"),
        Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"),
        Path("/home/box/.fonts/NotoSansCJKtc-Medium.otf"),
    ),
    (
        Path(r"C:\Windows\Fonts\msjhbd.ttc"),
        Path(r"C:\Windows\Fonts\msjhbd.ttc"),
        Path(r"C:\Windows\Fonts\msjh.ttc"),
    ),
    (
        Path(r"C:\Windows\Fonts\mingliu.ttc"),
        Path(r"C:\Windows\Fonts\mingliu.ttc"),
        Path(r"C:\Windows\Fonts\mingliu.ttc"),
    ),
]


def _og_font_files():
    for black_p, bold_p, med_p in _OG_FONT_CANDIDATES:
        if black_p.exists() and bold_p.exists() and med_p.exists():
            return black_p, bold_p, med_p
    return None


def _og_base(w=1200, h=630):
    img = Image.new("RGB", (w, h), "#0b1220")

    # soft orbs
    def orb(xy, r, color):
        layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        x, y = xy
        ld.ellipse((x - r, y - r, x + r, y + r), fill=color)
        return layer.filter(ImageFilter.GaussianBlur(80))

    base = img.convert("RGBA")
    for layer in (
        orb((220, 80), 340, (61, 139, 253, 90)),
        orb((980, 80), 300, (124, 58, 237, 70)),
        orb((900, 560), 260, (52, 211, 153, 50)),
    ):
        base = Image.alpha_composite(base, layer)
    return base.convert("RGB")


def make_og():
    w, h = 1200, 630
    img = _og_base(w, h)
    draw = ImageDraw.Draw(img)

    ff = _og_font_files()
    fonts = None
    if ff is not None:
        black_p, bold_p, med_p = ff
        try:
            fonts = (
                ImageFont.truetype(str(black_p), 96),
                ImageFont.truetype(str(bold_p), 42, index=0),
                ImageFont.truetype(str(med_p), 32, index=0),
                ImageFont.truetype(str(med_p), 24, index=0),
            )
        except OSError:
            fonts = None
    if fonts is None:
        print("og-image skipped (no CJK font)")
        return
    font_black, font_bold, font_med, font_sm = fonts

    # icon
    icon_path = ROOT / "icons/icon-512.png"
    if icon_path.exists():
        icon = Image.open(icon_path).convert("RGBA").resize((160, 160), Image.Resampling.LANCZOS)
        img.paste(icon, (80, 200), icon)

    left = 280 if icon_path.exists() else 80
    draw.text((left, 168), "DSE 數學題庫", font=font_black, fill="#ffffff")
    draw.text((left, 290), "香港中學文憑數學歷屆試題庫", font=font_bold, fill="#eef3fb")
    draw.text((left, 360), "必修 Core · 延伸 M1 · 延伸 M2", font=font_med, fill="#93c5fd")
    draw.text((left, 430), "免費　按年份或課題　Past Paper", font=font_sm, fill="#8b9bb3")
    draw.text((80, 560), "hkdse.exampaper.cloud", font=font_sm, fill="#64748b")
    out = ROOT / "og-image.png"
    img.save(out, "PNG", optimize=True)
    print("og-image", out, out.stat().st_size)


_OG_Q_FONTS = None


def _question_og_fonts():
    global _OG_Q_FONTS
    if _OG_Q_FONTS is None:
        ff = _og_font_files()
        if ff is None:
            return None
        black_p, bold_p, med_p = ff
        _OG_Q_FONTS = (
            ImageFont.truetype(str(black_p), 72),
            ImageFont.truetype(str(bold_p), 46, index=0),
            ImageFont.truetype(str(med_p), 34, index=0),
            ImageFont.truetype(str(med_p), 26, index=0),
        )
    return _OG_Q_FONTS


def make_question_og(sid, year, code, qno, subject_short, paper_label, topic="", marks=None):
    """逐題 OG 卡：Telegram/WhatsApp 分享預覽帶題號＋課題，唔再全站一張 generic 圖。
    檔案路徑必須同 question_og_url() 一致：/og/<sid>/<year>/<paper-code>/q<qno>.png。"""
    fonts = _question_og_fonts()
    if fonts is None:
        return None
    f_big, f_head, f_med, f_sm = fonts
    img = _og_base()
    draw = ImageDraw.Draw(img)

    draw.text((80, 110), f"DSE {subject_short} {year} {paper_label} 第 {qno} 題", font=f_head, fill="#93c5fd")
    big = str(topic) if topic else "深度分析＋答案"
    if len(big) > 14:
        big = big[:13] + "…"
    draw.text((80, 180), big, font=f_big, fill="#ffffff")
    draw.text((80, 330), "三層解題提示 · 誘答項逆向工程 · 速解策略", font=f_med, fill="#eef3fb")
    meta_bits = ["免費答案＋逐項分析"]
    if marks:
        meta_bits.append(f"{marks} 分")
    draw.text((80, 400), "　".join(meta_bits), font=f_sm, fill="#8b9bb3")
    draw.text((80, 540), "hkdse.exampaper.cloud", font=f_sm, fill="#64748b")

    out = ROOT / "og" / sid / str(year) / str(code).lower() / f"q{qno}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, "PNG", optimize=True)
    return out


def make_htaccess():
    # 呢個函數係 .htaccess 嘅單一來源。同 disk 上手改版保持同步：
    # - 短 cache（HTML 60s、css/js 5min）壓住 Hostinger CDN 預設
    # - 唔再有 /math/<年>/<卷>/ → reader fragment 301（深度分析頁係正式 indexable 頁面）
    (ROOT / ".htaccess").write_text(
        """# DSE 數學題庫 — HTTPS, apex host, static defaults
DirectoryIndex index.html
Options -Indexes

<IfModule mod_rewrite.c>
  RewriteEngine On
  RewriteCond %{HTTPS} !=on
  RewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
  RewriteCond %{HTTP_HOST} ^www\\.hkdse\\.exampaper\\.cloud$ [NC]
  RewriteRule ^ https://hkdse.exampaper.cloud%{REQUEST_URI} [L,R=301]
  # 舊 /questions/math/... 問題頁已併入新深度分析頁 /math/...（同 stub 嘅 canonical/meta-refresh 一致）
  RewriteRule ^questions/math/([0-9]{4})/(paper-[0-9][a-z]?(-en)?)/q([0-9]+)/?$ https://hkdse.exampaper.cloud/math/$1/$2/q$4/ [R=301,L,NE]
</IfModule>

<IfModule mod_headers.c>
  Header set X-Content-Type-Options "nosniff"
  Header set Referrer-Policy "strict-origin-when-cross-origin"
</IfModule>

<IfModule mod_expires.c>
  ExpiresActive On
  # 改完要即刻見到：頁面 60 秒、程式／樣式 5 分鐘
  ExpiresByType text/html "access plus 1 minutes"
  ExpiresByType text/css "access plus 5 minutes"
  ExpiresByType application/javascript "access plus 5 minutes"
  ExpiresByType application/manifest+json "access plus 5 minutes"
  # 內容唔會原地改的資產：長快取
  ExpiresByType image/png "access plus 30 days"
  ExpiresByType image/jpeg "access plus 30 days"
  ExpiresByType image/webp "access plus 30 days"
  ExpiresByType image/svg+xml "access plus 30 days"
  ExpiresByType application/pdf "access plus 30 days"
</IfModule>

<IfModule mod_headers.c>
  # mod_expires 只出 Expires；Cache-Control 亦要短，先至壓得住 Hostinger CDN 的 1 小時預設
  <FilesMatch "\\.(html|htm)$">
    Header set Cache-Control "public, max-age=60, must-revalidate"
  </FilesMatch>
  <FilesMatch "\\.(css|js|json)$">
    Header set Cache-Control "public, max-age=300, must-revalidate"
  </FilesMatch>
  <FilesMatch "sw\\.js$">
    Header set Cache-Control "no-cache"
  </FilesMatch>
</IfModule>

<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/css text/plain application/javascript application/json image/svg+xml
</IfModule>
""",
        encoding="utf-8",
    )


def make_robots():
    # 列出 disk 上實際存在嘅 sitemap*.xml，同 sanity_check 嘅「robots ↔ 檔案一致」互相鎖住。
    sm_lines = "\n".join(
        f"Sitemap: {SITE}/{p.name}"
        for p in sorted(ROOT.glob("sitemap*.xml"))
    )
    (ROOT / "robots.txt").write_text(
        f"""User-agent: *
Allow: /
Disallow: /mathjax/
Disallow: /papers/

{sm_lines}
""",
        encoding="utf-8",
    )


def make_sitemap():
    # De-dupe, never include domain root or PDFs.
    seen = set()
    urls = []
    for loc, pri, freq in SITEMAP_URLS:
        if loc.rstrip("/") == SITE or loc.endswith(".pdf"):
            continue
        if loc in seen:
            continue
        seen.add(loc)
        urls.append((loc, pri, freq))
    # 手維護頁面條目
    for pth in EXTRA_SITEMAP_PATHS:
        if (ROOT / pth.lstrip("/") / "index.html").is_file():
            loc = f"{SITE}{pth}"
            if loc not in seen:
                seen.add(loc)
                urls.append((loc, "0.6", "monthly"))
    # topics/ 課題索引頁（gen_topics_index.py 生成）係 indexable 內容，自動收錄
    for p in sorted((ROOT / "topics").glob("*/index.html")) if (ROOT / "topics").is_dir() else []:
        loc = f"{SITE}/topics/{p.parent.name}/"
        if loc not in seen:
            seen.add(loc)
            urls.append((loc, "0.6", "monthly"))
    # 保留呢個 build 唔會重新產生嘅舊條目（非數學科 notice 頁、bafs/chi 等手維護內容頁）：
    # 檔案仍存在先保留，死鏈自然淘汰。
    sm_path = ROOT / "sitemap.xml"
    if sm_path.is_file():
        for loc in re.findall(r"<loc>(.*?)</loc>", sm_path.read_text(encoding="utf-8")):
            if loc in seen or loc.rstrip("/") == SITE or loc.endswith(".pdf"):
                continue
            # 純數學站：preserve 只保留數學／課題／hub／blog／M1／M2 路徑（bafs/geog 等舊 resource 頁唔再收）
            if not loc.startswith(
                (f"{SITE}/math/", f"{SITE}/topics/", f"{SITE}/hub/", f"{SITE}/blog/", f"{SITE}/m1/", f"{SITE}/m2/")
            ):
                continue
            if sitemap_local_path(loc).is_file():
                seen.add(loc)
                urls.append((loc, "0.5", "monthly"))
    urls.sort(key=lambda x: (0 if x[0] == HUB else 1, x[0]))
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for loc, pri, freq in urls:
        # lastmod 跟輸出檔實際 mtime（呢個 build 無重寫嘅舊頁保留真實日期，唔再派 stale 日期）
        fp = sitemap_local_path(loc)
        lastmod = date.fromtimestamp(fp.stat().st_mtime).isoformat() if fp.is_file() else TODAY
        parts.append(
            f"  <url>\n    <loc>{esc(loc)}</loc>\n    <lastmod>{lastmod}</lastmod>\n    <changefreq>{freq}</changefreq>\n    <priority>{pri}</priority>\n  </url>"
        )
    parts.append("</urlset>\n")
    (ROOT / "sitemap.xml").write_text("\n".join(parts), encoding="utf-8")
    print("sitemap", len(urls), "urls")


def upgrade_legacy_topic_pages():
    # 舊 /topics/<slug>/ 頁（細粒度課題，144 頁、~1800 題列表）係長尾 SEO 資產，保留唔合併；
    # 新 /{sid}/{slug}/（make_topic_pages）係粗粒度 strand hub，兩套粒度唔同、唔係重複內容。
    # 呢度只做衛生修復（冪等）：
    #   1) 退役嘅 /questions/math/... 連結（href＋JSON-LD）改指 301 後嘅新深度分析頁
    #   2) 補 og:image／twitter:card（舊模板欠咗，Telegram/WhatsApp 預覽先有圖）
    tdir = ROOT / "topics"
    if not tdir.is_dir():
        print("legacy topics: no dir, skip")
        return
    n_files = n_links = n_head = 0
    for f in sorted(tdir.glob("*/index.html")):
        h = f.read_text(encoding="utf-8")
        orig = h
        h, k = re.subn(r"/questions/math/([0-9]{4})/([a-z0-9-]+)/q([0-9]+)/", r"/math/\1/\2/q\3/", h)
        n_links += k
        if 'property="og:image"' not in h:
            og = (
                f'<meta property="og:image" content="{SITE}/og-image.png" />\n'
                f'<meta property="og:image:width" content="1200" />\n'
                f'<meta property="og:image:height" content="630" />\n'
                f'<meta name="twitter:card" content="summary_large_image" />'
            )
            h, k2 = re.subn(
                r'(<meta property="og:url" content="[^"]*" />)',
                lambda m: m.group(1) + "\n" + og,
                h,
                count=1,
            )
            n_head += k2
        if h != orig:
            f.write_text(h, encoding="utf-8")
            n_files += 1
    print("legacy topics upgraded", "files", n_files, "links", n_links, "heads", n_head)


def sort_rows(rows):
    return sorted(
        rows,
        key=lambda r: (-year_sort_key(r["year"]), str(r["lang"]), r["name"], r["paper"]),
    )


def make_hub(catalog, papers):
    rows = attach_paths(catalog, papers)
    prerender = "\n".join(paper_row_html(r) for r in sort_rows(rows))
    item_list = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebSite",
                "@id": f"{SITE}/#website",
                "name": BRAND,
                "alternateName": ["DSE 數學題庫", "DSE Maths Past Paper 題庫", "香港中學文憑數學歷屆試題"],
                "url": HUB,
                "inLanguage": "zh-Hant-HK",
                "description": HUB_DESC,
                "publisher": {"@id": f"{SITE}/#org"},
                # SearchAction 要等站內真係有 ?q= 搜尋結果頁先加（目標 URL 冇功能會誤導 Google）
            },
            {
                "@type": "Organization",
                "@id": f"{SITE}/#org",
                "name": BRAND,
                "url": HUB,
                "logo": f"{SITE}/icons/icon-512.png",
            },
            {
                "@type": "CollectionPage",
                "@id": f"{HUB}#page",
                "name": HUB_TITLE,
                "description": HUB_DESC,
                "url": HUB,
                "inLanguage": "zh-Hant-HK",
                "isPartOf": {"@id": f"{SITE}/#website"},
                "about": [
                    {"@type": "Thing", "name": "數學（必修 Core）"},
                    {"@type": "Thing", "name": "數學延伸 M1"},
                    {"@type": "Thing", "name": "數學延伸 M2"},
                ],
                "mainEntity": {"@id": f"{HUB}#papers"},
            },
            {
                "@type": "ItemList",
                "@id": f"{HUB}#papers",
                "name": "DSE 數學歷屆試題卷組",
                "numberOfItems": 3,
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "數學必修 Core（卷一／卷二）", "url": f"{SITE}/math/"},
                    {"@type": "ListItem", "position": 2, "name": "數學延伸 M1", "url": f"{HUB}?track=m1"},
                    {"@type": "ListItem", "position": 3, "name": "數學延伸 M2", "url": f"{HUB}?track=m2"},
                ],
            },
            {
                "@type": "FAQPage",
                "mainEntity": faq_ld_entities(HUB_FAQS),
            },
        ],
    }
    faq_html = faq_block(HUB_FAQS)
    footer_links = (
        f'<a href="/math/">Core 必修</a> · '
        f'<a href="{HUB}?track=m1">M1</a> · '
        f'<a href="{HUB}?track=m2">M2</a>'
    )
    add_sitemap(HUB, "1.0", "daily")
    page = f"""<!DOCTYPE html>
<html lang="zh-Hant-HK">
<head>
{seo_head(HUB_TITLE, HUB_DESC, HUB)}
{ld_json(item_list)}
</head>
<body>
<header class="top">
  <div class="top-row">
    <p class="brand-lockup" aria-label="DSE 數學題庫">
      <span class="brand-dse">DSE</span>
      <span class="brand">數學題庫</span>
    </p>
    <button type="button" class="install-btn" data-install-app title="安裝 DSE 數學題庫至主畫面">
      <span>安裝</span>
    </button>
  </div>
  <h1>{esc(HUB_H1)}</h1>
  <p class="tagline">Core・M1・M2 歷屆試題、逐題深度分析——完全免費嘅 DSE 數學 Past Paper 題庫。</p>
  <div class="install-tip" id="installTip" hidden>
    <div class="install-tip-body">
      <strong>一鍵加入主畫面</strong>
      <span>iPhone／iPad：使用 Safari「分享」→「加入主畫面」。Android／電腦：瀏覽器選單 →「安裝應用程式」。</span>
    </div>
    <button type="button" class="install-tip-x" data-install-close aria-label="關閉"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg></button>
  </div>
</header>

<nav class="filters" aria-label="篩選">
  <div class="filters-inner">
    <div class="seg" id="trackSeg" role="tablist" aria-label="數學卷組">
      <button type="button" data-track="math" class="on" role="tab" aria-selected="true">Core</button>
      <button type="button" data-track="m1" role="tab" aria-selected="false">M1</button>
      <button type="button" data-track="m2" role="tab" aria-selected="false">M2</button>
    </div>
    <div class="seg" id="modeSeg" role="tablist" aria-label="瀏覽方式">
      <button type="button" data-mode="year" class="on" role="tab" aria-selected="true">按年份</button>
      <button type="button" data-mode="topic" role="tab" aria-selected="false">按課題</button>
    </div>
    <div class="topic-search" id="topicSearchWrap" hidden>
      <input type="search" id="topicSearch" placeholder="搜尋課題…" autocomplete="off" enterkeyhint="search" />
      <div class="topic-search-list" id="topicSearchList" hidden></div>
    </div>
    <div class="bar" id="yearBar">
      <div class="field">
        <label for="bYear" id="l2">年份</label>
        <button type="button" class="reel-btn" id="bYear" data-key="year">所有</button>
      </div>
      <div class="field" id="fPaper">
        <label for="bPaper">卷別</label>
        <button type="button" class="reel-btn" id="bPaper" data-key="paper">所有</button>
      </div>
    </div>
  </div>
</nav>

<main>
  <section id="result" class="paper-list" aria-live="polite">
    <p class="list-count">共 {len(rows)} 卷</p>
{prerender}
  </section>
</main>
{faq_html}
<footer>站內只放索引、連結同課題標籤，唔存放試卷原卷 · 只顯示資料庫已有內容<br>卷組：{footer_links}<br>相關：<a href="{esc(VISUAL_TUTOR)}" rel="noopener">{esc(VISUAL_TUTOR_LABEL)}</a></footer>

<!-- 滾輪選擇器 -->
<div class="reel-overlay" id="reel" hidden>
  <div class="reel-backdrop" id="reelBackdrop"></div>
  <div class="reel-sheet" role="dialog" aria-modal="true" aria-labelledby="reelTitle">
    <div class="reel-grabber" aria-hidden="true"></div>
    <div class="reel-head">
      <button type="button" class="reel-link" id="reelCancel">取消</button>
      <span id="reelTitle">年份／卷別</span>
      <button type="button" class="reel-link ok" id="reelDone">完成</button>
    </div>
    <div class="reel-window">
      <div class="reel-highlight" aria-hidden="true"></div>
      <div class="reel-wheel" id="reelWheel"></div>
    </div>
  </div>
</div>

<script src="/data.js?v={VER}"></script>
<script src="/hub/data.js?v={VER}"></script>
<script src="/hub/app.js?v={VER}"></script>
<script src="/pwa.js?v={VER}"></script>
</body>
</html>
"""
    (ROOT / "hub/index.html").write_text(page, encoding="utf-8")
    print("hub index", len(page))


def make_subject_pages(catalog, papers):
    by_id = defaultdict(list)
    for r in papers:
        by_id[r["id"]].append(r)
    for s in SUBJECTS:
        rows = sort_rows(by_id[s["id"]])
        if not rows:
            # 非數學科已落線（catalog 只返數學卷）：唔好重新產生、保留現有 notice 頁
            print("SKIP subject (no papers):", s["id"])
            continue
        span = year_span(rows)
        groups = defaultdict(list)
        for r in rows:
            groups[str(r["year"])].append(r)
        years = sorted(groups, reverse=True)
        year_pills = nav_pills(
            [(year_path(s["id"], y), str(y), y) for y in years],
            label="年份",
        )
        sections = []
        for year in years:
            items = "\n".join(paper_row_html(r) for r in groups[year])
            sections.append(
                f'<section class="year-group" id="y{year}">\n  <h2><a href="{year_path(s["id"], year)}">{year} 年</a></h2>\n  <div class="paper-list">\n{items}\n  </div>\n</section>'
            )
        url = f"{SITE}/{s['slug']}/"
        add_sitemap(url, "0.9", "weekly")
        graph = {
            "@context": "https://schema.org",
            "@graph": [
                ld_breadcrumb([("/hub/", "DSE 數學題庫"), (url, s["short"])]),
                {
                    "@type": "CollectionPage",
                    "name": s["title"],
                    "description": s["description"],
                    "url": url,
                    "inLanguage": "zh-Hant-HK",
                    "isPartOf": {"@id": f"{SITE}/#website"},
                    "about": {"@type": "Thing", "name": f"香港中學文憑 {s['name']}"},
                    "mainEntity": {
                        "@type": "ItemList",
                        "name": f"DSE {s['short']} 歷屆試題",
                        "numberOfItems": len(rows),
                        "itemListElement": [
                            {
                                "@type": "ListItem",
                                "position": i,
                                "name": f"DSE {short_name(r['name'])} {r['year']} {r['paper']}（{r['lang']}）",
                                "url": SITE + r["path"],
                            }
                            for i, r in enumerate(rows, 1)
                        ],
                    },
                },
                {
                    "@type": "FAQPage",
                    "mainEntity": faq_ld_entities(LANDING_FAQS),
                },
            ],
        }
        topic_cta = (
            f'<p class="page-cta"><a href="/hub/?subject={s["id"]}&amp;mode=topic">按課題篩選{esc(s["short"])}題目</a>'
            f' · <a href="/hub/?subject={s["id"]}&amp;mode=year">按年份睇卷</a>'
            f' · <a href="/hub/">返回 DSE 數學題庫主頁</a></p>'
        )
        strand_links = "\n    ".join(
            f'<a href="/{st["subject_id"]}/{st["slug"]}/">{esc(st["name"])}</a>'
            for st in STRANDS
            if st["subject_id"] == s["id"]
        )
        strand_block = ""
        if strand_links:
            strand_block = (
                '<section class="strand-index" aria-label="課題範疇">\n'
                "  <h2>按課題範疇溫習</h2>\n"
                '  <nav class="strand-nav">\n    '
                + strand_links
                + "\n  </nav>\n</section>\n"
            )
        topic_links = [
            (topic_path(tp["subject_id"], tp["slug"]), tp["name"], tp["slug"])
            for tp in TOPIC_PAGES
            if tp["subject_id"] == s["id"]
        ]
        topic_block = ""
        if topic_links:
            topic_block = (
                '<section class="strand-index" aria-label="課題">\n'
                "  <h2>按課題溫習</h2>\n  "
                + nav_pills(topic_links, label="課題")
                + "\n</section>\n"
            )
        faq = faq_block(LANDING_FAQS)
        page = f"""<!DOCTYPE html>
<html lang="zh-Hant-HK">
<head>
{seo_head(s['title'], s['description'], url)}
{ld_json(graph)}
</head>
<body class="subj-page">
<header class="hero">
  <div class="hero-glow" aria-hidden="true"></div>
  <div class="hero-inner">
    {crumb_html([("/hub/", "DSE 數學題庫"), (None, s["short"])])}
    <p class="brand">DSE 數學題庫</p>
    <h1>{esc(s['h1'])}</h1>
    <p class="tagline">{esc(s['blurb'])} 而家資料庫有 {len(rows)} 卷{('（' + span + '）') if span else ''}。</p>
        {subject_nav(catalog, current=s['id'])}
    {year_pills}
    {topic_cta}
  </div>
</header>
<main class="subj-main">
{strand_block}{topic_block}{chr(10).join(sections)}
{faq}
</main>
{site_footer(f'<a href="/hub/">返回 DSE 數學題庫主頁</a>')}
</body>
</html>
"""
        dest = ROOT / s["slug"]
        dest.mkdir(exist_ok=True)
        (dest / "index.html").write_text(page, encoding="utf-8")
        print("subject", s["slug"], len(rows), "papers", "years", len(years))


def patch_css():
    path = ROOT / "hub/style.css"
    text = path.read_text(encoding="utf-8")
    marker = "/* ===== SEO extras ===== */"
    extra = """
/* ===== SEO extras ===== */
.subj-nav {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 16px;
}
.subj-nav a {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 7px 12px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid var(--line);
  color: var(--ink);
  text-decoration: none;
  font-size: 13.5px;
  font-weight: 600;
}
.subj-nav a:hover,
.subj-nav a.on {
  border-color: rgba(61, 139, 253, 0.55);
  background: var(--acc-soft);
}
.subj-nav .n {
  color: var(--mut);
  font-weight: 500;
  font-size: 12px;
}
.crumb {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: var(--mut);
  margin-bottom: 10px;
}
.crumb a { color: #93c5fd; text-decoration: none; }
.crumb a:hover { text-decoration: underline; }
.page-cta { margin-top: 14px; }
.page-cta a {
  color: #93c5fd;
  font-weight: 600;
  text-decoration: none;
}
.page-cta a:hover { text-decoration: underline; }
.subj-main {
  max-width: var(--max);
  margin: 0 auto;
  padding: 8px 18px 24px;
  width: 100%;
}
.year-group { margin: 8px 0 22px; }
.year-group h2 {
  font-size: 16px;
  font-weight: 700;
  margin: 12px 0 8px;
  color: var(--ink);
}
.seo-faq {
  max-width: var(--max);
  margin: 12px auto 8px;
  padding: 0 18px 28px;
  width: 100%;
}
.seo-faq h2 {
  font-size: 16px;
  font-weight: 700;
  margin-bottom: 12px;
}
.seo-faq details {
  border: 1px solid var(--line);
  border-radius: 10px;
  background: var(--bg-elev);
  padding: 10px 14px;
  margin-bottom: 8px;
}
.seo-faq summary {
  cursor: pointer;
  font-weight: 600;
  color: var(--ink);
}
.seo-faq p {
  color: var(--mut);
  margin-top: 8px;
  font-size: 14px;
  line-height: 1.65;
}
footer a {
  color: #93c5fd;
  text-decoration: none;
}
footer a:hover { text-decoration: underline; }

.strand-nav {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 12px;
}
.strand-nav a {
  display: inline-flex;
  align-items: center;
  padding: 7px 12px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid var(--line);
  color: var(--ink);
  text-decoration: none;
  font-size: 13.5px;
  font-weight: 600;
}
.strand-nav a:hover,
.strand-nav a.on {
  border-color: rgba(61, 139, 253, 0.55);
  background: var(--acc-soft);
}
.strand-index { margin: 8px 0 22px; }
.strand-index h2,
.kw-section > h2 {
  font-size: 16px;
  font-weight: 700;
  margin: 12px 0 10px;
  color: var(--ink);
}
.kw-block {
  border: 1px solid var(--line);
  border-radius: 10px;
  background: var(--bg-elev);
  padding: 12px 14px;
  margin-bottom: 10px;
}
.kw-block h3 {
  font-size: 15px;
  font-weight: 700;
  margin: 0 0 6px;
  color: var(--ink);
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: baseline;
}
.kw-block .kw-count {
  color: var(--mut);
  font-weight: 500;
  font-size: 13px;
}
.kw-block p { margin: 6px 0; font-size: 14px; }
.kw-block a {
  color: #93c5fd;
  text-decoration: none;
  font-weight: 600;
}
.kw-block a:hover { text-decoration: underline; }
.kw-block.is-empty p {
  color: var(--mut);
  font-weight: 400;
}
.kw-qs {
  list-style: none;
  margin: 8px 0 0;
  padding: 0;
}
.kw-qs li { margin: 0; }
.kw-qs a {
  display: block;
  font-weight: 500;
  padding: 6px 0;
  border-top: 1px solid var(--line);
  color: var(--ink);
}
.kw-qs a:hover { color: #93c5fd; }
.kw-qs .q-meta {
  color: var(--mut);
  font-size: 12.5px;
  font-weight: 500;
  margin-right: 6px;
}
.year-group h2 a {
  color: inherit;
  text-decoration: none;
}
.year-group h2 a:hover { color: #93c5fd; text-decoration: underline; }
.q-index {
  list-style: none;
  margin: 8px 0 0;
  padding: 0;
}
.q-index li { margin: 0; }
.q-index a {
  display: block;
  font-weight: 500;
  padding: 7px 0;
  border-top: 1px solid var(--line);
  color: var(--ink);
  text-decoration: none;
}
.q-index a:hover { color: #93c5fd; }
.q-index .q-meta {
  color: var(--mut);
  font-size: 12.5px;
  font-weight: 500;
  margin-right: 6px;
}
.q-ai {
  display: inline-block;
  margin-left: 6px;
  padding: 1px 8px;
  border-radius: 999px;
  font-size: 11px;
  font-weight: 700;
  color: #0b62c4;
  background: rgba(11, 98, 196, 0.1);
  border: 1px solid rgba(11, 98, 196, 0.28);
  vertical-align: middle;
}
.q-embed { font-size: 15.5px; line-height: 1.8; max-width: 72ch; }
.q-embed img { max-width: 100%; height: auto; }
.ai-chips { color: var(--mut); font-size: 13px; }
.ai-hints { margin: 10px 0; }
.ai-hint { border: 1px solid var(--line); border-radius: 10px; padding: 8px 12px; margin: 6px 0; background: rgba(255,255,255,0.04); }
.ai-hint summary { cursor: pointer; font-weight: 700; color: #93c5fd; }
.ai-hint div { margin-top: 8px; line-height: 1.8; }
.ai-oa { display: grid; gap: 10px; margin: 10px 0; }
.ai-oa-card { border: 1px solid var(--line); border-radius: 10px; padding: 10px 14px; line-height: 1.7; }
.ai-oa-card strong { color: #93c5fd; }
.ai-oa-meta { margin: 2px 0 4px; font-size: 13px; color: var(--mut); }
.ai-strategy { border: 1px solid rgba(11,98,196,0.35); border-radius: 10px; padding: 10px 14px; background: rgba(11,98,196,0.08); }
.open-cta a {
  display: inline-block;
  margin-top: 4px;
}
footer {
  line-height: 1.7;
}

.topic-guide {
  margin: 8px 0 22px;
  border: 1px solid var(--line);
  border-radius: 10px;
  background: var(--bg-elev);
  padding: 12px 16px 14px;
}
.topic-guide h2 {
  font-size: 16px;
  font-weight: 700;
  margin: 0 0 8px;
  color: var(--ink);
}
.topic-guide p {
  color: var(--mut);
  margin: 0 0 8px;
  font-size: 14px;
  line-height: 1.65;
}
.topic-guide p:last-child {
  margin-bottom: 0;
}
.share-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
  margin: 14px 0 4px;
}
.share-row a,
.share-row button {
  display: inline-flex;
  align-items: center;
  padding: 6px 14px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid var(--line);
  color: var(--ink);
  text-decoration: none;
  font-size: 13.5px;
  font-weight: 600;
  cursor: pointer;
  font-family: inherit;
}
.share-row a:hover,
.share-row button:hover {
  border-color: rgba(61, 139, 253, 0.55);
  background: var(--acc-soft);
}
"""
    if marker in text:
        text = text.split(marker)[0].rstrip() + "\n" + extra
    else:
        text = text.rstrip() + "\n" + extra
    path.write_text(text, encoding="utf-8")
    print("css patched")


def patch_hub_data(papers):
    """Write resolved landing path onto each CATALOG row in hub/data.js."""
    path = ROOT / "hub/data.js"
    text = path.read_text(encoding="utf-8")
    # 中英文同卷同 hash：先用 (hash, lang) 對準；fallback 攞第一個（排序上係中文卷）
    by_key = {(p["hash"], p["lang"]): p["path"] for p in papers}
    by_hash = {}
    for p in papers:
        by_hash.setdefault(p["hash"], p["path"])
    text = re.sub(r",\s*path:\s*\"[^\"]*\"", "", text)

    def add_path(m):
        full = m.group(0)
        hash_ = m.group(1)
        # M1／M2 rows：直接入 /m1|/m2/<year>/paper-1-en/ 卷頁（gen_m1/gen_m2 生成）；
        # 冇 landing 嘅年份（如 PP row）留空 → viewHrefFor fallback reader 深連結
        idm = re.search(r'id:\s*"(\w+)"', full)
        ym = re.search(r'year:\s*(\d{4})', full)
        if idm and ym and idm.group(1) in ("m1", "m2"):
            land = ROOT / idm.group(1) / ym.group(1) / "paper-1-en" / "index.html"
            if land.is_file():
                return full[:-1] + f', path: "/{idm.group(1)}/{ym.group(1)}/paper-1-en/"' + "}"
            return full
        lg = re.search(r'lang:\s*"([^"]+)"', full)
        landing = by_key.get((hash_, lg.group(1))) if lg else None
        if not landing:
            landing = by_hash.get(hash_)
        if not landing:
            return full
        # 揀卷即入題庫 viewer 第一題，唔經卷目錄、唔入深度分析頁
        landing = BANK + hash_
        return full[:-1] + f', path: "{landing}"' + "}"

    new = re.sub(r"\{[^{}]*?hash:\s*\"(#[^\"]+)\"\s*\}", add_path, text)
    if new == text:
        print("hub data.js path patch: no changes")
        return
    path.write_text(new, encoding="utf-8")
    n = new.count('path: "')
    print("hub data.js paths", n)


def patch_app():
    path = ROOT / "hub/app.js"
    text = path.read_text(encoding="utf-8")
    # Keep landing-path helper if an older build rewrote viewHrefFor.
    if "function viewHrefFor(r)" in text and "r.path" not in text.split("function viewHrefFor(r)", 1)[1][:400]:
        old = re.search(
            r"function viewHrefFor\(r\) \{\n  return BANK_URL \+ r\.hash;\n\}",
            text,
        )
        if old:
            text = text.replace(
                old.group(0),
                """const PAPER_CODE = {
  "卷一": "paper-1",
  "卷二": "paper-2",
  "卷一甲": "paper-1a",
  "卷一乙": "paper-1b",
  "Paper 1": "paper-1",
  "Paper 2": "paper-2",
  "Paper 1A": "paper-1a",
  "Paper 1B": "paper-1b",
};

const LANDING_BY_HASH = {
  "#2012P2Q1": "/math/2012/paper-2-en/",
  "#2013P2Q1": "/math/2013/paper-2-en/",
};

function viewHrefFor(r) {
  if (r.path) return r.path;
  if (LANDING_BY_HASH[r.hash]) return LANDING_BY_HASH[r.hash];
  const code = PAPER_CODE[r.paper] || "paper-1";
  const slug = r.lang === "英文" ? `${code}-en` : code;
  return `/${r.id}/${r.year}/${slug}/`;
}""",
                1,
            )
            path.write_text(text, encoding="utf-8")
            print("app.js viewHrefFor -> landing paths")
            text = path.read_text(encoding="utf-8")
    hook = """(function applyQuery() {
  const p = new URLSearchParams(location.search);
  /* 卷組：?track=core|m1|m2（新）；?subject= 舊連結兼容 — econ/chem 等靜默 fallback Core */
  const TRACKS = { core: "math", math: "math", m1: "m1", m2: "m2" };
  const t = (p.get("track") || p.get("subject") || "").toLowerCase();
  if (TRACKS[t]) state.subject = TRACKS[t];
  const mode = p.get("mode");
  if (mode === "topic" || mode === "year") state.mode = mode;
  const year = p.get("year");
  if (year) state.year = year;
  const paper = p.get("paper");
  if (paper) state.paper = paper;
  const topic = p.get("topic") || p.get("tag");
  if (topic) {
    state.topic = topic;
    if (mode !== "year") state.mode = "topic";
  }
})();"""
    if re.search(r"\(function applyQuery\(\) \{.*?\}\)\(\);", text, re.S):
        text = re.sub(
            r"\(function applyQuery\(\) \{.*?\}\)\(\);",
            hook,
            text,
            count=1,
            flags=re.S,
        )
        path.write_text(text, encoding="utf-8")
        print("app.js query hook updated (topic/tag)")
        return
    idx = text.rfind("render();")
    if idx < 0:
        raise SystemExit("render(); not found in app.js")
    text = text[:idx] + hook + "\n\n" + text[idx:]
    path.write_text(text, encoding="utf-8")
    print("app.js query hook added (topic/tag)")



def ensure_root_ga4(text):
    if "G-LTB27V0RGW" in text:
        return text, False
    needle = '<script>\n/* 冇題號'
    if needle not in text:
        # fallback: inject before first script in head, or before </head>
        if "</head>" in text:
            return text.replace("</head>", GA4_TAG + "\n</head>", 1), True
        raise SystemExit("cannot find insertion point for root GA4")
    return text.replace(needle, GA4_TAG + "\n" + needle, 1), True


def patch_root_index():
    path = ROOT / "index.html"
    text = path.read_text(encoding="utf-8")
    text = text.replace('<html lang="zh-Hant">', '<html lang="zh-Hant-HK">', 1)
    # 根頁 canonical/og:url 統一指去域名根（唔好 og:url 指去 /hub/ 造成 canonical 訊號打架）
    root_url = f"{SITE}/"
    text = text.replace(f'<link rel="canonical" href="{HUB}"', f'<link rel="canonical" href="{root_url}"')
    text = text.replace(f'<meta property="og:url" content="{HUB}">', f'<meta property="og:url" content="{root_url}">')
    text = text.replace(f'<link rel="alternate" hreflang="zh-Hant-HK" href="{HUB}">', f'<link rel="alternate" hreflang="zh-Hant-HK" href="{root_url}">')
    text = text.replace(f'<link rel="alternate" hreflang="x-default" href="{HUB}">', f'<link rel="alternate" hreflang="x-default" href="{root_url}">')
    # 放開 pinch-zoom（a11y）
    text = text.replace(
        '<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
    )
    if f'rel="canonical" href="{HUB}"' in text:
        text, added = ensure_root_ga4(text)
        if added:
            path.write_text(text, encoding="utf-8")
            print("root index GA4 added")
        else:
            print("root index already patched")
        return
    old_title = "<title>DSE 題庫 · 數學 · 經濟 · 理科</title>"
    new_title = f"<title>{esc(HUB_TITLE)}</title>"
    if old_title in text:
        text = text.replace(old_title, new_title, 1)
    old_desc = '<meta name="description" content="DSE 數學、經濟、化學、生物、物理歷屆試題，按課題集中溫習。">'
    inject = f'''<meta name="description" content="{esc(HUB_DESC)}">
<link rel="canonical" href="{HUB}">
<link rel="alternate" hreflang="zh-Hant-HK" href="{HUB}">
<link rel="alternate" hreflang="x-default" href="{HUB}">
<meta name="robots" content="index, follow">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:locale" content="zh_HK">
<meta property="og:title" content="{esc(HUB_TITLE)}">
<meta property="og:description" content="{esc(HUB_DESC)}">
<meta property="og:url" content="{HUB}">
<meta property="og:image" content="{OG}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(HUB_TITLE)}">
<meta name="twitter:description" content="{esc(HUB_DESC)}">
<meta name="twitter:image" content="{OG}">'''
    if old_desc not in text:
        # 已 patch 過嘅 root（canonical 已指根）會行呢度，唔使再 inject
        text, added = ensure_root_ga4(text)
        path.write_text(text, encoding="utf-8")
        print("root index already patched (canonical=root)")
        return
    text = text.replace(old_desc, inject, 1)
    noscript = '<noscript><p><a href="/hub/">開啟 DSE 歷屆試題資料庫（DSE 數學題庫）</a>。本站亦有 <a href="/math/">數學</a>、<a href="/econ/">經濟</a>、<a href="/chem/">化學</a>、<a href="/bio/">生物</a>、<a href="/phys/">物理</a> 科目頁。</p></noscript>\n'
    if "<noscript>" not in text:
        text = text.replace("<body>", "<body>\n" + noscript, 1)
    path.write_text(text, encoding="utf-8")
    print("root index patched")


def patch_sw():
    path = ROOT / "sw.js"
    text = path.read_text(encoding="utf-8")
    text = re.sub(r'const CACHE = "dsehub-v[^"]+"', f'const CACHE = "dsehub-v{VER}"', text)
    path.write_text(text, encoding="utf-8")
    print("sw cache bumped")


def parse_topics():
    text = (ROOT / "hub/data.js").read_text(encoding="utf-8")
    start = text.index("const TOPICS = ")
    end = text.index("const PDF_LINKS", start)
    blob = text[start:end]
    topics = {}
    for sid, body in re.findall(r"(\w+):\s*\{(.*?)\n  \},", blob, re.S):
        topics[sid] = {}
        for name, arr in re.findall(r'"([^"]+)":\s*\[(.*?)\]', body, re.S):
            topics[sid][name] = re.findall(r'"([^"]+)"', arr)
    if set(topics) != {"math"}:
        raise SystemExit(f"unexpected TOPICS subjects: {list(topics)}")
    for st in STRANDS:
        kws = topics.get(st["subject_id"], {}).get(st["name"])
        if not kws:
            raise SystemExit(f"strand missing in TOPICS: {st['subject_id']} {st['name']}")
    return topics


def parse_questions():
    text = (ROOT / "data.js").read_text(encoding="utf-8")
    assign = text.index("=")
    data, _ = json.JSONDecoder().raw_decode(text[assign + 1 :].lstrip())
    qs = [q for q in data["questions"] if q.get("type") == "題目"]
    if len(qs) < 800:
        raise SystemExit(f"question parse too small: {len(qs)}")
    return qs


def load_analyses():
    """docs/analysis/<sid>/<year>/<paper-code>/q<qno>.json → key (subject_zh, year, paper_code, qno)。"""
    out = {}
    adir = ROOT / "analysis"
    if not adir.is_dir():
        return out
    for fp in sorted(adir.glob("*/*/*/q*.json")):
        try:
            data = json.loads(fp.read_text(encoding="utf-8"))
        except (OSError, ValueError) as e:
            print("analysis json skipped", fp, e)
            continue
        qq = data.get("question") or {}
        try:
            key = (qq["subject"], str(qq["year"]), paper_code_of(qq["paper"]), int(qq["qno"]))
        except (KeyError, ValueError):
            print("analysis json bad question meta", fp)
            continue
        out[key] = data
    if out:
        print("analyses", len(out))
    return out


def paper_no(paper):
    m = re.search(r"(\d+[A-Za-z]?)", str(paper or ""))
    return m.group(1).upper() if m else "1"


def q_year(q):
    """data.js year 而家有 str／int 仲有 'PP'/'SP'（練習／樣本卷），統一 normalize 做 str。"""
    y = q.get("year")
    return "" if y is None else str(y)


def year_sort_key(y):
    """數字年份做 int（由新到舊排）；PP/SP 排最尾。"""
    s = str(y)
    return int(s) if s.isdigit() else 0


def hash_for_question(q):
    pref = SUBJECT_PREFIX.get(q.get("subject"), "")
    return f"#{pref}{q['year']}P{paper_no(q['paper'])}Q{q['qno']}"


def question_href(q, topic=None):
    params = {"subject": q["subject"]}
    if topic:
        params["tag"] = topic
    return f"{BANK}?{urlencode(params)}{hash_for_question(q)}"


def hub_topic_path(sid, topic=None):
    q = f"subject={sid}&mode=topic"
    if topic:
        q += "&topic=" + quote(topic, safe="")
    return f"/hub/?{q}"


def sort_questions(rows):
    return sorted(
        rows,
        key=lambda q: (-year_sort_key(q["year"]), paper_no(q.get("paper")), int(q.get("qno") or 0)),
    )


def subject_meta(sid):
    for s in SUBJECTS:
        if s["id"] == sid:
            return s
    raise SystemExit(f"unknown subject {sid}")


def questions_for_tag(questions, sid, tag):
    subj = SID_TO_SUBJECT[sid]
    return [q for q in questions if q.get("subject") == subj and tag in (q.get("tags") or [])]


def tags_for_keyword(kw):
    return list(KW_TAG_MAP.get(kw) or [kw])


def questions_for_tags(questions, sid, tags):
    subj = SID_TO_SUBJECT[sid]
    want = set(tags)
    rows = []
    seen = set()
    for q in questions:
        if q.get("subject") != subj:
            continue
        qt = set(q.get("tags") or [])
        if not (qt & want):
            continue
        key = (q.get("year"), q.get("paper"), q.get("qno"))
        if key in seen:
            continue
        seen.add(key)
        rows.append(q)
    return rows


def questions_for_keyword(questions, sid, kw):
    return questions_for_tags(questions, sid, tags_for_keyword(kw))


def add_sitemap(loc, pri, freq):
    if not loc.startswith("http"):
        loc = SITE + loc
    SITEMAP_URLS.append((loc, pri, freq))


FEED_ITEMS = []  # (date_str, title, url) — make_question_pages 填，make_feed 寫出


def _rfc822_date(date_str):
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", str(date_str))
    if not m:
        return ""
    y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    try:
        wd = days[date(y, mo, d).weekday()]
    except ValueError:
        return ""
    return f"{wd}, {d:02d} {months[mo - 1]} {y} 00:00:00 +0800"


def make_feed():
    """RSS 2.0 feed：最新 blog 文＋最新深度分析題目（按 generated 日期，新到舊）。"""
    items = []
    blog_dir = ROOT / "blog"
    if blog_dir.is_dir():
        for f in sorted(blog_dir.glob("*/index.html")):
            t = re.search(r"<title>([^<]*)</title>", f.read_text(encoding="utf-8"))
            url = f"{SITE}/blog/{f.parent.name}/"
            items.append((_rfc822_date(date.fromtimestamp(f.stat().st_mtime).isoformat()), t.group(1) if t else f.parent.name, url))
    for d, title, url in FEED_ITEMS:
        items.append((_rfc822_date(d), title, url))
    seen = set()
    uniq = []
    for it in sorted(items, key=lambda x: x[0] or "", reverse=True):
        if it[2] in seen:
            continue
        seen.add(it[2])
        uniq.append(it)
    uniq = uniq[:60]
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss version="2.0"><channel>',
        f"<title>DSE 數學題庫 最新題目分析</title>",
        f"<link>{SITE}/</link>",
        "<description>DSE 數學逐題深度分析＋備試文章（hkdse.exampaper.cloud）</description>",
        "<language>zh-Hant-HK</language>",
    ]
    for d, title, url in uniq:
        parts.append(
            f"<item><title>{esc(title)}</title><link>{esc(url)}</link>"
            f"<guid>{esc(url)}</guid>{('<pubDate>' + d + '</pubDate>') if d else ''}</item>"
        )
    parts.append("</channel></rss>")
    (ROOT / "feed.xml").write_text("\n".join(parts), encoding="utf-8")
    print("feed", len(uniq), "items")


def topic_path(sid, slug):
    return f"/{sid}/{slug}/"


def topic_url_for_name(sid, name):
    slug = TOPIC_SLUG_BY_NAME.get((sid, name))
    return topic_path(sid, slug) if slug else None


def topic_page_for_name(sid, name):
    for tp in TOPIC_PAGES:
        if tp["subject_id"] == sid and tp["name"] == name:
            return tp
    return None


def topic_question_count(questions, sid, tp):
    subj = SID_TO_SUBJECT[sid]
    want = set(tp["tags"])
    seen = set()
    for q in questions:
        if q.get("subject") != subj:
            continue
        if set(q.get("tags") or []) & want:
            seen.add((q.get("year"), q.get("paper"), q.get("qno")))
    return len(seen)


def question_og_url(sid, year, code, qno):
    # 逐題 OG 圖（make_question_og 生成），檔案路徑同 URL 必須一致
    return f"{SITE}/og/{sid}/{year}/{str(code).lower()}/q{qno}.png"


def legacy_topic_map():
    # docs/topics/_mapping.json：題目 tag → 舊細粒度課題頁 slug（/topics/<slug>/）
    fp = ROOT / "topics" / "_mapping.json"
    try:
        data = json.loads(fp.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return {e["tag"]: e["slug"] for e in data.get("tags", []) if e.get("mapped") and e.get("slug")}


def legacy_topic_counts(questions):
    """回 (tag→slug map, slug→不重複題數)——問題頁「所屬課題」連結用。"""
    tmap = legacy_topic_map()
    counts = defaultdict(set)
    for q in questions:
        for t in q.get("tags") or []:
            slug = tmap.get(t)
            if slug:
                counts[slug].add((q.get("year"), q.get("paper"), q.get("qno")))
    return tmap, {k: len(v) for k, v in counts.items()}


def question_topic_chips(q, tmap, tcounts, limit=2):
    out = []
    seen = set()
    for t in q.get("tags") or []:
        slug = tmap.get(t)
        if not slug or slug in seen:
            continue
        seen.add(slug)
        out.append((t, slug, tcounts.get(slug, 0)))
        if len(out) >= limit:
            break
    return out


def crumb_html(items):
    bits = ['<nav class="crumb" aria-label="麵包屑">']
    for i, (href, label) in enumerate(items):
        if i:
            bits.append('<span aria-hidden="true">／</span>')
        if href:
            bits.append(f'<a href="{esc(href)}">{esc(label)}</a>')
        else:
            bits.append(f"<span>{esc(label)}</span>")
    bits.append("</nav>")
    return "\n      ".join(bits)


def ld_breadcrumb(items):
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i,
                "name": label,
                **({"item": href if href.startswith("http") else SITE + href} if href else {}),
            }
            for i, (href, label) in enumerate(items, 1)
        ],
    }


def site_footer(extra=""):
    vt = f'<a href="{esc(VISUAL_TUTOR)}" rel="noopener">{esc(VISUAL_TUTOR_LABEL)}</a>'
    parts = [extra] if extra else []
    parts.append(f'<a href="/hub/">DSE 數學題庫 主頁</a>')
    parts.append(f"相關：{vt}")
    parts.append("站內只放索引、連結同課題標籤，只顯示資料庫已有內容")
    return "<footer>" + " · ".join(parts) + "</footer>"



def topic_guide_html(guide):
    """Render the exam-focused study notes block for a topic or strand page."""
    if not guide:
        return ""
    if isinstance(guide, str):
        parts = [p.strip() for p in guide.split("\n") if p.strip()]
    else:
        parts = [str(p).strip() for p in guide if str(p).strip()]
    if not parts:
        return ""
    paras = "\n".join(f"  <p>{esc(p)}</p>" for p in parts)
    return (
        '<section class="topic-guide" aria-labelledby="topic-guide-heading">\n'
        '  <h2 id="topic-guide-heading">溫習要點同常見題型</h2>\n'
        f"{paras}\n"
        "</section>"
    )


def faq_block(pairs):
    details = []
    for i, (q, a) in enumerate(pairs):
        open_attr = " open" if i == 0 else ""
        details.append(
            "  <details{open}>\n    <summary>{q}</summary>\n    <p>{a}</p>\n  </details>".format(
                open=open_attr, q=esc(q), a=esc(a)
            )
        )
    return (
        '<section class="seo-faq" aria-label="常見問題">\n  <h2>常見問題</h2>\n'
        + "\n".join(details)
        + "\n</section>"
    )


FAQ_FREE = (
    "DSE 數學題庫係咪免費？",
    "係，真正完全免費查閱 DSE 數學歷屆試題索引同題目，唔使報名，亦唔使信用卡。",
)
FAQ_TOPIC = (
    "可唔可以按課題操練？",
    "可以。喺 DSE 數學題庫揀「按課題」，或者開啟各課題頁，就會列出相關題目，方便集中操同一類型。",
)
FAQ_FIND_YEAR = (
    "點樣搵某一年嘅 DSE past paper？",
    "喺 DSE 數學題庫主頁先揀 Core／M1／M2，再揀年份（Core 仲可以揀卷一或卷二），即刻開卷。",
)
FAQ_ENGLISH = (
    "有冇英文卷可以操？",
    "有。必修 Core 卷一卷二同延伸 M1／M2 都有英文卷，部分年份另有中文卷。每卷頁會標明語言。",
)
FAQ_PDF = (
    "可唔可以下載 PDF 原卷？",
    "站內主要提供題目索引同逐題睇題，方便溫習；部分卷另有 PDF 連結。內容以資料庫已有項目為準，並唔取代考評局官方刊物。",
)
FAQ_MOBILE = (
    "手機可唔可以睇題？",
    "可以。網站已為手機優化，亦支援加到主畫面，方便隨身搵 DSE past paper 同操卷。",
)
FAQ_SUBJECTS = (
    "呢個站係咪淨係數學？",
    "係，DSE 數學題庫專注數學一科：必修 Core（卷一／卷二）加延伸 M1、M2，非數學科目唔喺收錄範圍。",
)
FAQ_OFFICIAL = (
    "呢度係咪官方原卷檔案庫？",
    "站內主要提供索引、題目同課題標籤，方便溫習；部分卷另有 PDF 連結。內容以資料庫已有項目為準，並唔取代考試及評核局官方刊物。",
)
LANDING_FAQS = [FAQ_FREE, FAQ_TOPIC, FAQ_FIND_YEAR, FAQ_ENGLISH]
HUB_FAQS = [FAQ_FREE, FAQ_SUBJECTS, FAQ_TOPIC, FAQ_FIND_YEAR, FAQ_ENGLISH, FAQ_PDF, FAQ_MOBILE, FAQ_OFFICIAL]


def faq_ld_entities(pairs):
    return [
        {
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": a},
        }
        for q, a in pairs
    ]


def nav_pills(items, current=None, label="相關連結"):
    bits = [f'<nav class="strand-nav" aria-label="{esc(label)}">']
    for href, name, key in items:
        cls = ' class="on"' if current and key == current else ""
        bits.append(f'<a href="{esc(href)}"{cls}>{esc(name)}</a>')
    bits.append("</nav>")
    return "\n        ".join(bits)


def q_list_html(rows, topic=None, analyses=None, paper_path=None):
    items = []
    for q in rows:
        label = f"{q['subject']} {q['year']} {paper_zh_label(q.get('paper'))} Q{q['qno']}"
        title = (q.get("title") or "").strip()
        extra = f" — {esc(title)}" if title else ""
        badge = ""
        href = question_href(q, topic)
        akey = None
        if analyses is not None:
            akey = (q.get("subject"), q_year(q), paper_code_of(q.get("paper")), int(q.get("qno", -1)))
        if analyses and akey in analyses and paper_path and not topic:
            href = f"{paper_path}q{q['qno']}/"
            badge = '<span class="q-ai">AI 分析</span>'
        items.append(
            f'    <li><a href="{esc(href)}"><span class="q-meta">{esc(label)}</span>{extra}{badge}</a></li>'
        )
    return '<ul class="q-index">\n' + "\n".join(items) + "\n  </ul>"


def paper_code_of(paper):
    if paper in PAPER_CODE:
        return PAPER_CODE[paper]
    m = re.search(r"(\d+)\s*([A-Za-z])?", str(paper or ""))
    if not m:
        return "paper-1"
    code = "paper-" + m.group(1)
    if m.group(2):
        code += m.group(2).lower()
    return code


def paper_zh_label(paper):
    code = paper_code_of(paper)
    return PAPER_ZH.get(code, str(paper or "卷一"))


def infer_lang(file_name, fallback="中文"):
    f = file_name or ""
    if any(x in f for x in ("英文", "ENG", "(EN)", "English", "_EN", "-EN")):
        return "英文"
    if any(x in f for x in ("中文", "CHI", "(CHI)")):
        return "中文"
    return fallback


def paper_slug(code, lang):
    return f"{code}-en" if lang == "英文" else code


def paper_landing_path(sid, year, code, lang):
    return f"/{sid}/{year}/{paper_slug(code, lang)}/"


def year_path(sid, year):
    return f"/{sid}/{year}/"


def collect_papers(catalog, questions):
    """Merge catalog papers with bank papers. Language suffix: English gets -en, Chinese has no suffix."""
    q_index = {}
    for q in questions:
        sid = SUBJECT_TO_SID.get(q.get("subject"))
        if not sid:
            continue
        code = paper_code_of(q.get("paper"))
        lang = infer_lang(q.get("file") or "")
        key = (sid, str(q["year"]), code, lang)
        q_index.setdefault(key, []).append(q)

    papers = []
    seen = set()
    for r in catalog:
        sid = r["id"]
        code = paper_code_of(r["paper"])
        lang = r["lang"]
        key = (sid, str(r["year"]), code, lang)
        qs = sort_questions(q_index.get(key, []))
        if not qs:
            alts = [
                (lg, rows)
                for (s, y, c, lg), rows in q_index.items()
                if s == sid and y == str(r["year"]) and c == code
            ]
            # If the catalog language does not match the only bank language
            # (e.g. 2012/2013 卷二 marked 中文 but files are 英文卷), prefer the bank language
            # so we do not emit a hollow duplicate page.
            if len(alts) == 1:
                lang = alts[0][0]
                qs = sort_questions(alts[0][1])
        path = paper_landing_path(sid, r["year"], code, lang)
        papers.append(
            {
                "id": sid,
                "name": r["name"],
                "year": str(r["year"]),
                "paper": r["paper"] if r["paper"] in PAPER_ZH.values() else paper_zh_label(r["paper"]),
                "paper_code": code,
                "lang": lang,
                "hash": r["hash"],
                "path": path,
                "in_catalog": True,
                "questions": qs,
                "n_questions": len(qs),
            }
        )
        seen.add((sid, str(r["year"]), code, lang))

    # Bank-only papers (e.g. math 2014 Paper 2, chem 2025)
    default_name = {s["id"]: s["name"] for s in SUBJECTS}
    for key, qs in q_index.items():
        sid, year, code, lang = key
        if (sid, year, code, lang) in seen:
            continue
        qs = sort_questions(qs)
        if not qs:
            continue
        path = paper_landing_path(sid, year, code, lang)
        papers.append(
            {
                "id": sid,
                "name": default_name.get(sid, SID_TO_SUBJECT[sid]),
                "year": year,
                "paper": paper_zh_label(code),
                "paper_code": code,
                "lang": lang,
                "hash": hash_for_question(qs[0]),
                "path": path,
                "in_catalog": False,
                "questions": qs,
                "n_questions": len(qs),
            }
        )
        seen.add((sid, year, code, lang))
    papers.sort(key=lambda r: (r["id"], -year_sort_key(r["year"]), r["paper_code"], r["lang"]))
    return papers


def strand_nav_html(sid, current=None):
    bits = ['<nav class="strand-nav" aria-label="課題範疇">']
    for st in STRANDS:
        if st["subject_id"] != sid:
            continue
        cls = ' class="on"' if current == st["slug"] else ""
        bits.append(f'<a href="/{st["subject_id"]}/{st["slug"]}/"{cls}>{esc(st["name"])}</a>')
    bits.append("</nav>")
    return "\n        ".join(bits)


def _kw_empty_html(kw):
    return (
        '<section class="kw-block is-empty">\n'
        f"  <h3>{esc(kw)}</h3>\n"
        "  <p>呢個課題標籤暫時未有對應題目。</p>\n"
        "</section>"
    )


def _kw_match_html(kw, rows, sid, tag_counts=None):
    hub = hub_topic_path(sid, kw if not tag_counts or len(tag_counts) == 1 else None)
    topic_href = topic_url_for_name(sid, kw)
    items = []
    for q in rows[:SAMPLE_Q]:
        label = f"{q['subject']} {q['year']} Paper {paper_no(q['paper'])} Q{q['qno']}"
        title = (q.get("title") or "").strip()
        extra = f" — {esc(title)}" if title else ""
        items.append(
            f'    <li><a href="{esc(question_href(q, kw))}"><span class="q-meta">{esc(label)}</span>{extra}</a></li>'
        )
    links = []
    if topic_href:
        links.append(f'<a href="{esc(topic_href)}">開啟「{esc(kw)}」課題頁（{len(rows)} 題）</a>')
    if tag_counts and len(tag_counts) > 1:
        tag_bits = "、".join(
            f'<a href="{esc(hub_topic_path(sid, tag))}">{esc(tag)}</a>（{n}）'
            for tag, n in tag_counts
        )
        links.append("對應題目標籤：" + tag_bits)
    elif not topic_href:
        links.append(f'<a href="{esc(hub)}">喺 DSE 數學題庫 按課題查看全部 {len(rows)} 題</a>')
    else:
        links.append(f'<a href="{esc(hub_topic_path(sid, kw if not tag_counts else tag_counts[0][0]))}">喺 DSE 數學題庫 按課題篩選</a>')
    return (
        '<section class="kw-block">\n'
        f'  <h3>{esc(kw)} <span class="kw-count">{len(rows)} 題</span></h3>\n'
        + "".join(f"  <p>{x}</p>\n" for x in links)
        + '  <ul class="kw-qs">\n'
        + "\n".join(items)
        + "\n  </ul>\n</section>"
    )




def make_strand_pages(catalog, questions, topics):
    zeros = []
    for st in STRANDS:
        s = subject_meta(st["subject_id"])
        keywords = topics[st["subject_id"]][st["name"]]
        blocks = []
        listed_items = []
        matched_qs = {}
        for kw in keywords:
            used_tags = tags_for_keyword(kw)
            rows = sort_questions(questions_for_keyword(questions, st["subject_id"], kw))
            if not rows:
                zeros.append((st["subject_id"], st["name"], kw))
                blocks.append(_kw_empty_html(kw))
                continue
            matched_qs[kw] = rows
            tag_counts = []
            for tag in used_tags:
                n = len(questions_for_tag(questions, st["subject_id"], tag))
                if n:
                    tag_counts.append((tag, n))
            landing = topic_url_for_name(st["subject_id"], kw)
            listed_items.append(
                {
                    "@type": "ListItem",
                    "position": len(listed_items) + 1,
                    "name": f"{kw}（{len(rows)} 題）",
                    "url": SITE + (landing or hub_topic_path(st["subject_id"], kw)),
                }
            )
            blocks.append(_kw_match_html(kw, rows, st["subject_id"], tag_counts))
        union = []
        seen = set()
        for rows in matched_qs.values():
            for q in rows:
                key = (q.get("subject"), q.get("year"), q.get("paper"), q.get("qno"))
                if key in seen:
                    continue
                seen.add(key)
                union.append(q)
        url = f"{SITE}/{st['subject_id']}/{st['slug']}/"
        subj_url = f"{SITE}/{st['subject_id']}/"
        add_sitemap(url, "0.8", "weekly")
        unmatched = len(keywords) - len(matched_qs)
        tagline = (
            f"{st['blurb']} 想集中溫習 DSE {s['short']}「{st['name']}」past paper，"
            f"呢頁已按課題整理。資料庫入面，呢個範疇有 {len(union)} 題對應 "
            f"{len(matched_qs)} 個課題標籤"
        )
        tagline += f"，另有 {unmatched} 個課題暫時未有對應題目。" if unmatched else "。"
        strand_years = sorted({q_year(q) for q in union}, key=year_sort_key, reverse=True)
        year_nav = (
            nav_pills(
                [(year_path(st["subject_id"], y), str(y), y) for y in strand_years],
                label="年份",
            )
            if strand_years
            else ""
        )
        topic_landings = [
            (topic_path(tp["subject_id"], tp["slug"]), tp["name"], tp["slug"])
            for tp in TOPIC_PAGES
            if tp["subject_id"] == st["subject_id"] and tp.get("strand") == st["slug"]
        ]
        topic_nav = nav_pills(topic_landings, label="課題頁") if topic_landings else ""
        graph = {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "BreadcrumbList",
                    "itemListElement": [
                        {"@type": "ListItem", "position": 1, "name": "DSE 數學題庫", "item": HUB},
                        {"@type": "ListItem", "position": 2, "name": s["short"], "item": subj_url},
                        {"@type": "ListItem", "position": 3, "name": st["name"], "item": url},
                    ],
                },
                {
                    "@type": "CollectionPage",
                    "name": st["title"],
                    "description": st["description"],
                    "url": url,
                    "inLanguage": "zh-Hant-HK",
                    "isPartOf": {"@id": f"{SITE}/#website"},
                    "about": {"@type": "Thing", "name": f"香港中學文憑 {s['name']} {st['name']}"},
                    "mainEntity": {
                        "@type": "ItemList",
                        "name": f"DSE {s['short']} {st['name']} 課題",
                        "numberOfItems": len(listed_items) or len(keywords),
                        "itemListElement": listed_items
                        or [
                            {
                                "@type": "ListItem",
                                "position": i,
                                "name": kw,
                                "url": url,
                            }
                            for i, kw in enumerate(keywords, 1)
                        ],
                    },
                },
                {
                    "@type": "FAQPage",
                    "mainEntity": faq_ld_entities(LANDING_FAQS),
                },
            ],
        }
        siblings = " · ".join(
            f'<a href="/{x["subject_id"]}/{x["slug"]}/">{esc(x["name"])}</a>'
            for x in STRANDS
            if x["subject_id"] == st["subject_id"]
        )
        _strand_guide = topic_guide_html(st.get("guide"))
        if not _strand_guide:
            raise SystemExit(f"missing strand guide: {st['subject_id']} {st['name']}")
        page = "\n".join(
            [
                "<!DOCTYPE html>",
                '<html lang="zh-Hant-HK">',
                "<head>",
                seo_head(st["title"], st["description"], url),
                ld_json(graph),
                "</head>",
                '<body class="subj-page topic-page">',
                '<header class="hero">',
                '  <div class="hero-glow" aria-hidden="true"></div>',
                '  <div class="hero-inner">',
                '    <nav class="crumb" aria-label="麵包屑">',
                '      <a href="/hub/">DSE 數學題庫</a>',
                '      <span aria-hidden="true">／</span>',
                f'      <a href="/{st["subject_id"]}/">{esc(s["short"])}</a>',
                '      <span aria-hidden="true">／</span>',
                f"      <span>{esc(st['name'])}</span>",
                "    </nav>",
                '    <p class="brand">DSE 數學題庫</p>',
                f"    <h1>{esc(st['h1'])}</h1>",
                f'    <p class="tagline">{esc(tagline)}</p>',
                f"        {subject_nav(catalog, current=st['subject_id'])}",
                f"        {strand_nav_html(st['subject_id'], current=st['slug'])}",
                f"        {year_nav}" if year_nav else "",
                f"        {topic_nav}" if topic_nav else "",
                (
                    f'<p class="page-cta"><a href="{esc(hub_topic_path(st["subject_id"]))}">按課題篩選{esc(s["short"])}題目</a>'
                    f' · <a href="/{st["subject_id"]}/">返回{esc(s["short"])}科目頁</a>'
                    f' · <a href="/hub/?subject={st["subject_id"]}&amp;mode=year">按年份睇卷</a></p>'
                ),
                "  </div>",
                "</header>",
                '<main class="subj-main">',
                _strand_guide,
                '<section class="kw-section" aria-label="課題">',
                f"  <h2>{esc(st['name'])}課題</h2>",
                "\n".join(blocks),
                "</section>",
                (
                    f'<section class="strand-index" aria-label="出現年份">\n  <h2>出現年份</h2>\n  {year_nav}\n</section>'
                    if year_nav
                    else ""
                ),
                faq_block(LANDING_FAQS),
                "</main>",
                site_footer(f'<a href="/{st["subject_id"]}/">返回{esc(s["short"])}科目頁</a> · 同科範疇：{siblings}'),
                "</body>",
                "</html>",
                "",
            ]
        )
        dest = ROOT / st["subject_id"] / st["slug"]
        dest.mkdir(parents=True, exist_ok=True)
        (dest / "index.html").write_text(page, encoding="utf-8")
        print(
            "strand",
            f"/{st['subject_id']}/{st['slug']}/",
            "matched",
            len(matched_qs),
            "of",
            len(keywords),
            "qs",
            len(union),
        )
    if zeros:
        print("zero-match keywords:")
        for sid, strand, kw in zeros:
            print(f"  {sid} / {strand} / {kw}")
    else:
        print("zero-match keywords: none")
    return zeros


def topic_nav_html(sid, current=None):
    items = [
        (topic_path(tp["subject_id"], tp["slug"]), tp["name"], tp["slug"])
        for tp in TOPIC_PAGES
        if tp["subject_id"] == sid
    ]
    if not items:
        return ""
    return nav_pills(items, current=current, label="課題")


def year_nav_html(papers, sid, current=None):
    years = sorted({p["year"] for p in papers if p["id"] == sid}, reverse=True)
    return nav_pills(
        [(year_path(sid, y), str(y), y) for y in years],
        current=current,
        label="年份",
    )


def topic_hits_for_questions(sid, question_rows):
    """Topic landing links that match tags in the given question set."""
    hits = []
    for tp in TOPIC_PAGES:
        if tp["subject_id"] != sid:
            continue
        n = len(
            [
                q
                for q in question_rows
                if set(q.get("tags") or []) & set(tp["tags"])
            ]
        )
        if n:
            hits.append(
                (topic_path(sid, tp["slug"]), f"{tp['name']}（{n}）", tp["slug"])
            )
    return hits


def related_papers_for_years(papers, sid, years, limit=12):
    year_set = set(years)
    rows = [
        p
        for p in papers
        if p["id"] == sid and p["year"] in year_set
    ]
    rows = sorted(rows, key=lambda r: (-year_sort_key(r["year"]), r["paper_code"], r["lang"]))
    items = [
        (p["path"], f"{p['year']} {p['paper']}（{p['lang']}）", p["path"])
        for p in rows[:limit]
    ]
    if not items:
        return ""
    return (
        '<section class="strand-index" aria-label="相關年份卷">\n'
        "  <h2>相關年份卷</h2>\n  "
        + nav_pills(items, label="相關年份卷")
        + "\n</section>"
    )


def write_landing(
    path,
    title,
    description,
    canonical,
    graph,
    body_inner,
    footer_extra="",
    lang="zh-Hant-HK",
    og_locale="zh_HK",
    alternates=None,
    og_image=None,
    body_attrs="",
    extra_head="",
):
    page = (
        "<!DOCTYPE html>\n"
        f'<html lang="{esc(lang)}">\n'
        "<head>\n"
        f"{seo_head(title, description, canonical, lang=lang, og_locale=og_locale, alternates=alternates, og_image=og_image)}\n"
        f"{extra_head}\n"
        f"{ld_json(graph)}\n"
        "</head>\n"
        f'<body class="subj-page"{(" " + body_attrs) if body_attrs else ""}>\n'
        f"{body_inner}\n"
        f"{site_footer(footer_extra)}\n"
        "</body>\n"
        "</html>\n"
    )
    dest = ROOT / path.lstrip("/")
    if path.endswith("/"):
        dest = dest
        dest.mkdir(parents=True, exist_ok=True)
        out = dest / "index.html"
    else:
        dest.parent.mkdir(parents=True, exist_ok=True)
        out = dest
    out.write_text(page, encoding="utf-8")
    return out


def hero_html(crumbs, h1, tagline, catalog, sid, extra_nav="", cta=""):
    return (
        '<header class="hero">\n'
        '  <div class="hero-glow" aria-hidden="true"></div>\n'
        '  <div class="hero-inner">\n'
        f"    {crumb_html(crumbs)}\n"
        '    <p class="brand">DSE 數學題庫</p>\n'
        f"    <h1>{esc(h1)}</h1>\n"
        f'    <p class="tagline">{tagline}</p>\n'
        f"        {subject_nav(catalog, current=sid)}\n"
        f"        {extra_nav}\n"
        f"    {cta}\n"
        "  </div>\n"
        "</header>\n"
    )


def make_year_pages(catalog, papers, questions):
    by = defaultdict(list)
    for p in papers:
        by[(p["id"], str(p["year"]))].append(p)
    # Also include years that only appear in the question bank
    for q in questions:
        sid = SUBJECT_TO_SID.get(q.get("subject"))
        if sid:
            by.setdefault((sid, str(q["year"])), [])
    count = 0
    for (sid, year), rows in sorted(by.items(), key=lambda x: (x[0][0], -year_sort_key(x[0][1]))):
        rows = sort_rows(rows)
        s = subject_meta(sid)
        # questions that year
        yqs = [
            q
            for q in questions
            if q.get("subject") == SID_TO_SUBJECT[sid] and str(q["year"]) == str(year)
        ]
        if not rows and not yqs:
            continue
        path = year_path(sid, year)
        url = SITE + path
        n_papers = len(rows)
        n_qs = len(yqs)
        title = f"免費 DSE {s['short']} {year} 歷屆試題｜DSE 數學題庫"
        desc = (
            f"免費查閱 DSE {s['short']} {year} 年歷屆試題"
            + (f"，資料庫有 {n_papers} 卷" if n_papers else "")
            + (f"、{n_qs} 題索引" if n_qs else "")
            + "。真正完全免費，可按卷或課題操練。"
        )
        h1 = f"DSE {s['short']} {year} 歷屆試題"
        paper_bits = "、".join(f"{r['paper']}（{r['lang']}）" for r in rows) if rows else "相關題目"
        tagline = (
            f"免費 DSE {esc(s['short'])} {year} past paper："
            + (f"包括 {esc(paper_bits)}" if rows else "相關題目")
            + (f"。而家資料庫有 {n_qs} 題索引，可按卷或課題操練。" if n_qs else "。真正完全免費查閱。")
        )
        hub_link = f"/hub/?subject={sid}&amp;mode=year&amp;year={year}"
        cta = (
            f'<p class="page-cta"><a href="{hub_link}">喺 DSE 數學題庫 按年份睇 {year} 年卷</a>'
            f' · <a href="/{sid}/">返回{esc(s["short"])}科目頁</a>'
            f' · <a href="/hub/?subject={sid}&amp;mode=topic">按課題溫習</a></p>'
        )
        sibling_years = year_nav_html(papers, sid, current=year)
        sections = []
        if rows:
            items = "\n".join(paper_row_html(r) for r in rows)
            sections.append(
                f'<section class="year-group">\n  <h2>{year} 年各卷</h2>\n  <div class="paper-list">\n{items}\n  </div>\n</section>'
            )
        topic_hits = topic_hits_for_questions(sid, yqs)
        if topic_hits:
            sections.append(
                '<section class="strand-index" aria-label="本年相關課題">\n'
                "  <h2>本年相關課題</h2>\n  "
                + nav_pills(topic_hits, label="本年課題")
                + "\n</section>"
            )
        strand_links = [
            (f"/{st['subject_id']}/{st['slug']}/", st["name"], st["slug"])
            for st in STRANDS
            if st["subject_id"] == sid
        ]
        extra_nav = sibling_years
        if strand_links:
            extra_nav += "\n        " + nav_pills(strand_links, label="課題範疇")
        if topic_hits:
            # Keep a compact topic strip in the hero so year ↔ topic is obvious.
            extra_nav += "\n        " + nav_pills(topic_hits[:10], label="本年課題")
        crumbs = [("/hub/", "DSE 數學題庫"), (f"/{sid}/", s["short"]), (None, str(year))]
        graph = {
            "@context": "https://schema.org",
            "@graph": [
                ld_breadcrumb([("/hub/", "DSE 數學題庫"), (f"/{sid}/", s["short"]), (url, str(year))]),
                {
                    "@type": "CollectionPage",
                    "name": title,
                    "description": desc,
                    "url": url,
                    "inLanguage": "zh-Hant-HK",
                    "isPartOf": {"@id": f"{SITE}/#website"},
                    "about": {"@type": "Thing", "name": f"香港中學文憑 {s['name']} {year}"},
                    "mainEntity": {
                        "@type": "ItemList",
                        "name": f"DSE {s['short']} {year} 試卷",
                        "numberOfItems": n_papers or n_qs,
                        "itemListElement": [
                            {
                                "@type": "ListItem",
                                "position": i,
                                "name": f"{r['year']} {r['paper']}（{r['lang']}）",
                                "url": SITE + r["path"],
                            }
                            for i, r in enumerate(rows, 1)
                        ]
                        or [
                            {
                                "@type": "ListItem",
                                "position": 1,
                                "name": f"DSE {s['short']} {year}",
                                "url": url,
                            }
                        ],
                    },
                },
                {
                    "@type": "FAQPage",
                    "mainEntity": faq_ld_entities(LANDING_FAQS),
                },
            ],
        }
        body = hero_html(crumbs, h1, tagline, catalog, sid, extra_nav=extra_nav, cta=cta)
        body += '<main class="subj-main">\n' + "\n".join(sections) + "\n" + faq_block(LANDING_FAQS) + "\n</main>"
        write_landing(path, title, desc, url, graph, body, footer_extra=f'<a href="/{sid}/">返回{esc(s["short"])}科目頁</a>')
        add_sitemap(url, "0.8", "weekly")
        count += 1
        print("year", path, "papers", n_papers, "qs", n_qs)
    print("year pages", count)
    return count


def make_paper_pages(catalog, papers, questions, analyses=None):
    count = 0
    by_year = defaultdict(list)
    for p in papers:
        by_year[(p["id"], p["year"])].append(p)
    for r in papers:
        s = subject_meta(r["id"])
        path = r["path"]
        url = SITE + path
        qs = r["questions"]
        nq = len(qs)
        title = f"免費 DSE {s['short']} {r['year']} {r['paper']}（{r['lang']}）歷屆試題｜DSE 數學題庫"
        desc = (
            f"免費查閱 DSE {s['short']} {r['year']} 年{r['paper']}（{r['lang']}）歷屆試題"
            + (f"，資料庫有 {nq} 題索引，可逐題開啟。" if nq else "。可喺 DSE 數學題庫 開啟呢份卷。")
            + "真正完全免費。"
        )
        h1 = f"DSE {s['short']} {r['year']} {r['paper']}（{r['lang']}）"
        tagline = (
            f"真正完全免費查閱 DSE {esc(s['short'])} {r['year']} 年{esc(r['paper'])}（{esc(r['lang'])}）"
            + (f"。資料庫有 {nq} 題索引。" if nq else "。逐題索引稍後再補，你仍然可以喺題庫開啟呢份卷。")
        )
        open_href = paper_href(r)
        hub_qs = f"/hub/?subject={r['id']}&amp;mode=year&amp;year={r['year']}&amp;paper={quote(r['paper'], safe='')}"
        year_href = year_path(r["id"], r["year"])
        cta = (
            f'<p class="page-cta open-cta"><a href="{esc(open_href)}">喺題庫開啟呢份卷</a>'
            f' · <a href="{esc(year_href)}">返回 {r["year"]} 年頁</a>'
            f' · <a href="/{r["id"]}/">返回{esc(s["short"])}科目頁</a>'
            f' · <a href="{hub_qs}">喺 DSE 數學題庫 篩選呢一年</a></p>'
        )
        siblings = [
            (p["path"], f"{p['paper']}（{p['lang']}）", p["path"])
            for p in sort_rows(by_year[(r["id"], r["year"])])
        ]
        extra_nav = year_nav_html(papers, r["id"], current=r["year"])
        if siblings:
            extra_nav += "\n        " + nav_pills(siblings, current=r["path"], label="同年試卷")
        paper_topics = topic_hits_for_questions(r["id"], qs)
        if paper_topics:
            extra_nav += "\n        " + nav_pills(paper_topics[:8], label="相關課題")
        crumbs = [
            ("/hub/", "DSE 數學題庫"),
            (f"/{r['id']}/", s["short"]),
            (year_path(r["id"], r["year"]), str(r["year"])),
            (None, f"{r['paper']}（{r['lang']}）"),
        ]
        sections = []
        if nq:
            sections.append(
                f'<section class="kw-section" aria-label="題目索引">\n  <h2>題目索引（{nq} 題）</h2>\n  '
                + q_list_html(qs, analyses=analyses, paper_path=path)
                + "\n</section>"
            )
        else:
            sections.append(
                '<section class="kw-block">\n  <h2>題目索引</h2>\n'
                "  <p>呢份卷已收錄喺資料庫目錄，可以喺題庫開啟；逐題索引稍後再補。</p>\n"
                f'  <p><a href="{esc(open_href)}">開啟 {esc(s["short"])} {r["year"]} {esc(r["paper"])}</a></p>\n'
                "</section>"
            )
        if paper_topics:
            sections.append(
                '<section class="strand-index" aria-label="相關課題">\n'
                "  <h2>呢份卷相關課題</h2>\n  "
                + nav_pills(paper_topics, label="相關課題")
                + "\n</section>"
            )
        graph = {
            "@context": "https://schema.org",
            "@graph": [
                ld_breadcrumb(
                    [
                        ("/hub/", "DSE 數學題庫"),
                        (f"/{r['id']}/", s["short"]),
                        (year_path(r["id"], r["year"]), str(r["year"])),
                        (url, f"{r['paper']}（{r['lang']}）"),
                    ]
                ),
                {
                    "@type": "CollectionPage",
                    "name": title,
                    "description": desc,
                    "url": url,
                    "inLanguage": "zh-Hant-HK",
                    "isPartOf": {"@id": f"{SITE}/#website"},
                    "about": {
                        "@type": "Thing",
                        "name": f"香港中學文憑 {s['name']} {r['year']} {r['paper']}",
                    },
                    "mainEntity": {
                        "@type": "ItemList",
                        "name": f"DSE {s['short']} {r['year']} {r['paper']} 題目",
                        "numberOfItems": nq or 1,
                        "itemListElement": [
                            {
                                "@type": "ListItem",
                                "position": i,
                                "name": f"{q['subject']} {q['year']} {paper_zh_label(q.get('paper'))} Q{q['qno']}",
                                "url": question_href(q),
                            }
                            for i, q in enumerate(qs, 1)
                        ]
                        or [
                            {
                                "@type": "ListItem",
                                "position": 1,
                                "name": f"{s['short']} {r['year']} {r['paper']}",
                                "url": open_href,
                            }
                        ],
                    },
                },
            ],
        }
        body = hero_html(crumbs, h1, tagline, catalog, r["id"], extra_nav=extra_nav, cta=cta)
        body += '<main class="subj-main">\n' + "\n".join(sections) + "\n</main>"
        write_landing(
            path,
            title,
            desc,
            url,
            graph,
            body,
            footer_extra=f'<a href="{year_path(r["id"], r["year"])}">返回 {r["year"]} 年</a> · <a href="/{r["id"]}/">返回{esc(s["short"])}科目頁</a>',
        )
        add_sitemap(url, "0.7", "weekly")
        count += 1
        print("paper", path, "qs", nq, "catalog" if r["in_catalog"] else "bank-only")
    print("paper pages", count)
    return count


def _embed_question_html(q):
    """data.js 嘅 html img src 係 docs 根相對路徑；子頁面要用絕對路徑先搵到圖。"""
    html = q.get("html") or ""
    return re.sub(r'(src=")(?!/|https?://)', r"\1/", html)


def share_row_html(url, text, lang="zh"):
    # WhatsApp／Telegram 分享＋複製連結；click 事件由 /js/track.js 報 share_click／copy_link。
    q_url = quote(url, safe="")
    q_txt = quote(text, safe="")
    if lang == "en":
        aria, l_wa, l_tg, l_copy = "Share this question", "Share on WhatsApp", "Share on Telegram", "Copy link"
    else:
        aria, l_wa, l_tg, l_copy = "分享呢一題", "WhatsApp 分享", "Telegram 分享", "複製連結"
    return (
        f'<nav class="share-row" aria-label="{aria}">'
        f'<a data-share="whatsapp" href="https://wa.me/?text={q_txt}%20{q_url}" rel="noopener" target="_blank">{l_wa}</a>'
        f'<a data-share="telegram" href="https://t.me/share/url?url={q_url}&amp;text={q_txt}" rel="noopener" target="_blank">{l_tg}</a>'
        f'<button type="button" data-copy-link="{esc(url)}">{l_copy}</button>'
        "</nav>"
    )


def _analysis_section_html(analysis):
    a = analysis.get("analysis") or {}
    md = a.get("metadata") or {}
    oa = a.get("options_analysis") or {}
    cat_zh = {
        "Conceptual": "概念錯誤",
        "Calculation": "計算粗心",
        "Reading-Formatting": "審題不清",
        "Methodological": "策略錯誤",
    }
    chips = []
    if md.get("primary_topic"):
        chips.append(f'<span class="q-ai">{esc(md["primary_topic"])}</span>')
    if md.get("bloom_taxonomy_level"):
        chips.append(f"認知層次：{esc(str(md['bloom_taxonomy_level']))}")
    if md.get("estimated_time_seconds"):
        chips.append(f"建議作答 {esc(str(md['estimated_time_seconds']))} 秒")
    hint_items = []
    hints = [h for h in (a.get("scaffolding_hints") or []) if isinstance(h, str) and h.strip()]
    labels = ("提示 1（啟發）", "提示 2（知識）", "提示 3（破題）")
    for i, h in enumerate(hints[:3]):
        hint_items.append(
            f'<details class="ai-hint"><summary>{labels[i]}</summary><div>{esc(h)}</div></details>'
        )
    rows = []
    for L in "ABCD":
        v = oa.get(L)
        if not isinstance(v, dict):
            continue
        if v.get("is_correct") is True:
            head = f'<strong>{L}　✓ 正確答案</strong>'
            bits = ""
        else:
            head = f"<strong>{L}</strong>"
            bits = []
            if v.get("error_category"):
                bits.append(f'<span class="q-ai">{esc(cat_zh.get(v["error_category"], v["error_category"]))}</span>')
            if v.get("error_tag"):
                bits.append(esc(v["error_tag"]))
            bits = f'<p class="ai-oa-meta">{"　".join(bits)}</p>' if bits else ""
        thought = v.get("student_thought_process") or ""
        rows.append(f'<div class="ai-oa-card">{head}{bits}<div>{esc(thought)}</div></div>')
    strategy = ""
    if a.get("quick_solution_strategy"):
        strategy = f'<p class="ai-strategy"><strong>速解策略：</strong>{esc(a["quick_solution_strategy"])}</p>'
    formulas = ""
    if md.get("required_formulas"):
        fs = "、".join(esc(str(x)) for x in md["required_formulas"])
        formulas = f'<p>核心公式／定理：{fs}</p>'
    return (
        '<section class="kw-section" aria-label="深度分析">\n  <h2>深度分析</h2>\n'
        + (f'<p class="ai-chips">{"　".join(chips)}</p>' if chips else "")
        + formulas
        + (f'<div class="ai-hints">{"".join(hint_items)}</div>' if hint_items else "")
        + ('<h3>誘答項逆向工程</h3><div class="ai-oa">' + "".join(rows) + "</div>" if rows else "")
        + strategy
        + "\n</section>"
    )


def _qpage_graph(sid, s, akey, url, paper_row, qno, name, qtext, answers, accepted, lang_code, topic):
    """QAPage + LearningResource + Breadcrumb（zh/en 兩版共用）。"""
    crumbs = [
        ("/hub/", "DSE 數學題庫"),
        (f"/{sid}/", s["short"] if lang_code == "zh-Hant-HK" else s["en"]),
        (year_path(sid, akey[1]), akey[1]),
        (SITE + paper_row["path"], f"{paper_row['paper']}（{paper_row['lang']}）"),
        (url, f"第 {qno} 題" if lang_code == "zh-Hant-HK" else f"Question {qno}"),
    ]
    main_entity = {
        "@type": "Question",
        "name": name,
        "text": qtext,
        "answerCount": len(answers),
        "acceptedAnswer": {"@type": "Answer", "text": accepted},
    }
    if answers:
        main_entity["suggestedAnswer"] = answers
    graph_items = [ld_breadcrumb(crumbs), {"@type": "QAPage", "mainEntity": main_entity}]
    lr = {
        "@type": "LearningResource",
        "name": name,
        "url": url,
        "inLanguage": lang_code,
        "learningResourceType": "Exam question",
        "educationalLevel": "HKDSE",
        "isPartOf": {"@id": f"{SITE}/#website"},
    }
    if topic:
        lr["about"] = topic
        lr["teaches"] = topic
    graph_items.append(lr)
    return {"@context": "https://schema.org", "@graph": graph_items}


def _term(text):
    """選項文字收一個句尾（避免「。。」）。"""
    return re.sub(r"[。．.]+$", "", str(text or "")).strip()


def _clean_text(t):
    return re.sub(r"\s+", " ", strip_latex_delims(t)).strip()


def make_question_pages(catalog, papers, questions, analyses):
    """每題有分析 JSON 就出一頁 /<sid>/<year>/<paper-code>/q<qno>/；有英文題目記錄另出 -en twin（真英文內容）。"""
    if not analyses:
        print("question pages 0")
        return 0
    by_paper = defaultdict(list)
    for r in papers:
        by_paper[(r["id"], str(r["year"]), r["paper_code"])].append(r)
    # 同一題嘅中英文記錄收埋一組（analysis JSON 冇英文欄位，分析一律中文版）
    grouped = {}
    for q in sort_questions(questions):
        try:
            akey = (q.get("subject"), q_year(q), paper_code_of(q.get("paper")), int(q.get("qno", -1)))
        except ValueError:
            continue
        if akey not in analyses:
            continue
        if not SUBJECT_TO_SID.get(q.get("subject")):
            continue
        g = grouped.setdefault(akey, {"zh": None, "en": None})
        if infer_lang(q.get("file") or "") == "英文":
            if g["en"] is None:
                g["en"] = q
        elif g["zh"] is None:
            g["zh"] = q
    # prev/next 用：同一卷入面有頁嘅題號
    qnos_by_paper = defaultdict(list)
    for akey in grouped:
        qnos_by_paper[akey[:3]].append(akey[3])
    for v in qnos_by_paper.values():
        v.sort()

    en_short = {"math": "Maths", "econ": "Economics", "chem": "Chemistry", "bio": "Biology", "phys": "Physics"}
    tmap, tcounts = legacy_topic_counts(questions)

    def paper_row_for(sid, year, code, lang):
        rows = by_paper.get((sid, year, code)) or []
        hit = next((x for x in rows if x["lang"] == lang), None)
        return hit or (rows[0] if rows else None)

    count = 0
    zh_url_by_key = {}
    for akey in sorted(grouped, key=lambda k: (k[0], -year_sort_key(k[1]), k[2], k[3])):
        subj_name, year, code, qno = akey
        sid = SUBJECT_TO_SID[subj_name]
        g = grouped[akey]
        s = subject_meta(sid)
        a = analyses[akey].get("analysis") or {}
        md = a.get("metadata") or {}
        topic = md.get("primary_topic") or ""
        oa = a.get("options_analysis") or {}
        correct_letter = next((L for L in "ABCD" if isinstance(oa.get(L), dict) and oa[L].get("is_correct")), None)
        strategy_txt = str(a.get("quick_solution_strategy") or "")
        prev_q = next((n for n in reversed(qnos_by_paper[akey[:3]]) if n < qno), None)
        next_q = next((n for n in qnos_by_paper[akey[:3]] if n > qno), None)

        def prevnext_html(path_fmt):
            bits = []
            if prev_q is not None:
                bits.append(f'<a href="{esc(path_fmt.format(prev_q))}" rel="prev">← Q{prev_q}</a>')
            if next_q is not None:
                bits.append(f'<a href="{esc(path_fmt.format(next_q))}" rel="next">Q{next_q} →</a>')
            return '<nav class="q-prevnext" aria-label="上一題／下一題">' + "　".join(bits) + "</nav>" if bits else ""

        # ---- 中文頁（主體）----
        qzh_q = g["zh"]
        zh_row = paper_row_for(sid, year, code, "中文") or paper_row_for(sid, year, code, "英文")
        if qzh_q is not None and zh_row is not None:
            zh_path = f"{zh_row['path']}q{qno}/"
            zh_url = SITE + zh_path
            zh_url_by_key[akey] = zh_url
            qzh = paper_zh_label(code)
            tt = f"【{topic}】" if topic else ""
            title = f"DSE {s['short']} {year} {qzh} 第 {qno} 題{tt}深度分析＋答案｜DSE 數學題庫"
            desc = (
                f"DSE {s['short']} {year} {qzh} 第 {qno} 題深度解析：考點"
                + (f"「{topic}」" if topic else "")
                + "、三層解題提示、每個錯誤選項嘅思考盲點逆向工程同速解策略，附正確答案。"
            )
            h1 = f"DSE {s['short']} {year} {qzh} 第 {qno} 題{tt}深度分析"
            tagline = "考點圖譜 · 布魯姆認知層次 · 三層鷹架提示 · 誘答項逆向工程"
            bank_href = question_href(qzh_q)
            crumbs = [
                ("/hub/", "DSE 數學題庫"),
                (f"/{sid}/", s["short"]),
                (year_path(sid, year), year),
                (zh_row["path"], f"{zh_row['paper']}（{zh_row['lang']}）"),
                (None, f"第 {qno} 題"),
            ]
            topic_link = ""
            tp = topic_page_for_name(sid, topic) if topic else None
            if tp is not None:
                n_tp = topic_question_count(questions, sid, tp)
                tp_url = topic_path(sid, tp["slug"])
                topic_link = f' · <a href="{esc(tp_url)}">所屬課題：{esc(topic)}（{n_tp} 題）</a>'
            # 題目 tag → 舊細粒度課題頁（/topics/<slug>/，144 頁長尾資產）嘅 spoke→hub 內鏈
            for t_label, t_slug, n_q in question_topic_chips(qzh_q, tmap, tcounts):
                topic_link += f' · <a href="/topics/{esc(t_slug)}/">課題：{esc(t_label)}（{n_q} 題）</a>'
            en_twin_link = ""
            if g["en"] is not None and EMIT_EN_PAGES:
                en_twin_link = f' · <a href="{esc(zh_row["path"].rstrip("/"))}-en/q{qno}/">English version</a>'
            cta = (
                f'<p class="page-cta open-cta"><a href="{esc(bank_href)}">喺題庫開啟呢題</a>'
                f' · <a href="{esc(zh_row["path"])}">返回 {year} {esc(qzh)} 全卷</a>'
                + en_twin_link
                + topic_link
                + "</p>"
            )
            sections = [
                '<section class="kw-block" aria-label="題目">\n  <h2>題目</h2>\n'
                f'  <div class="q-embed">{_embed_question_html(qzh_q)}</div>\n</section>',
                share_row_html(zh_url, f"DSE {s['short']} {year} {qzh} 第 {qno} 題" + (f"【{topic}】" if topic else "")),
                _analysis_section_html(analyses[akey]),
            ]
            pn = prevnext_html(zh_row["path"] + "q{}/")
            if pn:
                sections.append(pn)
            opts = dict(re.findall(r"^-\s*([A-D])[.．、]\s*(.+)$", str(qzh_q.get("text") or ""), re.M))
            opts = {k: _clean_text(v) for k, v in opts.items()}
            answers = [{"@type": "Answer", "text": f"{L}. {_term(opts[L])}"} for L in "ABCD" if L in opts]
            qtext = _clean_text(qzh_q.get("text"))[:500]
            if correct_letter and correct_letter in opts:
                accepted = f"{correct_letter}. {_term(opts[correct_letter])}。速解策略：{_term(_clean_text(strategy_txt))}。"
            else:
                accepted = (_term(_clean_text(strategy_txt)) + "。") if strategy_txt else ""
            name = f"DSE {s['short']} {year} {qzh} 第 {qno} 題"
            graph = _qpage_graph(sid, s, akey, zh_url, zh_row, qno, name, qtext, answers, accepted, "zh-Hant-HK", topic)
            body = hero_html(crumbs, h1, tagline, catalog, sid, cta=cta)
            body += '<main class="subj-main">\n' + "\n".join(sections) + "\n</main>"
            en_alt = f"{SITE}{zh_row['path'].rstrip('/')}-en/q{qno}/" if g["en"] is not None and EMIT_EN_PAGES else None
            alternates = ([("zh-Hant-HK", zh_url), ("en", en_alt), ("x-default", zh_url)] if en_alt else None)
            og_url = question_og_url(sid, year, code, qno)
            make_question_og(
                sid, year, code, qno,
                subject_short=s["short"], paper_label=qzh, topic=topic, marks=md.get("marks"),
            )
            write_landing(
                zh_path,
                title,
                desc,
                zh_url,
                graph,
                body,
                footer_extra=f'<a href="{esc(zh_row["path"])}">返回 {year} {esc(qzh)}</a> · <a href="{esc(bank_href)}">喺題庫開啟呢題</a>',
                alternates=alternates,
                og_image=og_url,
                body_attrs=f'data-qpage data-topic="{esc(topic)}" data-year="{esc(str(year))}" data-paper="{esc(str(code))}" data-qno="{esc(str(qno))}" data-lang="zh"',
            )
            add_sitemap(zh_url, "0.8", "monthly")
            FEED_ITEMS.append((str(analyses[akey].get("generated") or ""), title, zh_url))
            count += 1

        # ---- 英文 twin（真英文內容：題目／選項用英文記錄；中文深度分析收摺）----
        qen_q = g["en"]
        if qen_q is None or not EMIT_EN_PAGES:
            continue
        en_row = paper_row_for(sid, year, code, "英文")
        if en_row is None:
            print("en twin skipped (no en paper row)", akey)
            continue
        en_path = f"{en_row['path']}q{qno}/"
        en_url = SITE + en_path
        if zh_url_by_key.get(akey) == en_url:
            # zh 頁已寫喺同一路徑（中英文卷無分路徑），唔好覆寫
            print("en twin skipped (same path as zh page)", akey)
            continue
        pl = paper_en_label(code)
        subj_en = en_short.get(sid, s["en"])
        title = (
            f"DSE {subj_en} {year} {pl} Question {qno}"
            + (f" — {topic}" if topic else "")
            + " — Answer, Traps & Speed Solution | DSE 數學題庫"
        )
        desc = (
            f"Free worked answer for DSE {subj_en} {year} {pl} Question {qno}: the correct answer,"
            " why each wrong option traps candidates, and a fast solving strategy."
            + (f" Topic: {topic}." if topic else "")
        )
        h1 = f"DSE {subj_en} {year} {pl} Question {qno}"
        tagline = "Correct answer · Option traps · Speed strategy · Detailed analysis in Chinese"
        bank_href = question_href(qen_q)
        crumbs = [
            ("/hub/", "DSE 數學題庫"),
            (f"/{sid}/", subj_en),
            (year_path(sid, year), year),
            (en_row["path"], f"{pl} (English)"),
            (None, f"Question {qno}"),
        ]
        zh_link = zh_url_by_key.get(akey)
        topic_link_en = ""
        tp_en = topic_page_for_name(sid, topic) if topic else None
        if tp_en is not None:
            n_tp = topic_question_count(questions, sid, tp_en)
            topic_link_en = f' · <a href="{esc(topic_path(sid, tp_en["slug"]))}">Topic: {esc(topic)}（{n_tp} questions）</a>'
        for t_label, t_slug, n_q in question_topic_chips(qen_q, tmap, tcounts):
            topic_link_en += f' · <a href="/topics/{esc(t_slug)}/">Topic: {esc(t_label)}（{n_q} questions）</a>'
        cta = (
            f'<p class="page-cta open-cta"><a href="{esc(bank_href)}">Open this question in the bank</a>'
            f' · <a href="{esc(en_row["path"])}">Back to {year} {esc(pl)}</a>'
            + (f' · <a href="{esc(zh_link)}">中文版</a>' if zh_link else "")
            + topic_link_en
            + "</p>"
        )
        en_opts = dict(re.findall(r"^-\s*([A-D])[.．、]\s*(.+)$", str(qen_q.get("text") or ""), re.M))
        en_opts = {k: _clean_text(v) for k, v in en_opts.items()}
        en_answers = [{"@type": "Answer", "text": f"{L}. {_term(en_opts[L])}"} for L in "ABCD" if L in en_opts]
        qtext = _clean_text(qen_q.get("text"))[:500]
        accepted = ""
        if correct_letter and correct_letter in en_opts:
            accepted = f"{correct_letter}. {_term(en_opts[correct_letter])}."
        name = f"DSE {subj_en} {year} {pl} Question {qno}"
        graph = _qpage_graph(sid, s, akey, en_url, en_row, qno, name, qtext, en_answers, accepted, "en", topic)
        answer_html = ""
        if correct_letter and correct_letter in en_opts:
            answer_html = (
                '<section class="kw-block" aria-label="Answer">\n  <h2>Answer</h2>\n'
                f'  <p class="ai-strategy"><strong>Correct answer: {correct_letter}.</strong> {esc(_term(en_opts[correct_letter]))}</p>\n</section>'
            )
        zh_analysis = _analysis_section_html(analyses[akey])
        zh_inner = f'<a href="{esc(zh_link)}">中文版深度分析</a>' if zh_link else ""
        analysis_note = (
            "The full step-by-step analysis (scaffolding hints, wrong-option traps, speed strategy) is written in Chinese. "
            + zh_inner
        )
        sections_en = [
            '<section class="kw-block" aria-label="Question">\n  <h2>Question</h2>\n'
            f'  <div class="q-embed">{_embed_question_html(qen_q)}</div>\n</section>',
            share_row_html(en_url, f"DSE {subj_en} {year} {pl} Question {qno}" + (f" ({topic})" if topic else ""), "en"),
        ]
        if answer_html:
            sections_en.append(answer_html)
        sections_en.append(
            '<section class="kw-section" aria-label="Deep analysis">\n  <h2>Deep analysis (Chinese)</h2>\n'
            f"  <p>{analysis_note}</p>\n"
            f"  <details><summary>展開中文深度分析（Open detailed analysis）</summary>\n{zh_analysis}\n  </details>\n</section>"
        )
        pn = prevnext_html(en_row["path"] + "q{}/")
        if pn:
            sections_en.append(pn)
        body = hero_html(crumbs, h1, tagline, catalog, sid, cta=cta)
        body += '<main class="subj-main">\n' + "\n".join(sections_en) + "\n</main>"
        alternates = [("en", en_url)] + ([("zh-Hant-HK", zh_link)] if zh_link else [])
        write_landing(
            en_path,
            title,
            desc,
            en_url,
            graph,
            body,
            footer_extra=f'<a href="{esc(en_row["path"])}">Back to {year} {esc(pl)}</a> · <a href="{esc(bank_href)}">Open in the bank</a>',
            lang="en",
            og_locale="en_HK",
            alternates=alternates,
            og_image=question_og_url(sid, year, code, qno),
            body_attrs=f'data-qpage data-topic="{esc(topic)}" data-year="{esc(str(year))}" data-paper="{esc(str(code))}" data-qno="{esc(str(qno))}" data-lang="en"',
        )
        add_sitemap(en_url, "0.8", "monthly")
        count += 1
    print("question pages", count)
    return count



def make_topic_pages(catalog, questions, papers):
    count = 0
    by_subj = defaultdict(int)
    existing = {q.get("subject"): set() for q in questions}
    # collect existing tags per subject
    tagset = defaultdict(set)
    for q in questions:
        sid = SUBJECT_TO_SID.get(q.get("subject"))
        if not sid:
            continue
        for tag in q.get("tags") or []:
            tagset[sid].add(tag)
    for tp in TOPIC_PAGES:
        sid = tp["subject_id"]
        s = subject_meta(sid)
        # keep only tags that exist
        tags = [tag for tag in tp["tags"] if tag in tagset[sid]]
        if not tags:
            print("SKIP topic (no real tags)", sid, tp["name"])
            continue
        rows = sort_questions(questions_for_tags(questions, sid, tags))
        if len(rows) < 8:
            print("SKIP thin topic", sid, tp["name"], len(rows))
            continue
        path = topic_path(sid, tp["slug"])
        url = SITE + path
        years = sorted({q_year(q) for q in rows}, key=year_sort_key)
        span = f"{years[0]}" if len(years) == 1 else f"{years[0]}–{years[-1]}"
        title = tp["title"]
        desc = tp["description"]
        h1 = tp["h1"]
        tagline = (
            f"{esc(tp['blurb'])} 想搵「DSE {esc(s['short'])} {esc(tp['name'])} past paper」"
            f"可以直接喺呢頁操。資料庫有 {len(rows)} 題（{esc(span)}），真正完全免費。"
        )
        hub = hub_topic_path(sid)
        cta = (
            f'<p class="page-cta"><a href="{esc(hub)}">喺 DSE 數學題庫 按課題篩選{esc(s["short"])}題目</a>'
            f' · <a href="/{sid}/">返回{esc(s["short"])}科目頁</a>'
            f' · <a href="/hub/?subject={sid}&amp;mode=year">按年份睇卷</a></p>'
        )
        year_list = sorted({q_year(q) for q in rows}, key=year_sort_key, reverse=True)
        year_hits = nav_pills(
            [(year_path(sid, y), str(y), y) for y in year_list],
            label="年份",
        )
        extra_nav = year_hits
        if tp.get("strand"):
            extra_nav += (
                "\n        "
                + nav_pills(
                    [
                        (f"/{st['subject_id']}/{st['slug']}/", st["name"], st["slug"])
                        for st in STRANDS
                        if st["subject_id"] == sid
                    ],
                    current=tp["strand"],
                    label="課題範疇",
                )
            )
        topic_nav = topic_nav_html(sid, current=tp["slug"])
        if topic_nav:
            extra_nav += "\n        " + topic_nav
        # tag counts
        tag_counts = []
        for tag in tags:
            n = len(questions_for_tag(questions, sid, tag))
            if n:
                tag_counts.append((tag, n))
        tag_html = "\n    ".join(
            f'<a href="{esc(hub_topic_path(sid, tag))}">{esc(tag)}<span class="n">{n} 題</span></a>'
            for tag, n in tag_counts
        )
        related_papers = related_papers_for_years(papers, sid, year_list)
        guide_html = topic_guide_html(tp.get("guide"))
        if not guide_html:
            raise SystemExit(f"missing topic guide: {sid} {tp['name']}")
        sections = [
            guide_html,
            '<section class="strand-index" aria-label="相關標籤">\n'
            "  <h2>相關題目標籤</h2>\n"
            '  <nav class="strand-nav">\n    '
            + tag_html
            + "\n  </nav>\n</section>",
            f'<section class="strand-index" aria-label="出現年份">\n  <h2>出現年份</h2>\n  {year_hits}\n</section>',
        ]
        if related_papers:
            sections.append(related_papers)
        sections.append(
            f'<section class="kw-section" aria-label="題目索引">\n  <h2>題目索引（{len(rows)} 題）</h2>\n  '
            + q_list_html(rows, topic=tp["name"])
            + "\n</section>"
        )
        crumbs = [("/hub/", "DSE 數學題庫"), (f"/{sid}/", s["short"])]
        crumb_ld = [("/hub/", "DSE 數學題庫"), (f"/{sid}/", s["short"])]
        if tp.get("strand"):
            st = next((x for x in STRANDS if x["slug"] == tp["strand"] and x["subject_id"] == sid), None)
            if st:
                crumbs.append((f"/{sid}/{st['slug']}/", st["name"]))
                crumb_ld.append((f"/{sid}/{st['slug']}/", st["name"]))
        crumbs.append((None, tp["name"]))
        crumb_ld.append((url, tp["name"]))
        graph = {
            "@context": "https://schema.org",
            "@graph": [
                ld_breadcrumb(crumb_ld),
                {
                    "@type": "CollectionPage",
                    "name": title,
                    "description": desc,
                    "url": url,
                    "inLanguage": "zh-Hant-HK",
                    "isPartOf": {"@id": f"{SITE}/#website"},
                    "about": {"@type": "Thing", "name": f"香港中學文憑 {s['name']} {tp['name']}"},
                    "mainEntity": {
                        "@type": "ItemList",
                        "name": f"DSE {s['short']} {tp['name']} 歷屆試題",
                        "numberOfItems": len(rows),
                        "itemListElement": [
                            {
                                "@type": "ListItem",
                                "position": i,
                                "name": f"{q['subject']} {q['year']} {paper_zh_label(q.get('paper'))} Q{q['qno']}",
                                "url": question_href(q, tp["name"]),
                            }
                            for i, q in enumerate(rows[:50], 1)
                        ],
                    },
                },
                {
                    "@type": "FAQPage",
                    "mainEntity": faq_ld_entities(LANDING_FAQS),
                },
            ],
        }
        body = hero_html(crumbs, h1, tagline, catalog, sid, extra_nav=extra_nav, cta=cta)
        body += '<main class="subj-main">\n' + "\n".join(sections) + "\n" + faq_block(LANDING_FAQS) + "\n</main>"
        write_landing(
            path,
            title,
            desc,
            url,
            graph,
            body,
            footer_extra=f'<a href="/{sid}/">返回{esc(s["short"])}科目頁</a>',
        )
        add_sitemap(url, "0.75", "weekly")
        by_subj[sid] += 1
        count += 1
        print("topic", path, "qs", len(rows), "tags", len(tag_counts))
    print("topic pages", count, dict(by_subj))
    return count


def sitemap_local_path(loc):
    path = loc[len(SITE) :] if loc.startswith(SITE) else loc
    if not path.startswith("/"):
        path = "/" + path
    if path.endswith("/"):
        return ROOT / path.lstrip("/") / "index.html"
    return ROOT / path.lstrip("/")


def make_question_redirect_stubs():
    """舊 /questions/math/<年>/<卷>/qN/ 頁換成 redirect stub（canonical + meta refresh；Hostinger 由 .htaccess 301）。"""
    qdir = ROOT / "questions" / "math"
    if not qdir.is_dir():
        print("question stubs 0 (no questions dir)")
        return 0
    made = skipped = 0
    for p in sorted(qdir.glob("*/*/q*/index.html")):
        rel = p.relative_to(ROOT).as_posix().replace("\\", "/")
        target_rel = rel[len("questions/") : -len("index.html")]
        if not (ROOT / target_rel / "index.html").is_file():
            # 新深度分析頁未出（無 analysis JSON）— 舊頁保留原樣，唔好 301 去 404
            skipped += 1
            continue
        url = f"{SITE}/{target_rel}"
        stub = (
            "<!DOCTYPE html>\n"
            '<html lang="zh-Hant-HK">\n<head>\n<meta charset="UTF-8">\n'
            f'<meta http-equiv="refresh" content="0; url={esc(url)}">\n'
            f'<link rel="canonical" href="{esc(url)}">\n'
            '<meta name="robots" content="noindex, follow">\n'
            "<title>呢頁已搬遷｜DSE 數學題庫</title>\n"
            f"{GA4_TAG}\n</head>\n<body>\n"
            f'<p>呢頁已搬到 <a href="{esc(url)}">{esc(url)}</a>。</p>\n'
            "</body>\n</html>\n"
        )
        p.write_text(stub, encoding="utf-8")
        made += 1
    print("question stubs", made, "kept(old, no target)", skipped)
    return made


def make_redirects():
    """Cloudflare Pages 用嘅 _redirects（Hostinger 301 由 make_htaccess 出）。"""
    (ROOT / "_redirects").write_text(
        "# 舊 /questions/math/ 問題頁併入新深度分析頁（Pages 301）\n"
        "/questions/math/:year/:paper/q:qno/  /math/:year/:paper/q:qno/  301\n",
        encoding="utf-8",
    )


def patch_offline_subjects():
    """純數學站：econ/chem/bio/phys 頁面全部 noindex（檔案留 disk，舊連結唔會 404）。Idempotent。"""
    n = 0
    for sid in ("econ", "chem", "bio", "phys"):
        d = ROOT / sid
        if not d.is_dir():
            continue
        for p in d.rglob("index.html"):
            t = p.read_text(encoding="utf-8", errors="replace")
            m = re.search(r'<meta name="robots" content="([^"]*)"', t)
            if m and "noindex" in m.group(1):
                continue
            new_meta = '<meta name="robots" content="noindex, follow">'
            if m:
                t = t.replace(m.group(0), new_meta, 1)
            elif "</head>" in t:
                t = t.replace("</head>", new_meta + "\n</head>", 1)
            else:
                continue
            p.write_text(t, encoding="utf-8")
            n += 1
    print("offline subjects noindex:", n, "pages patched")


def patch_blog_schema():
    """docs/blog/*/index.html 注入 BlogPosting JSON-LD＋GA4（手維護頁，build 唔會重寫）。"""
    bdir = ROOT / "blog"
    if not bdir.is_dir():
        return
    n = 0
    for p in sorted(bdir.glob("*/index.html")):
        t = p.read_text(encoding="utf-8")
        changed = False
        if "BlogPosting" not in t:
            m_title = re.search(r"<title>([^<]+)</title>", t)
            m_canon = re.search(r'rel="canonical" href="([^"]+)"', t)
            m_desc = re.search(r'name="description" content="([^"]*)"', t)
            m_date = re.search(r'"datePublished":\s*"([0-9-]+)"', t)
            headline = m_title.group(1) if m_title else p.parent.name
            url = m_canon.group(1) if m_canon else f"{SITE}/blog/{p.parent.name}/"
            desc = m_desc.group(1) if m_desc else ""
            pub = m_date.group(1) if m_date else date.fromtimestamp(p.stat().st_mtime).isoformat()
            posting = {
                "@context": "https://schema.org",
                "@type": "BlogPosting",
                "headline": headline,
                "description": desc,
                "url": url,
                "datePublished": pub,
                "dateModified": pub,
                "inLanguage": "zh-Hant-HK",
                "author": {"@type": "Organization", "name": BRAND, "url": HUB},
                "publisher": {
                    "@type": "Organization",
                    "name": BRAND,
                    "logo": {"@type": "ImageObject", "url": f"{SITE}/icons/icon-512.png"},
                },
                "mainEntityOfPage": {"@type": "WebPage", "@id": url},
            }
            block = ld_json(posting) + "\n"
            if "</head>" in t:
                t = t.replace("</head>", block + "</head>", 1)
                changed = True
        if "G-LTB27V0RGW" not in t and "</head>" in t:
            t = t.replace("</head>", GA4_TAG + "\n</head>", 1)
            changed = True
        if changed:
            p.write_text(t, encoding="utf-8")
            n += 1
    print("blog schema patched", n, "pages")


def sanity_check():
    missing = []
    for loc, pri, freq in SITEMAP_URLS:
        if loc.rstrip("/") == SITE or loc.endswith(".pdf"):
            raise SystemExit(f"forbidden sitemap loc: {loc}")
        fp = sitemap_local_path(loc)
        if not fp.is_file():
            missing.append((loc, str(fp)))
    if missing:
        for loc, fp in missing[:20]:
            print("MISSING", loc, fp)
        raise SystemExit(f"sitemap missing {len(missing)} local files")
    gsc = ROOT / "googlee4637b2d8c43fee7.html"
    gsc_text = gsc.read_text(encoding="utf-8").strip()
    if gsc_text != "google-site-verification: googlee4637b2d8c43fee7.html":
        raise SystemExit(f"GSC file changed: {gsc_text!r}")
    # spot checks
    samples = {
        ROOT / "math/2023/index.html": ["免費 DSE 數學 2023", "G-LTB27V0RGW"],
        ROOT / "math/exponents-logarithms/index.html": ["指數與對數", "G-LTB27V0RGW"],
        ROOT / "sitemap.xml": ["https://hkdse.exampaper.cloud/hub/"],
        ROOT / "hub/index.html": [
            "G-LTB27V0RGW",
            VISUAL_TUTOR,
            "點樣搵某一年嘅 DSE past paper？",
            "brand-lockup",
        ],
        ROOT / "math/index.html": ["免費 DSE 數學 past paper", "有冇英文卷可以操？"],
    }
    for fp, needles in samples.items():
        if not fp.is_file():
            raise SystemExit(f"spot-check missing file: {fp}")
        text = fp.read_text(encoding="utf-8")
        if "G-XFB3Y5KTJQ" in text:
            raise SystemExit(f"wrong GA4 id in {fp}")
        for n in needles:
            if n not in text:
                raise SystemExit(f"spot-check {fp} missing {n!r}")
    hub = (ROOT / "hub/index.html").read_text(encoding="utf-8")
    bad_hub = re.findall(r'href="https://hkdse\.exampaper\.cloud#[^"]+"', hub)
    if bad_hub:
        raise SystemExit(f"hub still has bank hash links: {bad_hub[:5]}")
    # hub/app.js 頂層 $() 引用嘅元素 ID 必須存在於 hub/index.html（手改頁面冇同步入模板就會令 app 成個死）
    app_js = (ROOT / "hub/app.js").read_text(encoding="utf-8")
    missing_ids = sorted(
        {
            m
            for m in re.findall(r'\$\("([A-Za-z][A-Za-z0-9_-]*)"\)', app_js)
            if f'id="{m}"' not in hub
        }
    )
    if missing_ids:
        raise SystemExit(f"hub/app.js references element ids missing from hub/index.html: {missing_ids}")
    sm = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    if f"<loc>{SITE}</loc>" in sm or f"<loc>{SITE}/</loc>" in sm:
        raise SystemExit("sitemap includes domain root")
    if ".pdf" in sm.lower():
        raise SystemExit("sitemap includes pdf")
    # Every local landing index.html (except site root) should be in the sitemap.
    # 非數學科已落線：notice 頁由人工維護、唔喺呢個 build 嘅 sitemap 入面，跳過。
    # questions/（sitemap-questions.xml 管）、m1/、m2/、download/ 等（專責腳本管）唔要求入呢個 sitemap。
    OWNED_PREFIXES = ("math/", "topics/", "hub/")
    OFFLINE_PREFIXES = ("chem/", "econ/", "bio/", "phys/")
    expected = set()
    for p in ROOT.rglob("index.html"):
        rel = p.relative_to(ROOT).as_posix()
        if "mathjax" in rel:
            continue
        if rel == "index.html" or rel.startswith(OFFLINE_PREFIXES):
            continue
        if not rel.startswith(OWNED_PREFIXES):
            continue
        expected.add(f"{SITE}/{p.parent.relative_to(ROOT).as_posix()}/".replace("\\", "/"))
    locs = set(re.findall(r"<loc>(.*?)</loc>", sm))
    missing_pages = sorted(expected - locs)
    if missing_pages:
        raise SystemExit(f"sitemap missing pages: {missing_pages[:10]}")
    # Canonical／og:url 唔准有 fragment（#）— fragment 會令成層頁面被當首頁重複
    frag_bad = []
    for prefix in ("math/", "questions/", "m1/", "m2/", "topics/"):
        for p in (ROOT / prefix).rglob("index.html"):
            t = p.read_text(encoding="utf-8", errors="replace")
            for m in re.finditer(r'(?:rel="canonical" href|property="og:url" content)="([^"]+)"', t):
                if "#" in m.group(1):
                    frag_bad.append((p.as_posix(), m.group(1)))
    if frag_bad:
        raise SystemExit(f"canonical/og:url contains fragment: {frag_bad[:5]}")
    # 深度分析頁 canonical 必須 = SITE + 自身路徑
    for p in (ROOT / "math").rglob("index.html"):
        rel = p.relative_to(ROOT).as_posix().replace("\\", "/")
        if not re.search(r"/q[0-9]+/index\.html$", rel):
            continue
        t = p.read_text(encoding="utf-8", errors="replace")
        want = f'{SITE}/{rel[: -len("index.html")]}'
        if f'<link rel="canonical" href="{want}">' not in t:
            m = re.search(r'rel="canonical" href="([^"]+)"', t)
            raise SystemExit(f"q-page canonical wrong: {rel} -> {m.group(1) if m else None!r} (want {want})")
    # robots.txt 列嘅 sitemap 同 disk 上實際檔案一致
    robots_txt = (ROOT / "robots.txt").read_text(encoding="utf-8")
    robots_sms = set(re.findall(r"^Sitemap:\s*\S+/(\S+)$", robots_txt, re.M))
    disk_sms = {p.name for p in ROOT.glob("sitemap*.xml")}
    if robots_sms != disk_sms:
        raise SystemExit(f"robots sitemap list {sorted(robots_sms)} != disk {sorted(disk_sms)}")
    print("sanity check ok", "sitemap urls", len(locs), "local landings", len(expected))


def main():
    global SITEMAP_URLS
    SITEMAP_URLS = []
    catalog = parse_catalog()
    topics = parse_topics()
    questions = parse_questions()
    papers = collect_papers(catalog, questions)
    analyses = load_analyses()
    print("catalog", len(catalog), "questions", len(questions), "papers", len(papers))
    # 退役 sitemap：sitemap-questions.xml（舊問題頁已 301）、sitemap-topics.xml（URL 已併入 sitemap.xml）
    for retired in ("sitemap-questions.xml", "sitemap-topics.xml"):
        p = ROOT / retired
        if p.is_file():
            p.unlink()
            print("retired sitemap removed:", retired)
    make_og()
    make_htaccess()
    make_robots()
    make_hub(catalog, papers)
    make_subject_pages(catalog, papers)
    make_strand_pages(catalog, questions, topics)
    n_year = make_year_pages(catalog, papers, questions)
    n_paper = make_paper_pages(catalog, papers, questions, analyses)
    n_question = make_question_pages(catalog, papers, questions, analyses)
    n_topic = make_topic_pages(catalog, questions, papers)
    upgrade_legacy_topic_pages()
    n_stub = make_question_redirect_stubs()
    make_redirects()
    make_sitemap()
    make_feed()
    patch_offline_subjects()
    patch_blog_schema()
    patch_css()
    patch_hub_data(papers)
    patch_app()
    patch_root_index()
    patch_sw()
    sanity_check()
    print("SEO build complete", "years", n_year, "papers", n_paper, "questions", n_question, "topics", n_topic)


if __name__ == "__main__":
    main()
