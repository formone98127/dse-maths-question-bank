/* ===== DSE Hub — 只放電子題庫已有嘅卷 ===== */

const BANK_URL = "https://formone98127.github.io/dse-maths-question-bank/";

/**
 * 每條 = 資料庫真實有嘅一卷
 * lang: 中文 | 英文
 * hash: 逐題睇深連結
 */
const CATALOG = [
  /* 數學（中文卷） */
  { id: "math", name: "數學（必修部分）", year: 2012, paper: "卷一", lang: "中文", hash: "#2012P1Q1" },
  { id: "math", name: "數學（必修部分）", year: 2012, paper: "卷二", lang: "中文", hash: "#2012P2Q1" },
  { id: "math", name: "數學（必修部分）", year: 2013, paper: "卷一", lang: "中文", hash: "#2013P1Q1" },
  { id: "math", name: "數學（必修部分）", year: 2013, paper: "卷二", lang: "中文", hash: "#2013P2Q1" },
  { id: "math", name: "數學（必修部分）", year: 2014, paper: "卷一", lang: "中文", hash: "#2014P1Q1" },
  { id: "math", name: "數學（必修部分）", year: 2015, paper: "卷二", lang: "中文", hash: "#2015P2Q1" },
  /* 經濟（英文卷） */
  { id: "econ", name: "經濟", year: 2015, paper: "卷一", lang: "英文", hash: "#econ2015P1Q1" },
  { id: "econ", name: "經濟", year: 2017, paper: "卷一", lang: "英文", hash: "#econ2017P1Q1" },
  { id: "econ", name: "經濟", year: 2020, paper: "卷一", lang: "英文", hash: "#econ2020P1Q1" },
];

/* 按課題：只為資料庫有嘅科目提供 */
const TOPICS = {
  math: {
    "數與代數": ["百分法", "指數與對數", "比、率與比例", "多項式（續）", "數系", "方程與不等式", "函數與圖像", "數列", "變分"],
    "度量、圖形與空間": ["三角學與解三角形", "求積法", "坐標幾何：直線", "坐標幾何：圓", "圓形幾何", "軌跡", "幾何變換"],
    "數據處理": ["統計圖表", "集中趨勢與離差", "概率", "排列與組合"],
  },
};

const PDF_LINKS = {};
