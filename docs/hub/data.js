/* ===== DSE 試題資料庫 — 資料檔 ===== */

/* 數學電子題庫（已上線嘅卷） */
const BANK_URL = "https://formone98127.github.io/dse-maths-question-bank/";
const BANK_DONE = {
  2012: ["卷一", "卷二"],
  2013: ["卷一", "卷二"],
  2014: ["卷一"],
  2015: ["卷二"],
};

/* 年份：新至舊 */
const YEARS = [2026, 2025, 2024, 2023, 2022, 2021, 2020, 2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012];

/*
  subject 欄位：
  - id / cat（核心科目｜選修科目）/ name
  - years：[起, 終]（null = 2012–2026 全部）
  - papers：卷別陣列；或 fn(year) 傳回該年卷別
  - bank：數學已上線嘅卷（連去電子題庫）
  - topics：{ 範疇: [課題...] }（按課題模式用）
  - note：卷別備註
*/
const SUBJECTS = [
  /* ---- 核心科目 ---- */
  {
    id: "math", cat: "核心科目", name: "數學（必修部分）",
    papers: ["卷一", "卷二"],
    bank: BANK_DONE,
    topics: {
      "數與代數": ["百分法", "指數與對數", "比、率與比例", "多項式（續）", "數系", "方程與不等式", "函數與圖像", "數列", "變分"],
      "度量、圖形與空間": ["三角學與解三角形", "求積法", "坐標幾何：直線", "坐標幾何：圓", "圓形幾何", "軌跡", "幾何變換"],
      "數據處理": ["統計圖表", "集中趨勢與離差", "概率", "排列與組合"],
    },
  },
  {
    id: "chi", cat: "核心科目", name: "中國語文",
    papers: ["卷一 閱讀", "卷二 寫作", "卷三 聆聽", "卷四 說話", "卷五 綜合能力"],
    note: "卷別 2024 起有調整，以官方公布為準",
  },
  {
    id: "eng", cat: "核心科目", name: "英國語文",
    papers: ["Paper 1 Reading", "Paper 2 Writing", "Paper 3 Listening", "Paper 4 Speaking"],
    note: "卷別以官方公布為準",
  },
  {
    id: "ls", cat: "核心科目", name: "通識教育",
    years: [2012, 2023],
    papers: ["卷一", "卷二"],
  },
  {
    id: "csc", cat: "核心科目", name: "公民與社會發展",
    years: [2024, 2026],
    papers: ["卷一"],
  },

  /* ---- 選修科目（先放熱門，陸續加） ---- */
  { id: "m12", cat: "選修科目", name: "數學延伸部分（M1／M2）", papers: ["M1 卷一", "M2 卷一"] },
  { id: "phy", cat: "選修科目", name: "物理", papers: ["卷一", "卷二"] },
  { id: "chem", cat: "選修科目", name: "化學", papers: ["卷一", "卷二"] },
  { id: "bio", cat: "選修科目", name: "生物", papers: ["卷一", "卷二"] },
  { id: "econ", cat: "選修科目", name: "經濟", papers: ["卷一", "卷二"],
    bank: { 2015: ["卷一"], 2017: ["卷一"], 2020: ["卷一"] }, bankTpl: "econ{Y}P1Q1" },
  { id: "bafs", cat: "選修科目", name: "企業、會計與財務概論", papers: ["卷一", "卷二A 會計", "卷二B 商業管理"] },
  { id: "ict", cat: "選修科目", name: "資訊及通訊科技", papers: ["卷一", "卷二"] },
  { id: "chist", cat: "選修科目", name: "中國歷史", papers: ["卷一", "卷二"] },
  { id: "hist", cat: "選修科目", name: "歷史", papers: ["卷一", "卷二"] },
  { id: "geog", cat: "選修科目", name: "地理", papers: ["卷一"] },
];

/* PDF 來源（Phase 2 逐條核實後填入）；結構：{ "<subjectId>|<year>|<paper>": url } */
const PDF_LINKS = {};
