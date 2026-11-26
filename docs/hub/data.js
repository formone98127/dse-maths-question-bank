/* ===== DSE Hub — 只放電子題庫已有的試卷 ===== */

const BANK_URL = "https://hkdse.exampaper.cloud/";

/**
 * 每條 = 資料庫真實有的一卷
 * lang: 中文 | 英文
 * hash: 逐題深層連結
 */
const CATALOG = [
  { id: "m2", name: "數學（延伸部分 M2）", year: 2025, paper: "M2", lang: "英文", hash: "#2025P2MQ1" , path: "/m2/2025/paper-1-en/"},
  { id: "m2", name: "數學（延伸部分 M2）", year: 2024, paper: "M2", lang: "英文", hash: "#2024P2MQ1" , path: "/m2/2024/paper-1-en/"},
  { id: "m2", name: "數學（延伸部分 M2）", year: 2023, paper: "M2", lang: "英文", hash: "#2023P2MQ1" , path: "/m2/2023/paper-1-en/"},
  { id: "m2", name: "數學（延伸部分 M2）", year: 2022, paper: "M2", lang: "英文", hash: "#2022P2MQ1" , path: "/m2/2022/paper-1-en/"},
  { id: "m2", name: "數學（延伸部分 M2）", year: 2021, paper: "M2", lang: "英文", hash: "#2021P2MQ1" , path: "/m2/2021/paper-1-en/"},
  { id: "m2", name: "數學（延伸部分 M2）", year: 2020, paper: "M2", lang: "英文", hash: "#2020P2MQ1" , path: "/m2/2020/paper-1-en/"},
  { id: "m2", name: "數學（延伸部分 M2）", year: 2018, paper: "M2", lang: "英文", hash: "#2018P2MQ1" , path: "/m2/2018/paper-1-en/"},
  { id: "m2", name: "數學（延伸部分 M2）", year: 2015, paper: "M2", lang: "英文", hash: "#2015P2MQ1" , path: "/m2/2015/paper-1-en/"},
  { id: "m1", name: "數學（延伸部分 M1）", year: 2012, paper: "M1", lang: "英文", hash: "#2012P1MQ1" , path: "/m1/2012/paper-1-en/"},
  { id: "m1", name: "數學（延伸部分 M1）", year: 2013, paper: "M1", lang: "英文", hash: "#2013P1MQ1" , path: "/m1/2013/paper-1-en/"},
  { id: "m1", name: "數學（延伸部分 M1）", year: 2014, paper: "M1", lang: "英文", hash: "#2014P1MQ1" , path: "/m1/2014/paper-1-en/"},
  { id: "m1", name: "數學（延伸部分 M1）", year: 2015, paper: "M1", lang: "英文", hash: "#2015P1MQ1" , path: "/m1/2015/paper-1-en/"},
  { id: "m1", name: "數學（延伸部分 M1）", year: 2016, paper: "M1", lang: "英文", hash: "#2016P1MQ1" , path: "/m1/2016/paper-1-en/"},
  { id: "m1", name: "數學（延伸部分 M1）", year: 2017, paper: "M1", lang: "英文", hash: "#2017P1MQ1" , path: "/m1/2017/paper-1-en/"},
  { id: "m1", name: "數學（延伸部分 M1）", year: 2018, paper: "M1", lang: "英文", hash: "#2018P1MQ1" , path: "/m1/2018/paper-1-en/"},
  { id: "m1", name: "數學（延伸部分 M1）", year: 2021, paper: "M1", lang: "英文", hash: "#2021P1MQ1" , path: "/m1/2021/paper-1-en/"},
  /* 數學（中文卷） */
  /* 經濟（英文卷） */
  /* 化學／生物／物理（第 2 層中文；先上線後校對） */
  /* 樣本試卷 / 練習卷（year 用字串，hub 會顯示「樣本試卷」「練習卷」） */
  { id: "math", name: "數學（必修部分）", year: 2025, paper: "卷一", lang: "英文", hash: "#2025P1Q1" , path: "https://hkdse.exampaper.cloud/#2025P1Q1"},
  { id: "m1", name: "數學（延伸部分 M1）", year: 2025, paper: "M1", lang: "英文", hash: "#2025P1MQ1" , path: "/m1/2025/paper-1-en/"},
  { id: "math", name: "數學（必修部分）", year: 2025, paper: "卷二", lang: "中文", hash: "#2025P2Q1" , path: "https://hkdse.exampaper.cloud/#2025P2Q1"},
  { id: "math", name: "數學（必修部分）", year: 2025, paper: "卷二", lang: "英文", hash: "#2025P2Q1" , path: "https://hkdse.exampaper.cloud/#2025P2Q1"},
  { id: "math", name: "數學（必修部分）", year: 2024, paper: "卷一", lang: "中文", hash: "#2024P1Q1" , path: "https://hkdse.exampaper.cloud/#2024P1Q1"},
  { id: "math", name: "數學（必修部分）", year: 2024, paper: "卷一", lang: "英文", hash: "#2024P1Q1" , path: "https://hkdse.exampaper.cloud/#2024P1Q1"},
  { id: "m1", name: "數學（延伸部分 M1）", year: 2024, paper: "M1", lang: "英文", hash: "#2024P1MQ1" , path: "/m1/2024/paper-1-en/"},
  { id: "math", name: "數學（必修部分）", year: 2024, paper: "卷二", lang: "中文", hash: "#2024P2Q1" , path: "https://hkdse.exampaper.cloud/#2024P2Q1"},
  { id: "math", name: "數學（必修部分）", year: 2024, paper: "卷二", lang: "英文", hash: "#2024P2Q1" , path: "https://hkdse.exampaper.cloud/#2024P2Q1"},
  { id: "math", name: "數學（必修部分）", year: 2023, paper: "卷一", lang: "中文", hash: "#2023P1Q1" , path: "https://hkdse.exampaper.cloud/#2023P1Q1"},
  { id: "math", name: "數學（必修部分）", year: 2023, paper: "卷一", lang: "英文", hash: "#2023P1Q1" , path: "https://hkdse.exampaper.cloud/#2023P1Q1"},
  { id: "m1", name: "數學（延伸部分 M1）", year: 2023, paper: "M1", lang: "英文", hash: "#2023P1MQ1" , path: "/m1/2023/paper-1-en/"},
  { id: "math", name: "數學（必修部分）", year: 2023, paper: "卷二", lang: "中文", hash: "#2023P2Q1" , path: "https://hkdse.exampaper.cloud/#2023P2Q1"},
  { id: "math", name: "數學（必修部分）", year: 2023, paper: "卷二", lang: "英文", hash: "#2023P2Q1" , path: "https://hkdse.exampaper.cloud/#2023P2Q1"},
  { id: "math", name: "數學（必修部分）", year: 2022, paper: "卷一", lang: "中文", hash: "#2022P1Q1" , path: "https://hkdse.exampaper.cloud/#2022P1Q1"},
  { id: "math", name: "數學（必修部分）", year: 2022, paper: "卷一", lang: "英文", hash: "#2022P1Q1" , path: "https://hkdse.exampaper.cloud/#2022P1Q1"},
  { id: "m1", name: "數學（延伸部分 M1）", year: 2022, paper: "M1", lang: "英文", hash: "#2022P1MQ1" , path: "/m1/2022/paper-1-en/"},
  { id: "math", name: "數學（必修部分）", year: 2022, paper: "卷二", lang: "英文", hash: "#2022P2Q1" , path: "https://hkdse.exampaper.cloud/#2022P2Q1"},
  { id: "math", name: "數學（必修部分）", year: 2021, paper: "卷一", lang: "中文", hash: "#2021P1Q1" , path: "https://hkdse.exampaper.cloud/#2021P1Q1"},
  { id: "math", name: "數學（必修部分）", year: 2021, paper: "卷一", lang: "英文", hash: "#2021P1Q1" , path: "https://hkdse.exampaper.cloud/#2021P1Q1"},
  { id: "math", name: "數學（必修部分）", year: 2021, paper: "卷二", lang: "中文", hash: "#2021P2Q1" , path: "https://hkdse.exampaper.cloud/#2021P2Q1"},
  { id: "math", name: "數學（必修部分）", year: 2021, paper: "卷二", lang: "英文", hash: "#2021P2Q1" , path: "https://hkdse.exampaper.cloud/#2021P2Q1"},
  { id: "math", name: "數學（必修部分）", year: 2020, paper: "卷一", lang: "中文", hash: "#2020P1Q1" , path: "https://hkdse.exampaper.cloud/#2020P1Q1"},
  { id: "math", name: "數學（必修部分）", year: 2020, paper: "卷一", lang: "英文", hash: "#2020P1Q1" , path: "https://hkdse.exampaper.cloud/#2020P1Q1"},
  { id: "m1", name: "數學（延伸部分 M1）", year: 2020, paper: "M1", lang: "英文", hash: "#2020P1MQ1" , path: "/m1/2020/paper-1-en/"},
  { id: "math", name: "數學（必修部分）", year: 2020, paper: "卷二", lang: "中文", hash: "#2020P2Q1" , path: "https://hkdse.exampaper.cloud/#2020P2Q1"},
  { id: "math", name: "數學（必修部分）", year: 2020, paper: "卷二", lang: "英文", hash: "#2020P2Q1" , path: "https://hkdse.exampaper.cloud/#2020P2Q1"},
  { id: "math", name: "數學（必修部分）", year: 2019, paper: "卷一", lang: "中文", hash: "#2019P1Q1" , path: "https://hkdse.exampaper.cloud/#2019P1Q1"},
  { id: "math", name: "數學（必修部分）", year: 2019, paper: "卷一", lang: "英文", hash: "#2019P1Q1" , path: "https://hkdse.exampaper.cloud/#2019P1Q1"},
  { id: "m1", name: "數學（延伸部分 M1）", year: 2019, paper: "M1", lang: "英文", hash: "#2019P1MQ1" , path: "/m1/2019/paper-1-en/"},
  { id: "math", name: "數學（必修部分）", year: 2019, paper: "卷二", lang: "中文", hash: "#2019P2Q1" , path: "https://hkdse.exampaper.cloud/#2019P2Q1"},
  { id: "math", name: "數學（必修部分）", year: 2019, paper: "卷二", lang: "英文", hash: "#2019P2Q1" , path: "https://hkdse.exampaper.cloud/#2019P2Q1"},
  { id: "math", name: "數學（必修部分）", year: 2018, paper: "卷一", lang: "中文", hash: "#2018P1Q1" , path: "https://hkdse.exampaper.cloud/#2018P1Q1"},
  { id: "math", name: "數學（必修部分）", year: 2018, paper: "卷一", lang: "英文", hash: "#2018P1Q1" , path: "https://hkdse.exampaper.cloud/#2018P1Q1"},
  { id: "math", name: "數學（必修部分）", year: 2018, paper: "卷二", lang: "中文", hash: "#2018P2Q1" , path: "https://hkdse.exampaper.cloud/#2018P2Q1"},
  { id: "math", name: "數學（必修部分）", year: 2018, paper: "卷二", lang: "英文", hash: "#2018P2Q1" , path: "https://hkdse.exampaper.cloud/#2018P2Q1"},
  { id: "math", name: "數學（必修部分）", year: 2017, paper: "卷一", lang: "中文", hash: "#2017P1Q1" , path: "https://hkdse.exampaper.cloud/#2017P1Q1"},
  { id: "math", name: "數學（必修部分）", year: 2017, paper: "卷一", lang: "英文", hash: "#2017P1Q1" , path: "https://hkdse.exampaper.cloud/#2017P1Q1"},
  { id: "math", name: "數學（必修部分）", year: 2017, paper: "卷二", lang: "中文", hash: "#2017P2Q1" , path: "https://hkdse.exampaper.cloud/#2017P2Q1"},
  { id: "math", name: "數學（必修部分）", year: 2017, paper: "卷二", lang: "英文", hash: "#2017P2Q1" , path: "https://hkdse.exampaper.cloud/#2017P2Q1"},
  { id: "math", name: "數學（必修部分）", year: 2016, paper: "卷一", lang: "中文", hash: "#2016P1Q1" , path: "https://hkdse.exampaper.cloud/#2016P1Q1"},
  { id: "math", name: "數學（必修部分）", year: 2016, paper: "卷一", lang: "英文", hash: "#2016P1Q1" , path: "https://hkdse.exampaper.cloud/#2016P1Q1"},
  { id: "math", name: "數學（必修部分）", year: 2016, paper: "卷二", lang: "中文", hash: "#2016P2Q1" , path: "https://hkdse.exampaper.cloud/#2016P2Q1"},
  { id: "math", name: "數學（必修部分）", year: 2016, paper: "卷二", lang: "英文", hash: "#2016P2Q1" , path: "https://hkdse.exampaper.cloud/#2016P2Q1"},
  { id: "math", name: "數學（必修部分）", year: 2015, paper: "卷一", lang: "中文", hash: "#2015P1Q1" , path: "https://hkdse.exampaper.cloud/#2015P1Q1"},
  { id: "math", name: "數學（必修部分）", year: 2015, paper: "卷一", lang: "英文", hash: "#2015P1Q1" , path: "https://hkdse.exampaper.cloud/#2015P1Q1"},
  { id: "math", name: "數學（必修部分）", year: 2015, paper: "卷二", lang: "中文", hash: "#2015P2Q1" , path: "https://hkdse.exampaper.cloud/#2015P2Q1"},
  { id: "math", name: "數學（必修部分）", year: 2015, paper: "卷二", lang: "英文", hash: "#2015P2Q1" , path: "https://hkdse.exampaper.cloud/#2015P2Q1"},
  { id: "math", name: "數學（必修部分）", year: 2014, paper: "卷一", lang: "中文", hash: "#2014P1Q1" , path: "https://hkdse.exampaper.cloud/#2014P1Q1"},
  { id: "math", name: "數學（必修部分）", year: 2014, paper: "卷一", lang: "英文", hash: "#2014P1Q1" , path: "https://hkdse.exampaper.cloud/#2014P1Q1"},
  { id: "math", name: "數學（必修部分）", year: 2014, paper: "卷二", lang: "中文", hash: "#2014P2Q1" , path: "https://hkdse.exampaper.cloud/#2014P2Q1"},
  { id: "math", name: "數學（必修部分）", year: 2014, paper: "卷二", lang: "英文", hash: "#2014P2Q1" , path: "https://hkdse.exampaper.cloud/#2014P2Q1"},
  { id: "math", name: "數學（必修部分）", year: 2013, paper: "卷一", lang: "中文", hash: "#2013P1Q1" , path: "https://hkdse.exampaper.cloud/#2013P1Q1"},
  { id: "math", name: "數學（必修部分）", year: 2013, paper: "卷一", lang: "英文", hash: "#2013P1Q1" , path: "https://hkdse.exampaper.cloud/#2013P1Q1"},
  { id: "math", name: "數學（必修部分）", year: 2013, paper: "卷二", lang: "中文", hash: "#2013P2Q1" , path: "https://hkdse.exampaper.cloud/#2013P2Q1"},
  { id: "math", name: "數學（必修部分）", year: 2013, paper: "卷二", lang: "英文", hash: "#2013P2Q1" , path: "https://hkdse.exampaper.cloud/#2013P2Q1"},
  { id: "math", name: "數學（必修部分）", year: 2012, paper: "卷一", lang: "中文", hash: "#2012P1Q1" , path: "https://hkdse.exampaper.cloud/#2012P1Q1"},
  { id: "math", name: "數學（必修部分）", year: 2012, paper: "卷一", lang: "英文", hash: "#2012P1Q1" , path: "https://hkdse.exampaper.cloud/#2012P1Q1"},
  { id: "math", name: "數學（必修部分）", year: 2012, paper: "卷二", lang: "中文", hash: "#2012P2Q1" , path: "https://hkdse.exampaper.cloud/#2012P2Q1"},
  { id: "math", name: "數學（必修部分）", year: 2012, paper: "卷二", lang: "英文", hash: "#2012P2Q1" , path: "https://hkdse.exampaper.cloud/#2012P2Q1"},
  { id: "math", name: "數學（必修部分）", year: "PP", paper: "卷一", lang: "中文", hash: "#PPP1Q1" , path: "https://hkdse.exampaper.cloud/#PPP1Q1"},
  { id: "math", name: "數學（必修部分）", year: "SP", paper: "卷一", lang: "中文", hash: "#SPP1Q1" , path: "https://hkdse.exampaper.cloud/#SPP1Q1"},
  { id: "math", name: "數學（必修部分）", year: "PP", paper: "卷一", lang: "英文", hash: "#PPP1Q1" , path: "https://hkdse.exampaper.cloud/#PPP1Q1"},
  { id: "m1", name: "數學（延伸部分 M1）", year: "PP", paper: "M1", lang: "英文", hash: "#PPP1MQ1" , path: "https://hkdse.exampaper.cloud/#PPP1MQ1"},
];

/* 按課題：只為資料庫有的科目提供（葉節點對齊電子題庫 tags） */
const TOPICS = {
  math: {
    "數與代數": ["百分法", "指數與對數", "比、率與比例", "多項式（續）", "數系", "方程與不等式", "函數與圖像", "數列", "變分"],
    "度量、圖形與空間": ["三角學與解三角形", "求積法", "坐標幾何：直線", "坐標幾何：圓", "圓形幾何", "軌跡", "幾何變換"],
    "數據處理": ["統計圖表", "集中趨勢與離差", "概率", "排列與組合"],
  },
};

/* 全卷 PDF → 本站直連檔（點擊即下載，不跳轉 dsepaper.hk 頁面） */
const PDF_LINKS = {
  "math|2012|卷一": "../papers/math-2012-p1.pdf",
  "math|2012|卷二": "../papers/math-2012-p2.pdf",
  "math|2013|卷一": "../papers/math-2013-p1.pdf",
  "math|2013|卷二": "../papers/math-2013-p2.pdf",
  "math|2014|卷一": "../papers/math-2014-p1.pdf",
  "math|2015|卷二": "../papers/math-2015-p2.pdf",
  "econ|2015|卷一": "../papers/econ-2015-p1.pdf",
  "econ|2017|卷一": "../papers/econ-2017-p1.pdf",
  "econ|2020|卷一": "../papers/econ-2020-p1.pdf",
};
