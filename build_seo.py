#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build on-page SEO assets for hkdse.exampaper.cloud (run from this folder)."""
from __future__ import annotations

import html
import json
import re
from collections import defaultdict
from datetime import date
from pathlib import Path
from urllib.parse import quote, urlencode

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path("/workspace/hkdse-publish/dse-maths-question-bank/docs")
SITE = "https://hkdse.exampaper.cloud"
VER = "20261112seo2"
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
        "blurb": "按年份或課題查閱香港中學文憑試（DSE）數學必修部分歷屆試題，涵蓋卷一、卷二，部分年份有中文或英文卷。適合操卷、對題同按課題集中溫習。",
        "title": "DSE 數學必修歷屆試題免費 Past Paper（2012–2023）｜DSE Hub",
        "description": "免費查閱 DSE 數學必修部分 2012 至 2023 年歷屆試題，按年份或課題溫習卷一、卷二。DSE Hub 提供題目索引同課題標籤，方便操卷。",
        "h1": "DSE 數學必修歷屆試題",
    },
    {
        "id": "econ",
        "slug": "econ",
        "name": "經濟",
        "short": "經濟",
        "en": "Economics",
        "blurb": "查閱 DSE 經濟科歷屆試題，而家資料庫已有 2015、2017、2020 年卷一（英文卷），可按課題例如供求、GDP、貨幣同貿易集中溫習。",
        "title": "DSE 經濟歷屆試題免費 Past Paper（2015、2017、2020）｜DSE Hub",
        "description": "免費查閱 DSE 經濟科歷屆試題，現有 2015、2017、2020 年卷一。可按課題溫習供求、市場、GDP、貨幣同國際貿易等。",
        "h1": "DSE 經濟歷屆試題",
    },
    {
        "id": "chem",
        "slug": "chem",
        "name": "化學",
        "short": "化學",
        "en": "Chemistry",
        "blurb": "查閱 DSE 化學科歷屆試題，資料庫已覆蓋 2012 至 2025 年卷一甲、卷一乙同卷二（中文卷），方便按年份揀卷操練。",
        "title": "DSE 化學歷屆試題免費 Past Paper（2012–2025）｜DSE Hub",
        "description": "免費查閱 DSE 化學 2012 至 2025 年歷屆試題，包括卷一甲、卷一乙同卷二。DSE Hub 提供題目索引，方便按年份操卷。",
        "h1": "DSE 化學歷屆試題",
    },
    {
        "id": "bio",
        "slug": "bio",
        "name": "生物",
        "short": "生物",
        "en": "Biology",
        "blurb": "查閱 DSE 生物科歷屆試題。而家資料庫已有 2023 年卷一同卷二（中文卷），之後會繼續加其他年份。",
        "title": "DSE 生物歷屆試題免費 Past Paper（2023）｜DSE Hub",
        "description": "免費查閱 DSE 生物歷屆試題。現已提供 2023 年卷一同卷二，可喺 DSE Hub 直接檢視題目。",
        "h1": "DSE 生物歷屆試題",
    },
    {
        "id": "phys",
        "slug": "phys",
        "name": "物理",
        "short": "物理",
        "en": "Physics",
        "blurb": "查閱 DSE 物理科歷屆試題。而家資料庫已有 2024 年卷一同卷二（中文卷），之後會繼續加其他年份。",
        "title": "DSE 物理歷屆試題免費 Past Paper（2024）｜DSE Hub",
        "description": "免費查閱 DSE 物理歷屆試題。現已提供 2024 年卷一同卷二，可喺 DSE Hub 直接檢視題目。",
        "h1": "DSE 物理歷屆試題",
    },
]

# One landing page per curriculum strand (not per keyword).
STRANDS = [
    {
        "subject_id": "math",
        "name": "數與代數",
        "slug": "number-and-algebra",
        "title": "免費 DSE 數學 數與代數 歷屆試題｜DSE Hub",
        "description": "免費查閱 DSE 數學「數與代數」歷屆試題，按百分法、函數與圖像、數列、變分等課題溫習。DSE Hub 提供題目索引，方便操卷。",
        "h1": "DSE 數學：數與代數",
        "blurb": "集中溫習 DSE 數學必修「數與代數」，包括百分法、指數與對數、方程、函數與圖像、數列同變分等課題。",
    },
    {
        "subject_id": "math",
        "name": "度量、圖形與空間",
        "slug": "measures-shape-space",
        "title": "免費 DSE 數學 度量、圖形與空間 歷屆試題｜DSE Hub",
        "description": "免費查閱 DSE 數學「度量、圖形與空間」歷屆試題，按求積法、軌跡等課題溫習三角、坐標同圖形題。DSE Hub 提供題目索引，方便操卷。",
        "h1": "DSE 數學：度量、圖形與空間",
        "blurb": "集中溫習 DSE 數學必修「度量、圖形與空間」，包括三角、求積法、坐標幾何、圓形幾何、軌跡同幾何變換。",
    },
    {
        "subject_id": "math",
        "name": "數據處理",
        "slug": "data-handling",
        "title": "免費 DSE 數學 數據處理 歷屆試題｜DSE Hub",
        "description": "免費查閱 DSE 數學「數據處理」歷屆試題，按概率、排列與組合等課題集中溫習統計題。DSE Hub 提供題目索引，方便操卷。",
        "h1": "DSE 數學：數據處理",
        "blurb": "集中溫習 DSE 數學必修「數據處理」，包括統計圖表、集中趨勢與離差、概率同排列與組合。",
    },
    {
        "subject_id": "econ",
        "name": "基本經濟概念",
        "slug": "basic-concepts",
        "title": "免費 DSE 經濟 基本經濟概念 歷屆試題｜DSE Hub",
        "description": "免費查閱 DSE 經濟「基本經濟概念」歷屆試題，按機會成本、稀少性、經濟制度等課題溫習。DSE Hub 提供題目索引，方便操卷。",
        "h1": "DSE 經濟：基本經濟概念",
        "blurb": "集中溫習 DSE 經濟「基本經濟概念」，包括機會成本、稀少性、基本經濟問題、經濟制度同價格機制。",
    },
    {
        "subject_id": "econ",
        "name": "生產與企業",
        "slug": "production-firms",
        "title": "免費 DSE 經濟 生產與企業 歷屆試題｜DSE Hub",
        "description": "免費查閱 DSE 經濟「生產與企業」歷屆試題，按成本、規模經濟、公司種類、勞動生產力等課題溫習。DSE Hub 方便按課題操卷。",
        "h1": "DSE 經濟：生產與企業",
        "blurb": "集中溫習 DSE 經濟「生產與企業」，包括公司種類、成本、規模經濟、利潤同勞動生產力。",
    },
    {
        "subject_id": "econ",
        "name": "市場與價格",
        "slug": "market-and-price",
        "title": "免費 DSE 經濟 市場與價格 歷屆試題｜DSE Hub",
        "description": "免費查閱 DSE 經濟「市場與價格」歷屆試題，按供求、彈性、價格上限、補貼同稅負等課題溫習。DSE Hub 方便按課題操卷。",
        "h1": "DSE 經濟：市場與價格",
        "blurb": "集中溫習 DSE 經濟「市場與價格」，包括供求、彈性、價格管制、稅同補貼。",
    },
    {
        "subject_id": "econ",
        "name": "市場結構與競爭",
        "slug": "market-structure",
        "title": "免費 DSE 經濟 市場結構與競爭 歷屆試題｜DSE Hub",
        "description": "免費查閱 DSE 經濟「市場結構與競爭」歷屆試題，按完全競爭、壟斷性競爭、寡頭壟斷同價格歧視等課題溫習。",
        "h1": "DSE 經濟：市場結構與競爭",
        "blurb": "集中溫習 DSE 經濟「市場結構與競爭」，包括完全競爭、壟斷性競爭、寡頭壟斷同價格歧視。",
    },
    {
        "subject_id": "econ",
        "name": "效率、公平與政府角色",
        "slug": "efficiency-equity-government",
        "title": "免費 DSE 經濟 效率、公平與政府角色 歷屆試題｜DSE Hub",
        "description": "免費查閱 DSE 經濟「效率、公平與政府角色」歷屆試題，按外部性、堅尼系數、稅制同收入不均等課題溫習。",
        "h1": "DSE 經濟：效率、公平與政府角色",
        "blurb": "集中溫習 DSE 經濟「效率、公平與政府角色」，包括外部性、公營物品、收入不均、堅尼系數同稅制。",
    },
    {
        "subject_id": "econ",
        "name": "經濟表現量度",
        "slug": "measuring-performance",
        "title": "免費 DSE 經濟 經濟表現量度 歷屆試題｜DSE Hub",
        "description": "免費查閱 DSE 經濟「經濟表現量度」歷屆試題，按 GDP、名義同實質 GDP、人均 GDP、國民收入等課題溫習。",
        "h1": "DSE 經濟：經濟表現量度",
        "blurb": "集中溫習 DSE 經濟「經濟表現量度」，包括 GDP、名義同實質 GDP、人均 GDP、國民收入同產業結構。",
    },
    {
        "subject_id": "econ",
        "name": "國民收入與價格水平",
        "slug": "national-income-price-level",
        "title": "免費 DSE 經濟 國民收入與價格水平 歷屆試題｜DSE Hub",
        "description": "免費查閱 DSE 經濟「國民收入與價格水平」歷屆試題，按總需求、總供給、AD-AS、產出缺口等課題溫習。",
        "h1": "DSE 經濟：國民收入與價格水平",
        "blurb": "集中溫習 DSE 經濟「國民收入與價格水平」，包括總需求、總供給、AD-AS、潛在產出同產出缺口。",
    },
    {
        "subject_id": "econ",
        "name": "貨幣與銀行",
        "slug": "money-and-banking",
        "title": "免費 DSE 經濟 貨幣與銀行 歷屆試題｜DSE Hub",
        "description": "免費查閱 DSE 經濟「貨幣與銀行」歷屆試題，按貨幣供應、銀行乘數、聯繫匯率同利率等課題溫習。",
        "h1": "DSE 經濟：貨幣與銀行",
        "blurb": "集中溫習 DSE 經濟「貨幣與銀行」，包括貨幣供應、存款創造、銀行乘數、聯繫匯率同利率。",
    },
    {
        "subject_id": "econ",
        "name": "宏觀經濟問題與政策",
        "slug": "macro-problems-policy",
        "title": "免費 DSE 經濟 宏觀經濟問題與政策 歷屆試題｜DSE Hub",
        "description": "免費查閱 DSE 經濟「宏觀經濟問題與政策」歷屆試題，按通脹、失業、財政政策、貨幣政策等課題溫習。",
        "h1": "DSE 經濟：宏觀經濟問題與政策",
        "blurb": "集中溫習 DSE 經濟「宏觀經濟問題與政策」，包括通脹、失業、財政政策、貨幣政策同貨幣數量理論。",
    },
    {
        "subject_id": "econ",
        "name": "國際貿易與金融",
        "slug": "international-trade-finance",
        "title": "免費 DSE 經濟 國際貿易與金融 歷屆試題｜DSE Hub",
        "description": "免費查閱 DSE 經濟「國際貿易與金融」歷屆試題，按比較優勢、貿易得益、匯率、經常帳同國際收支等課題溫習。",
        "h1": "DSE 經濟：國際貿易與金融",
        "blurb": "集中溫習 DSE 經濟「國際貿易與金融」，包括比較優勢、貿易得益、匯率、經常帳同國際收支。",
    },
]

SID_TO_SUBJECT = {"math": "數學", "econ": "經濟", "chem": "化學", "bio": "生物", "phys": "物理"}
SUBJECT_PREFIX = {"數學": "", "經濟": "econ", "化學": "chem", "生物": "bio", "物理": "phys"}
SAMPLE_Q = 3
VISUAL_TUTOR = "https://dsemaths.canonlessons.com"
VISUAL_TUTOR_LABEL = "免費 DSE 數學視覺教程"
SUBJECT_TO_SID = {v: k for k, v in SID_TO_SUBJECT.items()}
SITEMAP_URLS = []

PAPER_CODE = {
    "卷一": "paper-1",
    "卷二": "paper-2",
    "卷一甲": "paper-1a",
    "卷一乙": "paper-1b",
    "Paper 1": "paper-1",
    "Paper 2": "paper-2",
    "Paper 1A": "paper-1a",
    "Paper 1B": "paper-1b",
}
PAPER_ZH = {
    "paper-1": "卷一",
    "paper-2": "卷二",
    "paper-1a": "卷一甲",
    "paper-1b": "卷一乙",
}

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
     "title": "免費 DSE 數學 指數與對數 歷屆試題｜DSE Hub",
     "description": "免費查閱 DSE 數學「指數與對數」歷屆試題，按指數定律、對數同指數函數等課題操練。DSE Hub 真正完全免費。",
     "h1": "DSE 數學：指數與對數",
     "blurb": "集中溫習指數定律、對數、指數函數同相關方程題。"},
    {"subject_id": "math", "name": "比、率與比例", "slug": "ratio-rate-proportion", "strand": "number-and-algebra",
     "tags": KW_TAG_MAP["比、率與比例"],
     "title": "免費 DSE 數學 比、率與比例 歷屆試題｜DSE Hub",
     "description": "免費查閱 DSE 數學「比、率與比例」歷屆試題，按比率與比例等課題操練。DSE Hub 真正完全免費。",
     "h1": "DSE 數學：比、率與比例",
     "blurb": "集中溫習比率、比例同相關應用題。"},
    {"subject_id": "math", "name": "多項式與因式分解", "slug": "polynomials-factorization", "strand": "number-and-algebra",
     "tags": KW_TAG_MAP["多項式（續）"],
     "title": "免費 DSE 數學 多項式與因式分解 歷屆試題｜DSE Hub",
     "description": "免費查閱 DSE 數學「多項式與因式分解」歷屆試題，涵蓋多項式、因式分解同因式定理。DSE Hub 真正完全免費。",
     "h1": "DSE 數學：多項式與因式分解",
     "blurb": "集中溫習多項式、因式分解、因式定理等課題，對應課程「多項式（續）」。"},
    {"subject_id": "math", "name": "數系", "slug": "number-systems", "strand": "number-and-algebra",
     "tags": KW_TAG_MAP["數系"],
     "title": "免費 DSE 數學 數系 歷屆試題｜DSE Hub",
     "description": "免費查閱 DSE 數學「數系」歷屆試題，按複數、數制同進制轉換等課題操練。DSE Hub 真正完全免費。",
     "h1": "DSE 數學：數系",
     "blurb": "集中溫習複數、數制、進制轉換等數系課題。"},
    {"subject_id": "math", "name": "方程與不等式", "slug": "equations-inequalities", "strand": "number-and-algebra",
     "tags": KW_TAG_MAP["方程與不等式"],
     "title": "免費 DSE 數學 方程與不等式 歷屆試題｜DSE Hub",
     "description": "免費查閱 DSE 數學「方程與不等式」歷屆試題，按一元二次方程、不等式同線性規劃等課題操練。DSE Hub 真正完全免費。",
     "h1": "DSE 數學：方程與不等式",
     "blurb": "集中溫習方程、不等式、聯立方程同線性規劃。"},
    {"subject_id": "math", "name": "百分法與利息", "slug": "percentages-interest", "strand": "number-and-algebra",
     "tags": KW_TAG_MAP["百分法"],
     "title": "免費 DSE 數學 百分法與利息 歷屆試題｜DSE Hub",
     "description": "免費查閱 DSE 數學「百分法與利息」歷屆試題，按百分數、百分比同利息增長等課題操練。DSE Hub 真正完全免費。",
     "h1": "DSE 數學：百分法與利息",
     "blurb": "集中溫習百分法、百分比、利息同增長題。"},
    {"subject_id": "math", "name": "函數與圖像", "slug": "functions-graphs", "strand": "number-and-algebra",
     "tags": ["二次函數", "函數與圖像", "函數", "二次函數圖像", "圖像"],
     "title": "免費 DSE 數學 函數與圖像 歷屆試題｜DSE Hub",
     "description": "免費查閱 DSE 數學「函數與圖像」歷屆試題，按二次函數同函數圖像等課題操練。DSE Hub 真正完全免費。",
     "h1": "DSE 數學：函數與圖像",
     "blurb": "集中溫習函數、二次函數同圖像題。"},
    {"subject_id": "math", "name": "數列", "slug": "sequences", "strand": "number-and-algebra",
     "tags": ["數列", "等比數列", "等差數列", "公比"],
     "title": "免費 DSE 數學 數列 歷屆試題｜DSE Hub",
     "description": "免費查閱 DSE 數學「數列」歷屆試題，按等比數列、等差數列等課題操練。DSE Hub 真正完全免費。",
     "h1": "DSE 數學：數列",
     "blurb": "集中溫習數列、等比數列同等差數列。"},
    {"subject_id": "math", "name": "變分", "slug": "variations", "strand": "number-and-algebra",
     "tags": ["變分", "正變", "部分正變"],
     "title": "免費 DSE 數學 變分 歷屆試題｜DSE Hub",
     "description": "免費查閱 DSE 數學「變分」歷屆試題，按正變等課題操練。DSE Hub 真正完全免費。",
     "h1": "DSE 數學：變分",
     "blurb": "集中溫習變分同正變題。"},
    # math — 度量、圖形與空間
    {"subject_id": "math", "name": "三角學與解三角形", "slug": "trigonometry", "strand": "measures-shape-space",
     "tags": KW_TAG_MAP["三角學與解三角形"],
     "title": "免費 DSE 數學 三角學與解三角形 歷屆試題｜DSE Hub",
     "description": "免費查閱 DSE 數學「三角學與解三角形」歷屆試題，按三角比、三角恆等式同正弦／餘弦定理等課題操練。DSE Hub 真正完全免費。",
     "h1": "DSE 數學：三角學與解三角形",
     "blurb": "集中溫習三角比、解三角形、三角恆等式同相關定理。"},
    {"subject_id": "math", "name": "坐標幾何：直線", "slug": "coordinate-geometry-line", "strand": "measures-shape-space",
     "tags": KW_TAG_MAP["坐標幾何：直線"],
     "title": "免費 DSE 數學 坐標幾何（直線）歷屆試題｜DSE Hub",
     "description": "免費查閱 DSE 數學「坐標幾何：直線」歷屆試題，按直線方程、斜率同點到直線距離等課題操練。DSE Hub 真正完全免費。",
     "h1": "DSE 數學：坐標幾何（直線）",
     "blurb": "集中溫習直線方程同坐標平面上嘅直線問題。"},
    {"subject_id": "math", "name": "坐標幾何：圓", "slug": "coordinate-geometry-circle", "strand": "measures-shape-space",
     "tags": KW_TAG_MAP["坐標幾何：圓"],
     "title": "免費 DSE 數學 坐標幾何（圓）歷屆試題｜DSE Hub",
     "description": "免費查閱 DSE 數學「坐標幾何：圓」歷屆試題，按圓的方程、直線與圓相交等課題操練。DSE Hub 真正完全免費。",
     "h1": "DSE 數學：坐標幾何（圓）",
     "blurb": "集中溫習圓的方程同直線與圓嘅關係。"},
    {"subject_id": "math", "name": "圓形幾何", "slug": "circle-geometry", "strand": "measures-shape-space",
     "tags": KW_TAG_MAP["圓形幾何"],
     "title": "免費 DSE 數學 圓形幾何 歷屆試題｜DSE Hub",
     "description": "免費查閱 DSE 數學「圓形幾何」歷屆試題，按圓的性質、圓的幾何同圓周角等課題操練。DSE Hub 真正完全免費。",
     "h1": "DSE 數學：圓形幾何",
     "blurb": "集中溫習圓的性質、圓周角同相關幾何題。"},
    {"subject_id": "math", "name": "幾何變換", "slug": "geometric-transformations", "strand": "measures-shape-space",
     "tags": KW_TAG_MAP["幾何變換"],
     "title": "免費 DSE 數學 幾何變換 歷屆試題｜DSE Hub",
     "description": "免費查閱 DSE 數學「幾何變換」歷屆試題，按變換與對稱、平移、旋轉同反射等課題操練。DSE Hub 真正完全免費。",
     "h1": "DSE 數學：幾何變換",
     "blurb": "集中溫習變換、對稱、平移、旋轉同反射。"},
    {"subject_id": "math", "name": "求積法", "slug": "mensuration", "strand": "measures-shape-space",
     "tags": ["求積法", "立體圖形", "立體幾何", "梯形面積", "體積", "曲面面積", "總表面積", "圓錐", "圓錐體", "圓柱體", "直立角柱體", "直立角錐體"],
     "title": "免費 DSE 數學 求積法 歷屆試題｜DSE Hub",
     "description": "免費查閱 DSE 數學「求積法」歷屆試題，按面積、體積同立體圖形等課題操練。DSE Hub 真正完全免費。",
     "h1": "DSE 數學：求積法",
     "blurb": "集中溫習求積法、立體圖形同面積體積題。"},
    {"subject_id": "math", "name": "平面幾何與相似三角形", "slug": "plane-geometry-similar-triangles", "strand": "measures-shape-space",
     "tags": ["平面幾何", "相似三角形", "相似圖形", "全等三角形", "等腰三角形", "畢氏定理", "直角三角形"],
     "title": "免費 DSE 數學 平面幾何與相似三角形 歷屆試題｜DSE Hub",
     "description": "免費查閱 DSE 數學「平面幾何與相似三角形」歷屆試題，按相似、全等等課題操練。DSE Hub 真正完全免費。",
     "h1": "DSE 數學：平面幾何與相似三角形",
     "blurb": "集中溫習平面幾何、相似三角形同相關證明題。"},
    # math — 數據處理
    {"subject_id": "math", "name": "統計圖表", "slug": "statistical-graphs", "strand": "data-handling",
     "tags": KW_TAG_MAP["統計圖表"],
     "title": "免費 DSE 數學 統計圖表 歷屆試題｜DSE Hub",
     "description": "免費查閱 DSE 數學「統計圖表」歷屆試題，按統計、框線圖、幹葉圖同棒形圖等課題操練。DSE Hub 真正完全免費。",
     "h1": "DSE 數學：統計圖表",
     "blurb": "集中溫習統計圖表，包括框線圖、幹葉圖同棒形圖。"},
    {"subject_id": "math", "name": "集中趨勢與離差", "slug": "central-tendency-dispersion", "strand": "data-handling",
     "tags": KW_TAG_MAP["集中趨勢與離差"],
     "title": "免費 DSE 數學 集中趨勢與離差 歷屆試題｜DSE Hub",
     "description": "免費查閱 DSE 數學「集中趨勢與離差」歷屆試題，按平均、中位數、標準差同標準分等課題操練。DSE Hub 真正完全免費。",
     "h1": "DSE 數學：集中趨勢與離差",
     "blurb": "集中溫習平均值、中位數、眾數、標準差、標準分同離差。"},
    {"subject_id": "math", "name": "概率", "slug": "probability", "strand": "data-handling",
     "tags": ["概率", "期望值", "幾何概率"],
     "title": "免費 DSE 數學 概率 歷屆試題｜DSE Hub",
     "description": "免費查閱 DSE 數學「概率」歷屆試題，按概率同期望值等課題操練。DSE Hub 真正完全免費。",
     "h1": "DSE 數學：概率",
     "blurb": "集中溫習概率同期望值題。"},
    {"subject_id": "math", "name": "排列與組合", "slug": "permutations-combinations", "strand": "data-handling",
     "tags": ["排列與組合", "計數原理"],
     "title": "免費 DSE 數學 排列與組合 歷屆試題｜DSE Hub",
     "description": "免費查閱 DSE 數學「排列與組合」歷屆試題，按排列、組合同計數原理操練。DSE Hub 真正完全免費。",
     "h1": "DSE 數學：排列與組合",
     "blurb": "集中溫習排列與組合同計數原理。"},
    # chem — clustered curriculum topics
    {"subject_id": "chem", "name": "化學計量", "slug": "stoichiometry", "strand": None,
     "tags": ["摩爾計算", "實驗式", "濃度", "滴定"],
     "title": "免費 DSE 化學 化學計量 歷屆試題｜DSE Hub",
     "description": "免費查閱 DSE 化學「化學計量」歷屆試題，按摩爾計算、實驗式、濃度同滴定等課題操練。DSE Hub 真正完全免費。",
     "h1": "DSE 化學：化學計量",
     "blurb": "集中溫習摩爾計算、實驗式、濃度同滴定。"},
    {"subject_id": "chem", "name": "酸鹼", "slug": "acids-bases", "strand": None,
     "tags": ["酸鹼", "pH", "中和", "酸"],
     "title": "免費 DSE 化學 酸鹼 歷屆試題｜DSE Hub",
     "description": "免費查閱 DSE 化學「酸鹼」歷屆試題，按 pH、中和同酸等課題操練。DSE Hub 真正完全免費。",
     "h1": "DSE 化學：酸鹼",
     "blurb": "集中溫習酸鹼、pH 同中和題。"},
    {"subject_id": "chem", "name": "有機化學", "slug": "organic-chemistry", "strand": None,
     "tags": ["有機化合物", "醇", "官能基", "聚合物", "有機轉化", "烯", "烯烴", "加成聚合", "酯", "裂解", "單體", "系統命名", "對映異構", "旋光性", "水解", "分餾"],
     "title": "免費 DSE 化學 有機化學 歷屆試題｜DSE Hub",
     "description": "免費查閱 DSE 化學「有機化學」歷屆試題，按官能基、醇、烯、聚合物同有機轉化等課題操練。DSE Hub 真正完全免費。",
     "h1": "DSE 化學：有機化學",
     "blurb": "集中溫習有機化合物、官能基、聚合物同有機轉化。"},
    {"subject_id": "chem", "name": "氧化還原", "slug": "redox", "strand": None,
     "tags": ["氧化還原", "氧化數", "還原", "氧化"],
     "title": "免費 DSE 化學 氧化還原 歷屆試題｜DSE Hub",
     "description": "免費查閱 DSE 化學「氧化還原」歷屆試題，按氧化數、氧化同還原等課題操練。DSE Hub 真正完全免費。",
     "h1": "DSE 化學：氧化還原",
     "blurb": "集中溫習氧化還原、氧化數同相關反應。"},
    {"subject_id": "chem", "name": "化學鍵與分子結構", "slug": "bonding-structure", "strand": None,
     "tags": ["分子間引力", "氫鍵", "分子形狀", "電子排佈", "離子化合物", "極性", "分子結構", "電子圖", "結構"],
     "title": "免費 DSE 化學 化學鍵與分子結構 歷屆試題｜DSE Hub",
     "description": "免費查閱 DSE 化學「化學鍵與分子結構」歷屆試題，按分子形狀、氫鍵、電子排佈同極性等課題操練。DSE Hub 真正完全免費。",
     "h1": "DSE 化學：化學鍵與分子結構",
     "blurb": "集中溫習化學鍵、分子結構、分子間引力同電子排佈。"},
    {"subject_id": "chem", "name": "反應速率", "slug": "reaction-rate", "strand": None,
     "tags": ["反應速率", "催化劑"],
     "title": "免費 DSE 化學 反應速率 歷屆試題｜DSE Hub",
     "description": "免費查閱 DSE 化學「反應速率」歷屆試題，按反應速率同催化劑等課題操練。DSE Hub 真正完全免費。",
     "h1": "DSE 化學：反應速率",
     "blurb": "集中溫習反應速率同催化劑題。"},
    {"subject_id": "chem", "name": "化學平衡", "slug": "chemical-equilibrium", "strand": None,
     "tags": ["平衡常數", "平衡", "化學平衡", "勒沙特列原理", "勒沙特列"],
     "title": "免費 DSE 化學 化學平衡 歷屆試題｜DSE Hub",
     "description": "免費查閱 DSE 化學「化學平衡」歷屆試題，按平衡常數同勒沙特列原理等課題操練。DSE Hub 真正完全免費。",
     "h1": "DSE 化學：化學平衡",
     "blurb": "集中溫習化學平衡、平衡常數同勒沙特列原理。"},
    {"subject_id": "chem", "name": "電解與電化學", "slug": "electrolysis-electrochemistry", "strand": None,
     "tags": ["電解", "化學電池", "燃料電池", "電鍍", "導電性", "鏽蝕"],
     "title": "免費 DSE 化學 電解與電化學 歷屆試題｜DSE Hub",
     "description": "免費查閱 DSE 化學「電解與電化學」歷屆試題，按電解、化學電池、燃料電池同電鍍等課題操練。DSE Hub 真正完全免費。",
     "h1": "DSE 化學：電解與電化學",
     "blurb": "集中溫習電解、化學電池、燃料電池同電鍍。"},
    {"subject_id": "chem", "name": "熱化學", "slug": "thermochemistry", "strand": None,
     "tags": ["焓變", "赫斯定律", "生成焓", "燃燒焓", "量熱法", "燃燒"],
     "title": "免費 DSE 化學 熱化學 歷屆試題｜DSE Hub",
     "description": "免費查閱 DSE 化學「熱化學」歷屆試題，按焓變、赫斯定律、生成焓同量熱法等課題操練。DSE Hub 真正完全免費。",
     "h1": "DSE 化學：熱化學",
     "blurb": "集中溫習焓變、赫斯定律、燃燒焓同量熱法。"},
    {"subject_id": "chem", "name": "金屬與周期表", "slug": "metals-periodic-table", "strand": None,
     "tags": ["周期表", "過渡金屬", "金屬活性序", "同位素", "鋁", "鐵", "金屬", "銅"],
     "title": "免費 DSE 化學 金屬與周期表 歷屆試題｜DSE Hub",
     "description": "免費查閱 DSE 化學「金屬與周期表」歷屆試題，按金屬活性序、過渡金屬、同位素同周期表等課題操練。DSE Hub 真正完全免費。",
     "h1": "DSE 化學：金屬與周期表",
     "blurb": "集中溫習周期表、金屬活性序、過渡金屬同同位素。"},
]

# Map a curriculum / topic name to its landing slug (same subject).
TOPIC_SLUG_BY_NAME = {}
for _tp in TOPIC_PAGES:
    TOPIC_SLUG_BY_NAME[(_tp["subject_id"], _tp["name"])] = _tp["slug"]
# 多項式（續） lands on the polynomials cluster page
TOPIC_SLUG_BY_NAME[("math", "多項式（續）")] = "polynomials-factorization"
TOPIC_SLUG_BY_NAME[("math", "百分法")] = "percentages-interest"

HUB_TITLE = "免費 DSE 歷屆試題｜數學經濟化學生物物理 Past Paper｜DSE Hub"
HUB_DESC = "免費查閱香港中學文憑試（DSE）數學、經濟、化學、生物、物理歷屆試題，按年份或課題溫習，支援中英文卷。唔使報名，即時喺 DSE Hub 開卷。"
HUB_H1 = "香港中學文憑（DSE）歷屆試題資料庫"


def esc(s):
    return html.escape(str(s), quote=True)


def parse_catalog():
    text = (ROOT / "hub/data.js").read_text(encoding="utf-8")
    rows = re.findall(
        r'\{ id: "(\w+)", name: "([^"]+)", year: (\d+), paper: "([^"]+)", lang: "([^"]+)", hash: "([^"]+)" \}',
        text,
    )
    catalog = [
        {"id": i, "name": n, "year": int(y), "paper": p, "lang": lg, "hash": h}
        for i, n, y, p, lg, h in rows
    ]
    if len(catalog) < 50:
        raise SystemExit(f"catalog parse too small: {len(catalog)}")
    return catalog


def short_name(name):
    return re.sub(r"（.*?）", "", name).replace("\s", " ").strip()


def year_span(rows):
    years = sorted({r["year"] for r in rows})
    if not years:
        return ""
    if len(years) == 1:
        return str(years[0])
    if years == list(range(years[0], years[-1] + 1)):
        return f"{years[0]}–{years[-1]}"
    if len(years) <= 4:
        return "、".join(str(y) for y in years)
    return f"{years[0]}–{years[-1]}"


GA4_ID = "G-LTB27V0RGW"
GA4_TAG = """<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-LTB27V0RGW"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-LTB27V0RGW');
</script>"""


def seo_head(title, description, canonical, og_type="website", extra=""):
    return f"""<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<meta name="keywords" content="DSE, 香港中學文憑, 歷屆試題, past paper, DSE 數學, DSE 經濟, DSE 化學, DSE 生物, DSE 物理, 免費題庫, 按課題">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="googlebot" content="index, follow">
<meta name="author" content="DSE Hub">
<link rel="canonical" href="{esc(canonical)}">
<link rel="alternate" hreflang="zh-Hant-HK" href="{esc(canonical)}">
<link rel="alternate" hreflang="x-default" href="{esc(canonical)}">
<meta property="og:type" content="{esc(og_type)}">
<meta property="og:site_name" content="DSE Hub">
<meta property="og:locale" content="zh_HK">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{esc(canonical)}">
<meta property="og:image" content="{esc(OG)}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="DSE Hub 香港中學文憑歷屆試題資料庫">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(description)}">
<meta name="twitter:image" content="{esc(OG)}">
<meta name="theme-color" content="#0b1220">
<link rel="manifest" href="/manifest.webmanifest">
<link rel="icon" type="image/png" sizes="32x32" href="/icons/favicon-32.png">
<link rel="icon" type="image/png" sizes="192x192" href="/icons/icon-192.png">
<link rel="apple-touch-icon" sizes="180x180" href="/icons/apple-touch-icon.png">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black">
<meta name="apple-mobile-web-app-title" content="DSE Hub">
<meta name="application-name" content="DSE Hub">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/hub/style.css?v={VER}">
{GA4_TAG}
{extra}"""


def ld_json(obj):
    return '<script type="application/ld+json">\n' + json.dumps(obj, ensure_ascii=False, indent=2) + "\n</script>"


def paper_href(row):
    return BANK.rstrip("/") + row["hash"]


def paper_row_html(r):
    sn = short_name(r["name"])
    landing = r.get("path")
    href = landing or paper_href(r)
    nq = r.get("n_questions")
    title = f"文憑試 DSE {sn} {r['year']} · {r['paper']}（{r['lang']}）"
    sub = esc(r["name"])
    if nq:
        sub += f" · {nq} 題索引"
    elif landing:
        sub += " · 目錄已收錄"
    return f"""    <article class="paper-row">
      <a class="paper-main" href="{esc(href)}" title="開啟卷頁">
        <div class="paper-year">{r['year']}</div>
        <div class="paper-body">
          <div class="paper-tags">
            <span class="tag subj">{esc(sn)}</span>
            <span class="tag cat">{esc(r['paper'])}</span>
            <span class="tag lang">{esc(r['lang'])}</span>
          </div>
          <div class="paper-title">{esc(title)}</div>
          <div class="paper-sub">{sub}</div>
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


def make_og():
    w, h = 1200, 630
    img = Image.new("RGB", (w, h), "#0b1220")
    overlay = Image.new("RGB", (w, h), "#0b1220")
    d0 = ImageDraw.Draw(overlay)
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
    img = base.convert("RGB")
    draw = ImageDraw.Draw(img)

    font_black = ImageFont.truetype("/home/box/.fonts/NotoSansCJKtc-Black.otf", 96)
    font_bold = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc", 42, index=0)
    font_med = ImageFont.truetype("/home/box/.fonts/NotoSansCJKtc-Medium.otf", 32)
    font_sm = ImageFont.truetype("/home/box/.fonts/NotoSansCJKtc-Medium.otf", 24)

    # icon
    icon_path = ROOT / "icons/icon-512.png"
    if icon_path.exists():
        icon = Image.open(icon_path).convert("RGBA").resize((160, 160), Image.Resampling.LANCZOS)
        img.paste(icon, (80, 200), icon)

    left = 280 if icon_path.exists() else 80
    draw.text((left, 168), "DSE Hub", font=font_black, fill="#ffffff")
    draw.text((left, 290), "香港中學文憑歷屆試題資料庫", font=font_bold, fill="#eef3fb")
    draw.text((left, 360), "數學 · 經濟 · 化學 · 生物 · 物理", font=font_med, fill="#93c5fd")
    draw.text((left, 430), "免費　按年份或課題　Past Paper", font=font_sm, fill="#8b9bb3")
    draw.text((80, 560), "hkdse.exampaper.cloud", font=font_sm, fill="#64748b")
    out = ROOT / "og-image.png"
    img.save(out, "PNG", optimize=True)
    print("og-image", out, out.stat().st_size)


def make_htaccess():
    (ROOT / ".htaccess").write_text(
        """# DSE Hub — HTTPS, apex host, static defaults
DirectoryIndex index.html
Options -Indexes

<IfModule mod_rewrite.c>
  RewriteEngine On
  RewriteCond %{HTTPS} !=on
  RewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
  RewriteCond %{HTTP_HOST} ^www\\.hkdse\\.exampaper\\.cloud$ [NC]
  RewriteRule ^ https://hkdse.exampaper.cloud%{REQUEST_URI} [L,R=301]
</IfModule>

<IfModule mod_headers.c>
  Header set X-Content-Type-Options "nosniff"
  Header set Referrer-Policy "strict-origin-when-cross-origin"
</IfModule>

<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType text/html "access plus 1 hour"
  ExpiresByType text/css "access plus 7 days"
  ExpiresByType application/javascript "access plus 7 days"
  ExpiresByType image/png "access plus 30 days"
  ExpiresByType image/jpeg "access plus 30 days"
  ExpiresByType image/svg+xml "access plus 30 days"
  ExpiresByType application/pdf "access plus 30 days"
  ExpiresByType application/manifest+json "access plus 7 days"
</IfModule>

<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/css text/plain application/javascript application/json image/svg+xml
</IfModule>
""",
        encoding="utf-8",
    )


def make_robots():
    (ROOT / "robots.txt").write_text(
        f"""User-agent: *
Allow: /
Disallow: /mathjax/

Sitemap: {SITE}/sitemap.xml
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
    urls.sort(key=lambda x: (0 if x[0] == HUB else 1, x[0]))
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for loc, pri, freq in urls:
        parts.append(
            f"  <url>\n    <loc>{esc(loc)}</loc>\n    <lastmod>2026-11-12</lastmod>\n    <changefreq>{freq}</changefreq>\n    <priority>{pri}</priority>\n  </url>"
        )
    parts.append("</urlset>\n")
    (ROOT / "sitemap.xml").write_text("\n".join(parts), encoding="utf-8")
    print("sitemap", len(urls), "urls")


def sort_rows(rows):
    return sorted(
        rows,
        key=lambda r: (-r["year"], r["lang"], r["name"], r["paper"]),
    )


def make_hub(catalog):
    prerender = "\n".join(paper_row_html(r) for r in sort_rows(catalog))
    counts = defaultdict(int)
    for r in catalog:
        counts[r["id"]] += 1
    item_list = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebSite",
                "@id": f"{SITE}/#website",
                "name": "DSE Hub",
                "alternateName": ["DSE 歷屆試題資料庫", "香港中學文憑歷屆試題"],
                "url": HUB,
                "inLanguage": "zh-Hant-HK",
                "description": HUB_DESC,
                "publisher": {"@id": f"{SITE}/#org"},
            },
            {
                "@type": "Organization",
                "@id": f"{SITE}/#org",
                "name": "DSE Hub",
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
                    {"@type": "Thing", "name": s["name"]} for s in SUBJECTS
                ],
                "mainEntity": {"@id": f"{HUB}#papers"},
            },
            {
                "@type": "ItemList",
                "@id": f"{HUB}#papers",
                "name": "DSE 歷屆試題科目",
                "numberOfItems": 5,
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": i,
                        "name": s["name"],
                        "url": f"{SITE}/{s['slug']}/",
                    }
                    for i, s in enumerate(SUBJECTS, 1)
                ],
            },
            {
                "@type": "FAQPage",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": "DSE Hub 係咪免費？",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": "係，DSE Hub 免費查閱香港中學文憑試歷屆試題索引同題目，唔使報名，亦唔使信用卡。",
                        },
                    },
                    {
                        "@type": "Question",
                        "name": "而家有邊啲科目？",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": "而家有數學（必修部分）、經濟、化學、生物同物理。每科已上線嘅年份同卷別，以資料庫實際內容為準。",
                        },
                    },
                    {
                        "@type": "Question",
                        "name": "可唔可以按課題溫習？",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": "可以。喺主頁揀「按課題」，先揀科目再揀課題，就會列出相關題目，方便集中操同一類型。",
                        },
                    },
                    {
                        "@type": "Question",
                        "name": "呢度係咪官方原卷檔案庫？",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": "站內主要提供索引、題目同課題標籤，方便溫習；部分卷另有 PDF 連結。內容以資料庫已有項目為準，並唔取代考試及評核局官方刊物。",
                        },
                    },
                ],
            },
        ],
    }
    faq_html = """
<section class="seo-faq" aria-label="常見問題">
  <h2>常見問題</h2>
  <details open>
    <summary>DSE Hub 係咪免費？</summary>
    <p>係，免費查閱香港中學文憑試歷屆試題索引同題目，唔使報名，亦唔使信用卡。</p>
  </details>
  <details>
    <summary>而家有邊啲科目？</summary>
    <p>而家有數學（必修部分）、經濟、化學、生物同物理。每科已上線嘅年份同卷別，以資料庫實際內容為準，科目頁會列出全部已有卷。</p>
  </details>
  <details>
    <summary>可唔可以按課題溫習？</summary>
    <p>可以。喺上面揀「按課題」，先揀科目再揀課題，就會列出相關題目，方便集中操同一類型。</p>
  </details>
  <details>
    <summary>呢度係咪官方原卷檔案庫？</summary>
    <p>站內主要提供索引、題目同課題標籤，方便溫習；部分卷另有 PDF 連結。內容以資料庫已有項目為準，並唔取代考試及評核局官方刊物。</p>
  </details>
</section>
"""
    footer_links = " · ".join(
        f'<a href="/{s["slug"]}/">{esc(s["short"])}</a>' for s in SUBJECTS
    )
    add_sitemap(HUB, "1.0", "daily")
    page = f"""<!DOCTYPE html>
<html lang="zh-Hant-HK">
<head>
{seo_head(HUB_TITLE, HUB_DESC, HUB)}
{ld_json(item_list)}
</head>
<body>
<header class="hero">
  <div class="hero-glow" aria-hidden="true"></div>
  <div class="hero-inner">
    <div class="hero-head">
      <p class="brand">DSE Hub</p>
      <button type="button" class="install-btn" data-install-app title="安裝 DSE Hub 到主畫面">
        <span>一鍵安裝</span>
      </button>
    </div>
    <div class="install-tip" id="installTip" hidden>
      <div class="install-tip-body">
        <strong>一鍵加到主畫面</strong>
        <span>iPhone／iPad：用 Safari「分享」→「加到主畫面」。Android／電腦 Chrome、Edge：瀏覽器選單 →「安裝應用程式」。</span>
      </div>
      <button type="button" class="install-tip-x" data-install-close aria-label="閂">×</button>
    </div>
    <h1>{esc(HUB_H1)}</h1>
    <p class="tagline">真正免費。按年份或課題，查閱 DSE 數學、經濟、化學、生物、物理 past paper——唔使報班都睇到題。</p>
        {subject_nav(catalog)}
  </div>
</header>

<nav class="filters" aria-label="篩選">
  <div class="filters-inner">
    <div class="titlebar">
      <span class="filters-label">搵卷</span>
      <div class="seg" id="modeSeg">
        <button type="button" data-mode="year" class="on">按年份</button>
        <button type="button" data-mode="topic">按課題</button>
      </div>
    </div>
    <div class="bar" id="yearBar">
      <div class="field">
        <label>科目</label>
        <button type="button" class="reel-btn" id="bSubj" data-key="subject">所有</button>
      </div>
      <div class="field">
        <label id="l2">年份</label>
        <button type="button" class="reel-btn" id="bYear" data-key="year">所有</button>
      </div>
      <div class="field" id="fPaper">
        <label>卷別</label>
        <button type="button" class="reel-btn" id="bPaper" data-key="paper">所有</button>
      </div>
    </div>
  </div>
</nav>

<main>
  <section id="result" class="paper-list" aria-live="polite">
    <p class="list-count">共 {len(catalog)} 卷</p>
{prerender}
  </section>
</main>
{faq_html}
<footer>站內只放索引、連結同課題標籤，唔存放試卷原卷 · 只顯示資料庫已有內容<br>科目：{footer_links}<br>相關：<a href="{esc(VISUAL_TUTOR)}" rel="noopener">{esc(VISUAL_TUTOR_LABEL)}</a></footer>

<!-- 滾輪（Reel） -->
<div class="reel-overlay" id="reel" hidden>
  <div class="reel-backdrop" id="reelBackdrop"></div>
  <div class="reel-sheet" role="dialog" aria-modal="true" aria-labelledby="reelTitle">
    <div class="reel-head">
      <button type="button" class="reel-link" id="reelCancel">取消</button>
      <span id="reelTitle">科目</span>
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
<script src="//pwa.js?v={VER}"></script>
</body>
</html>
"""
    # typo fix pwa path
    page = page.replace('src="//pwa.js', 'src="/pwa.js')
    (ROOT / "hub/index.html").write_text(page, encoding="utf-8")
    print("hub index", len(page))


def make_subject_pages(catalog, papers):
    by_id = defaultdict(list)
    for r in papers:
        by_id[r["id"]].append(r)
    for s in SUBJECTS:
        rows = sort_rows(by_id[s["id"]])
        if not rows:
            raise SystemExit(f"no rows for {s['id']}")
        span = year_span(rows)
        groups = defaultdict(list)
        for r in rows:
            groups[r["year"]].append(r)
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
                ld_breadcrumb([("/hub/", "DSE Hub"), (url, s["short"])]),
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
            ],
        }
        topic_cta = f'<p class="page-cta"><a href="/hub/?subject={s["id"]}&amp;mode=topic">按課題篩選{esc(s["short"])}題目</a> · <a href="/hub/?subject={s["id"]}&amp;mode=year">按年份睇卷</a></p>'
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
        faq = faq_block([FAQ_FREE, FAQ_TOPIC])
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
    {crumb_html([("/hub/", "DSE Hub"), (None, s["short"])])}
    <p class="brand">DSE Hub</p>
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
{site_footer(f'<a href="/hub/">返回 DSE Hub 主頁</a>')}
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
.open-cta a {
  display: inline-block;
  margin-top: 4px;
}
footer {
  line-height: 1.7;
}
"""
    if marker in text:
        text = text.split(marker)[0].rstrip() + "\n" + extra
    else:
        text = text.rstrip() + "\n" + extra
    path.write_text(text, encoding="utf-8")
    print("css patched")


def patch_app():
    path = ROOT / "hub/app.js"
    text = path.read_text(encoding="utf-8")
    hook = """(function applyQuery() {
  const p = new URLSearchParams(location.search);
  const sid = p.get("subject");
  if (sid && SID_SUBJECT[sid]) state.subject = sid;
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
    if old_title not in text:
        raise SystemExit("root title not found")
    text = text.replace(old_title, new_title, 1)
    old_desc = '<meta name="description" content="DSE 數學、經濟、化學、生物、物理歷屆試題，按課題集中溫習。">'
    inject = f'''<meta name="description" content="{esc(HUB_DESC)}">
<link rel="canonical" href="{HUB}">
<link rel="alternate" hreflang="zh-Hant-HK" href="{HUB}">
<link rel="alternate" hreflang="x-default" href="{HUB}">
<meta name="robots" content="index, follow">
<meta property="og:type" content="website">
<meta property="og:site_name" content="DSE Hub">
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
        raise SystemExit("root description not found")
    text = text.replace(old_desc, inject, 1)
    noscript = '<noscript><p><a href="/hub/">開啟 DSE 歷屆試題資料庫（DSE Hub）</a>。本站亦有 <a href="/math/">數學</a>、<a href="/econ/">經濟</a>、<a href="/chem/">化學</a>、<a href="/bio/">生物</a>、<a href="/phys/">物理</a> 科目頁。</p></noscript>\n'
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
    if set(topics) != {"math", "econ"}:
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
    if len(qs) < 1000:
        raise SystemExit(f"question parse too small: {len(qs)}")
    return qs


def paper_no(paper):
    m = re.search(r"(\d+[A-Za-z]?)", str(paper or ""))
    return m.group(1).upper() if m else "1"


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
        key=lambda q: (-int(q["year"]), paper_no(q.get("paper")), int(q.get("qno") or 0)),
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


def topic_path(sid, slug):
    return f"/{sid}/{slug}/"


def topic_url_for_name(sid, name):
    slug = TOPIC_SLUG_BY_NAME.get((sid, name))
    return topic_path(sid, slug) if slug else None


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
    parts.append(f'<a href="/hub/">DSE Hub 主頁</a>')
    parts.append(f"相關：{vt}")
    parts.append("站內只放索引、連結同課題標籤，只顯示資料庫已有內容")
    return "<footer>" + " · ".join(parts) + "</footer>"


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
    "DSE Hub 係咪免費？",
    "係，真正完全免費查閱香港中學文憑試歷屆試題索引同題目，唔使報名，亦唔使信用卡。",
)
FAQ_TOPIC = (
    "可唔可以按課題操練？",
    "可以。喺 DSE Hub 揀「按課題」，或者開啟各課題頁，就會列出相關題目，方便集中操同一類型。",
)


def nav_pills(items, current=None, label="相關連結"):
    bits = [f'<nav class="strand-nav" aria-label="{esc(label)}">']
    for href, name, key in items:
        cls = ' class="on"' if current and key == current else ""
        bits.append(f'<a href="{esc(href)}"{cls}>{esc(name)}</a>')
    bits.append("</nav>")
    return "\n        ".join(bits)


def q_list_html(rows, topic=None):
    items = []
    for q in rows:
        label = f"{q['subject']} {q['year']} {paper_zh_label(q.get('paper'))} Q{q['qno']}"
        title = (q.get("title") or "").strip()
        extra = f" — {esc(title)}" if title else ""
        items.append(
            f'    <li><a href="{esc(question_href(q, topic))}"><span class="q-meta">{esc(label)}</span>{extra}</a></li>'
        )
    return '<ul class="q-index">\n' + "\n".join(items) + "\n  </ul>"


def paper_code_of(paper):
    if paper in PAPER_CODE:
        return PAPER_CODE[paper]
    m = re.search(r"(\d+)\s*([A-Da-d])?", str(paper or ""))
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
    if any(x in f for x in ("英文", "ENG", "(EN)", "English")):
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
        key = (sid, int(q["year"]), code, lang)
        q_index.setdefault(key, []).append(q)

    papers = []
    seen = set()
    for r in catalog:
        sid = r["id"]
        code = paper_code_of(r["paper"])
        lang = r["lang"]
        key = (sid, r["year"], code, lang)
        qs = sort_questions(q_index.get(key, []))
        if not qs:
            alts = [
                (lg, rows)
                for (s, y, c, lg), rows in q_index.items()
                if s == sid and y == r["year"] and c == code
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
                "year": r["year"],
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
        seen.add((sid, r["year"], code, lang))

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
    papers.sort(key=lambda r: (r["id"], -r["year"], r["paper_code"], r["lang"]))
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
        links.append(f'<a href="{esc(hub)}">喺 DSE Hub 按課題查看全部 {len(rows)} 題</a>')
    else:
        links.append(f'<a href="{esc(hub_topic_path(sid, kw if not tag_counts else tag_counts[0][0]))}">喺 DSE Hub 按課題篩選</a>')
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
            f"{st['blurb']} 資料庫入面，呢個範疇有 {len(union)} 題對應 "
            f"{len(matched_qs)} 個課題標籤"
        )
        tagline += f"，另有 {unmatched} 個課題暫時未有對應題目。" if unmatched else "。"
        graph = {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "BreadcrumbList",
                    "itemListElement": [
                        {"@type": "ListItem", "position": 1, "name": "DSE Hub", "item": HUB},
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
            ],
        }
        siblings = " · ".join(
            f'<a href="/{x["subject_id"]}/{x["slug"]}/">{esc(x["name"])}</a>'
            for x in STRANDS
            if x["subject_id"] == st["subject_id"]
        )
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
                '      <a href="/hub/">DSE Hub</a>',
                '      <span aria-hidden="true">／</span>',
                f'      <a href="/{st["subject_id"]}/">{esc(s["short"])}</a>',
                '      <span aria-hidden="true">／</span>',
                f"      <span>{esc(st['name'])}</span>",
                "    </nav>",
                '    <p class="brand">DSE Hub</p>',
                f"    <h1>{esc(st['h1'])}</h1>",
                f'    <p class="tagline">{esc(tagline)}</p>',
                f"        {subject_nav(catalog, current=st['subject_id'])}",
                f"        {strand_nav_html(st['subject_id'], current=st['slug'])}",
                f'    <p class="page-cta"><a href="{esc(hub_topic_path(st["subject_id"]))}">按課題篩選{esc(s["short"])}題目</a></p>',
                "  </div>",
                "</header>",
                '<main class="subj-main">',
                '<section class="kw-section" aria-label="課題">',
                f"  <h2>{esc(st['name'])}課題</h2>",
                "\n".join(blocks),
                "</section>",
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


def write_landing(path, title, description, canonical, graph, body_inner, footer_extra=""):
    page = (
        "<!DOCTYPE html>\n"
        '<html lang="zh-Hant-HK">\n'
        "<head>\n"
        f"{seo_head(title, description, canonical)}\n"
        f"{ld_json(graph)}\n"
        "</head>\n"
        '<body class="subj-page">\n'
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
        '    <p class="brand">DSE Hub</p>\n'
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
        by[(p["id"], p["year"])].append(p)
    # Also include years that only appear in the question bank
    for q in questions:
        sid = SUBJECT_TO_SID.get(q.get("subject"))
        if sid:
            by.setdefault((sid, int(q["year"])), [])
    count = 0
    for (sid, year), rows in sorted(by.items(), key=lambda x: (x[0][0], -x[0][1])):
        rows = sort_rows(rows)
        s = subject_meta(sid)
        # questions that year
        yqs = [
            q
            for q in questions
            if q.get("subject") == SID_TO_SUBJECT[sid] and int(q["year"]) == year
        ]
        if not rows and not yqs:
            continue
        path = year_path(sid, year)
        url = SITE + path
        n_papers = len(rows)
        n_qs = len(yqs)
        title = f"免費 DSE {s['short']} {year} 歷屆試題｜DSE Hub"
        desc = (
            f"免費查閱 DSE {s['short']} {year} 年歷屆試題"
            + (f"，資料庫有 {n_papers} 卷" if n_papers else "")
            + (f"、{n_qs} 題索引" if n_qs else "")
            + "。真正完全免費，可按卷或課題操練。"
        )
        h1 = f"DSE {s['short']} {year} 歷屆試題"
        paper_bits = "、".join(f"{r['paper']}（{r['lang']}）" for r in rows) if rows else "相關題目"
        tagline = (
            f"真正完全免費查閱 DSE {esc(s['short'])} {year} 年歷屆試題"
            + (f"，包括 {esc(paper_bits)}" if rows else "")
            + (f"。而家資料庫有 {n_qs} 題索引。" if n_qs else "。")
        )
        hub_link = f"/hub/?subject={sid}&amp;mode=year&amp;year={year}"
        cta = (
            f'<p class="page-cta"><a href="{hub_link}">喺 DSE Hub 按年份睇 {year} 年卷</a>'
            f' · <a href="/{sid}/">返回{esc(s["short"])}科目頁</a></p>'
        )
        sibling_years = year_nav_html(papers, sid, current=year)
        sections = []
        if rows:
            items = "\n".join(paper_row_html(r) for r in rows)
            sections.append(
                f'<section class="year-group">\n  <h2>{year} 年各卷</h2>\n  <div class="paper-list">\n{items}\n  </div>\n</section>'
            )
        # topics that have questions this year
        topic_hits = []
        for tp in TOPIC_PAGES:
            if tp["subject_id"] != sid:
                continue
            n = len(
                [
                    q
                    for q in yqs
                    if set(q.get("tags") or []) & set(tp["tags"])
                ]
            )
            if n:
                topic_hits.append((topic_path(sid, tp["slug"]), f"{tp['name']}（{n}）", tp["slug"]))
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
        crumbs = [("/hub/", "DSE Hub"), (f"/{sid}/", s["short"]), (None, str(year))]
        graph = {
            "@context": "https://schema.org",
            "@graph": [
                ld_breadcrumb([("/hub/", "DSE Hub"), (f"/{sid}/", s["short"]), (url, str(year))]),
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
                    "mainEntity": [
                        {
                            "@type": "Question",
                            "name": FAQ_FREE[0],
                            "acceptedAnswer": {"@type": "Answer", "text": FAQ_FREE[1]},
                        },
                        {
                            "@type": "Question",
                            "name": FAQ_TOPIC[0],
                            "acceptedAnswer": {"@type": "Answer", "text": FAQ_TOPIC[1]},
                        },
                    ],
                },
            ],
        }
        body = hero_html(crumbs, h1, tagline, catalog, sid, extra_nav=extra_nav, cta=cta)
        body += '<main class="subj-main">\n' + "\n".join(sections) + "\n" + faq_block([FAQ_FREE, FAQ_TOPIC]) + "\n</main>"
        write_landing(path, title, desc, url, graph, body, footer_extra=f'<a href="/{sid}/">返回{esc(s["short"])}科目頁</a>')
        add_sitemap(url, "0.8", "weekly")
        count += 1
        print("year", path, "papers", n_papers, "qs", n_qs)
    print("year pages", count)
    return count


def make_paper_pages(catalog, papers, questions):
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
        title = f"免費 DSE {s['short']} {r['year']} {r['paper']}（{r['lang']}）歷屆試題｜DSE Hub"
        desc = (
            f"免費查閱 DSE {s['short']} {r['year']} 年{r['paper']}（{r['lang']}）歷屆試題"
            + (f"，資料庫有 {nq} 題索引，可逐題開啟。" if nq else "。可喺 DSE Hub 開啟呢份卷。")
            + "真正完全免費。"
        )
        h1 = f"DSE {s['short']} {r['year']} {r['paper']}（{r['lang']}）"
        tagline = (
            f"真正完全免費查閱 DSE {esc(s['short'])} {r['year']} 年{esc(r['paper'])}（{esc(r['lang'])}）"
            + (f"。資料庫有 {nq} 題索引。" if nq else "。逐題索引稍後再補，你仍然可以喺題庫開啟呢份卷。")
        )
        open_href = paper_href(r)
        hub_qs = f"/hub/?subject={r['id']}&amp;mode=year&amp;year={r['year']}&amp;paper={quote(r['paper'], safe='')}"
        cta = (
            f'<p class="page-cta open-cta"><a href="{esc(open_href)}">喺題庫開啟呢份卷</a>'
            f' · <a href="{hub_qs}">喺 DSE Hub 篩選呢一年</a></p>'
        )
        siblings = [
            (p["path"], f"{p['paper']}（{p['lang']}）", p["path"])
            for p in sort_rows(by_year[(r["id"], r["year"])])
        ]
        extra_nav = year_nav_html(papers, r["id"], current=r["year"])
        if siblings:
            extra_nav += "\n        " + nav_pills(siblings, current=r["path"], label="同年試卷")
        crumbs = [
            ("/hub/", "DSE Hub"),
            (f"/{r['id']}/", s["short"]),
            (year_path(r["id"], r["year"]), str(r["year"])),
            (None, f"{r['paper']}（{r['lang']}）"),
        ]
        sections = []
        if nq:
            sections.append(
                f'<section class="kw-section" aria-label="題目索引">\n  <h2>題目索引（{nq} 題）</h2>\n  '
                + q_list_html(qs)
                + "\n</section>"
            )
        else:
            sections.append(
                '<section class="kw-block">\n  <h2>題目索引</h2>\n'
                "  <p>呢份卷已收錄喺資料庫目錄，可以喺題庫開啟；逐題索引稍後再補。</p>\n"
                f'  <p><a href="{esc(open_href)}">開啟 {esc(s["short"])} {r["year"]} {esc(r["paper"])}</a></p>\n'
                "</section>"
            )
        graph = {
            "@context": "https://schema.org",
            "@graph": [
                ld_breadcrumb(
                    [
                        ("/hub/", "DSE Hub"),
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
        years = sorted({int(q["year"]) for q in rows})
        span = f"{years[0]}" if len(years) == 1 else f"{years[0]}–{years[-1]}"
        title = tp["title"]
        desc = tp["description"]
        h1 = tp["h1"]
        tagline = (
            f"{esc(tp['blurb'])} 資料庫有 {len(rows)} 題（{esc(span)}），真正完全免費按課題操練。"
        )
        hub = hub_topic_path(sid)
        cta = (
            f'<p class="page-cta"><a href="{esc(hub)}">喺 DSE Hub 按課題篩選{esc(s["short"])}題目</a>'
            f' · <a href="/{sid}/">返回{esc(s["short"])}科目頁</a></p>'
        )
        extra_nav = topic_nav_html(sid, current=tp["slug"])
        if tp.get("strand"):
            extra_nav = (
                nav_pills(
                    [
                        (f"/{st['subject_id']}/{st['slug']}/", st["name"], st["slug"])
                        for st in STRANDS
                        if st["subject_id"] == sid
                    ],
                    current=tp["strand"],
                    label="課題範疇",
                )
                + "\n        "
                + extra_nav
            )
        year_hits = nav_pills(
            [
                (year_path(sid, y), str(y), y)
                for y in sorted({int(q["year"]) for q in rows}, reverse=True)
            ],
            label="年份",
        )
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
        sections = [
            '<section class="strand-index" aria-label="相關標籤">\n'
            "  <h2>相關題目標籤</h2>\n"
            '  <nav class="strand-nav">\n    '
            + tag_html
            + "\n  </nav>\n</section>",
            f'<section class="strand-index" aria-label="出現年份">\n  <h2>出現年份</h2>\n  {year_hits}\n</section>',
            f'<section class="kw-section" aria-label="題目索引">\n  <h2>題目索引（{len(rows)} 題）</h2>\n  '
            + q_list_html(rows, topic=tp["name"])
            + "\n</section>",
        ]
        crumbs = [("/hub/", "DSE Hub"), (f"/{sid}/", s["short"])]
        crumb_ld = [("/hub/", "DSE Hub"), (f"/{sid}/", s["short"])]
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
                    "mainEntity": [
                        {
                            "@type": "Question",
                            "name": FAQ_FREE[0],
                            "acceptedAnswer": {"@type": "Answer", "text": FAQ_FREE[1]},
                        },
                        {
                            "@type": "Question",
                            "name": FAQ_TOPIC[0],
                            "acceptedAnswer": {"@type": "Answer", "text": FAQ_TOPIC[1]},
                        },
                    ],
                },
            ],
        }
        body = hero_html(crumbs, h1, tagline, catalog, sid, extra_nav=extra_nav, cta=cta)
        body += '<main class="subj-main">\n' + "\n".join(sections) + "\n" + faq_block([FAQ_FREE, FAQ_TOPIC]) + "\n</main>"
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
        ROOT / "chem/2024/paper-1a/index.html": ["化學 2024", "卷一甲", "G-LTB27V0RGW"],
        ROOT / "sitemap.xml": ["https://hkdse.exampaper.cloud/hub/"],
        ROOT / "hub/index.html": ["G-LTB27V0RGW", VISUAL_TUTOR],
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
    sm = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    if f"<loc>{SITE}</loc>" in sm or f"<loc>{SITE}/</loc>" in sm:
        raise SystemExit("sitemap includes domain root")
    if ".pdf" in sm.lower():
        raise SystemExit("sitemap includes pdf")
    print("sanity check ok", "sitemap urls", len({u[0] for u in SITEMAP_URLS}))


def main():
    global SITEMAP_URLS
    SITEMAP_URLS = []
    catalog = parse_catalog()
    topics = parse_topics()
    questions = parse_questions()
    papers = collect_papers(catalog, questions)
    print("catalog", len(catalog), "questions", len(questions), "papers", len(papers))
    make_og()
    make_htaccess()
    make_robots()
    make_hub(catalog)
    make_subject_pages(catalog, papers)
    make_strand_pages(catalog, questions, topics)
    n_year = make_year_pages(catalog, papers, questions)
    n_paper = make_paper_pages(catalog, papers, questions)
    n_topic = make_topic_pages(catalog, questions, papers)
    make_sitemap()
    patch_css()
    patch_app()
    patch_root_index()
    patch_sw()
    sanity_check()
    print("SEO build complete", "years", n_year, "papers", n_paper, "topics", n_topic)


if __name__ == "__main__":
    main()
