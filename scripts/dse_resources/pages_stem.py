# -*- coding: utf-8 -*-
"""Math, M1, M2, Chemistry, Economics, Physics, Biology resource pages."""
from .template import COPYRIGHT_NOTE, card_link, official_links_html, render_page

HUB = ("/hub/", "DSE Hub")


def C(*p):
    return [HUB, *p]


def nav(links):
    items = "\n".join(f'        <a href="{h}">{n}</a>' for h, n in links)
    return f'<nav class="strand-nav" aria-label="科目資源">\n{items}\n        </nav>'


MATH_TOPICS = [
    ("/math/number-and-algebra/", "數與代數"),
    ("/math/exponents-logarithms/", "指數與對數"),
    ("/math/ratio-rate-proportion/", "比、率與比例"),
    ("/math/polynomials-factorization/", "多項式與因式分解"),
    ("/math/number-systems/", "數系"),
    ("/math/equations-inequalities/", "方程與不等式"),
    ("/math/percentages-interest/", "百分法與利息"),
    ("/math/functions-graphs/", "函數與圖像"),
    ("/math/sequences/", "數列"),
    ("/math/variations/", "變分"),
    ("/math/measures-shape-space/", "度量、圖形與空間"),
    ("/math/trigonometry/", "三角學與解三角形"),
    ("/math/coordinate-geometry-line/", "坐標幾何：直線"),
    ("/math/coordinate-geometry-circle/", "坐標幾何：圓"),
    ("/math/circle-geometry/", "圓形幾何"),
    ("/math/geometric-transformations/", "幾何變換"),
    ("/math/mensuration/", "求積法"),
    ("/math/plane-geometry-similar-triangles/", "平面幾何與相似三角形"),
    ("/math/data-handling/", "數據處理"),
    ("/math/statistical-graphs/", "統計圖表"),
    ("/math/central-tendency-dispersion/", "集中趨勢與離差"),
    ("/math/probability/", "概率"),
    ("/math/permutations-combinations/", "排列與組合"),
    ("/math/calculator/", "Casio 計算機程式"),
]

CHEM_TOPICS = [
    ("/chem/stoichiometry/", "化學計量"),
    ("/chem/bonding-structure/", "鍵合與結構"),
    ("/chem/metals-periodic-table/", "金屬與週期表"),
    ("/chem/acids-bases/", "酸鹼"),
    ("/chem/redox/", "氧化還原"),
    ("/chem/electrolysis-electrochemistry/", "電解與電化學"),
    ("/chem/reaction-rate/", "反應速率"),
    ("/chem/chemical-equilibrium/", "化學平衡"),
    ("/chem/thermochemistry/", "熱化學"),
    ("/chem/organic-chemistry/", "有機化學"),
]

ECON_TOPICS = [
    ("/econ/basic-concepts/", "基本經濟概念"),
    ("/econ/production-firms/", "生產與企業"),
    ("/econ/market-and-price/", "市場與價格"),
    ("/econ/market-structure/", "市場結構與競爭"),
    ("/econ/efficiency-equity-government/", "效率、公平與政府角色"),
    ("/econ/measuring-performance/", "經濟表現量度"),
    ("/econ/national-income-price-level/", "國民收入與價格水平"),
    ("/econ/money-and-banking/", "貨幣與銀行"),
    ("/econ/macro-problems-policy/", "宏觀經濟問題與政策"),
    ("/econ/international-trade-finance/", "國際貿易與金融"),
]


def _topic_links(pairs):
    return "\n".join(f'<a href="{h}">{n}</a>' for h, n in pairs)


FORMULA_DISCLAIMER = (
    '<p class="res-note"><strong>公式表聲明：</strong>'
    "呢份係原創溫習清單，用自己嘅措辭整理常見關係同應試注意。"
    "正式考試請同時核對試卷或考評局提供嘅官方公式表，符號同適用條件以當年卷面為準。"
    "記得：有公式都要寫出代入過程，唔好只抄最後答案。</p>"
)


def page_math_formulas():
    topics = _topic_links(MATH_TOPICS)
    body = f"""
{COPYRIGHT_NOTE}
{FORMULA_DISCLAIMER}
<section class="res-sec">
  <h2>點樣同現有課題頁一齊用</h2>
  <p>數學必修部分已有按課題整理嘅歷屆題目頁，亦有 Casio 程式庫。呢頁唔取代官方公式表，而係幫你喺操卷前快速檢查：邊啲關係要熟、邊啲題型最常漏條件。詳細題目請行下面課題頁或<a href="/math/">數學科目頁</a>。</p>
  <nav class="res-toc" aria-label="課題頁">{topics}</nav>
</section>
<section class="res-sec">
  <h2>數與代數：常要用到嘅關係</h2>
  <ul>
    <li>定律同指數：乘除同一底數時指數相加或相減；乘方時指數相乘。遇到根式，先改寫成分數指數再算，最後先還原。負指數代表倒數，唔好當成負數。</li>
    <li>對數：只在真數為正時有定義。對數加法對應真數相乘。換底公式用嚟把冷門底轉到計數機可處理嘅底。</li>
    <li>二次方程：先判斷能不能因式分解；否則用公式。判别式決定實根數目。求根同系數關係前，先確認二次項系數唔係零，並留意根嘅限制（例如長度必須為正）。</li>
    <li>不等式：乘或除負數要改向。涉及絕對值或分式，先找臨界點，再用數線分區間測試。</li>
    <li>數列：等差靠公差，等比靠公比。求和前先確認係邊一種，以及第一項同項數有冇取錯。應用題要把「第 n 項」同「前 n 項和」分清楚。</li>
    <li>變分：正變、反變、聯變先寫比例式，再代入一組已知值求常數，最後先用常數去預測。唔好未求常數就代入第二組數。</li>
  </ul>
</section>
<section class="res-sec">
  <h2>度量、圖形與空間</h2>
  <ul>
    <li>三角比：在直角三角形先標示對邊鄰邊斜邊。擴展到一般三角形時，用正弦或餘弦關係，並檢查鈍角會唔會令餘弦為負。</li>
    <li>解三角形：已知兩邊一夾角，通常較穩陣用餘弦求第三邊；已知兩邊同其中一邊嘅對角，要警惕可能有兩解。</li>
    <li>直線：斜率、兩點式、點斜式同一般式要能互換。平行斜率相同，垂直斜率乘積為 −1（直立或水平線另外處理）。</li>
    <li>圓：圓心半徑式同一般式互換時，小心配方。直線同圓相交，把直線代入圓方程，用判别式判斷交點數。</li>
    <li>求積：先認立體（柱、錐、球、棱柱等），再寫對應體積或表面積關係。組合體要寫「加邊啲、減邊啲」，單位同圓周率取位跟題目。</li>
  </ul>
</section>
<section class="res-sec">
  <h2>數據處理</h2>
  <ul>
    <li>集中趨勢：平均數受極端值影響較大，中位數較穩。分組數據要用組中點估算，並註明係估算。</li>
    <li>離差：範圍只看兩端；四分位距看中間一半；標準差先睇「同平均數嘅距離」。比較兩組數據時，同時講水平同散佈。</li>
    <li>概率：先判斷係唔係等可能。互斥事件加法，獨立事件乘法。條件概率要寫清楚「在已知發生之後，樣本空間點樣收窄」。</li>
    <li>排列組合：先問有冇次序、可唔可以重複、有冇限制條件。限制條件多時，用互補（全部減去不合條件）往往更乾淨。</li>
  </ul>
</section>
<section class="res-sec">
  <h2>卷一同卷二應試習慣</h2>
  <ul>
    <li>卷一傳統題：抄題中關鍵條件、寫公式、代入、單位同所求，一步都唔好跳。答案要合理精確度。</li>
    <li>甲部(1)爭取全對；甲部(2)同乙部先計畫時間，遇到卡關題先寫已確定部分。</li>
    <li>卷二選擇題：先自己算出或縮小範圍，再對選項。圖像題先睇截距、斜率、頂點同定義域。</li>
    <li>程式只供核對：見<a href="/math/calculator/">Casio 程式庫</a>。考試仍然要展示步驟。</li>
  </ul>
</section>
{official_links_html("math")}
"""
    return "/math/formulas/", render_page(
        path="/math/formulas/",
        title="DSE 數學必修公式同應試技巧｜DSE Hub",
        description="原創整理數學必修常見關係同卷一、卷二應試習慣，並連去現有課題筆記同 Casio 程式庫。請同時核對官方公式表。",
        crumbs=C(("/math/", "數學"), ("/math/formulas/", None)),
        h1="數學必修：公式同應試技巧",
        tagline="用自己嘅措辭整理常考關係。正式考試請同時核對官方公式表，並寫出步驟。",
        body=body,
        schema_type="Article",
        nav_html=nav([("/math/", "數學科目頁"), ("/math/formulas/", "公式同應試"), ("/math/calculator/", "計算機程式"), ("/m1/", "M1"), ("/m2/", "M2")]),
        footer_back=("/math/", "返回數學科目頁"),
        keywords="DSE 數學公式, 應試技巧, 必修部分, 免費",
    )


def _ext_landing(slug, name, formal, intro, papers, links, af_key):
    cards = "\n".join(card_link(*c) for c in links)
    body = f"""
{COPYRIGHT_NOTE}
<section class="res-sec">
  <h2>科目簡介</h2>
  <p>{intro}</p>
</section>
<section class="res-sec">
  <h2>公開評核（以 2027 年大綱為例）</h2>
  <p>{papers}</p>
</section>
<section class="res-sec">
  <h2>本站資源</h2>
  <div class="res-grid">{cards}</div>
</section>
{official_links_html(af_key)}
"""
    return f"/{slug}/", render_page(
        path=f"/{slug}/",
        title=f"免費 DSE 數學{name}溫習資源｜DSE Hub",
        description=f"為數學延伸部分{formal}提供原創公式溫習表同課題筆記。請同時核對官方公式表。",
        crumbs=C((f"/{slug}/", None)),
        h1=f"DSE 數學{name}溫習資源",
        tagline=f"{formal}。呢度提供原創溫習清單同課題重點，並唔取代官方評核大綱或公式表。",
        body=body,
        schema_type="CollectionPage",
        nav_html=nav([("/resources/", "全科資源"), ("/math/", "數學必修"), (f"/{slug}/", name), (f"/{slug}/formulas/", "公式表"), (f"/{slug}/notes/", "課題筆記")]),
        cta_html=f'<p class="page-cta"><a href="/{slug}/formulas/">公式表</a> · <a href="/{slug}/notes/">課題筆記</a> · <a href="/math/formulas/">必修公式</a></p>',
    )


def page_m1_landing():
    return _ext_landing(
        "m1", "延伸單元一", "單元一（微積分與統計）",
        "數學延伸部分單元一集中微積分同統計。考生必須同時報考必修部分，並且只可以選一個延伸單元。單元一適合想用微積分處理變化，並且較多接觸概率分布同推斷統計嘅同學。本站筆記由基本概念從頭整理，唔會抄錄任何官方課程文件或收費筆記。",
        "單元一公開考試只設一卷，全屬傳統題，時間約兩小時三十分鐘，全部題目通常都要作答，並分為較淺同較深兩部分。準確結構以當年評核大綱為準。電子計算機可用，但推導同符號陳述仍然要寫清楚。",
        [("/m1/formulas/", "公式", "單元一公式溫習表", "導數、積分、概率分布同推斷統計嘅常用關係。"),
         ("/m1/notes/", "筆記", "微積分與統計課題筆記", "極限直覺、微分應用、積分、二項及常態分布、置信區間等。")],
        "m1",
    )


def page_m2_landing():
    return _ext_landing(
        "m2", "延伸單元二", "單元二（代數與微積分）",
        "數學延伸部分單元二集中代數同微積分，包括矩陣、向量、數學歸納法，以及較完整嘅微積分技巧。同樣必須同時報考必修部分，並且只可選一個延伸單元。呢頁面向想加強嚴謹推導同空間代數嘅同學。",
        "單元二公開考試只設一卷，全屬傳統題，時間約兩小時三十分鐘，全部題目通常都要作答，並分為較淺同較深兩部分。準確結構以當年評核大綱為準。答案要有推理過程，而唔係只交數值。",
        [("/m2/formulas/", "公式", "單元二公式溫習表", "矩陣、向量、導數、積分同常用三角微積分關係。"),
         ("/m2/notes/", "筆記", "代數與微積分課題筆記", "歸納法、矩陣運算、向量幾何、微分同積分技巧。")],
        "m2",
    )


def page_m1_formulas():
    body = f"""
{COPYRIGHT_NOTE}
{FORMULA_DISCLAIMER}
<section class="res-sec">
  <h2>微積分</h2>
  <ul>
    <li>導數量度瞬間變化率。多項式逐項微分；乘積、商同複合函數要分清用邊一條法則，寫出中間步驟。</li>
    <li>切線斜率就係該點導數。有關極大極小，先求駐點，再用二階導數或符號變化判斷，並檢查端點（如果定義域封閉）。</li>
    <li>不定積分係微分嘅逆運算，唔好漏積分常數。定積分先求原函數再代入上下限，並注意下限大於上限時嘅變號，以及對稱性可唔可以減省運算。</li>
    <li>面積同變化量問題：先畫草圖，決定邊條曲線在上，以及交點。旋轉體或變化率應用要先寫關係，再先微分或積分。</li>
  </ul>
</section>
<section class="res-sec">
  <h2>統計同概率</h2>
  <ul>
    <li>先分清離散同連續。二項分布要確認次數固定、每次只有兩結果、獨立、成功概率不變。</li>
    <li>期望同方差：線性變換時，期望跟常數加減乘，方差只受倍數影響，加減常數唔改方差。</li>
    <li>常態分布：標準化成 z 之後先查表或用計數機。講「大約」時仍要寫出標準化步驟。</li>
    <li>抽樣同置信區間：分清總體參數同樣本統計量。區間寫成估計值加減誤差幅度，並說明置信水平意味住「同樣方法重複時」嘅覆蓋率，而唔係「呢個區間有某概率包住未知參數」嘅隨便講法。</li>
  </ul>
</section>
<section class="res-sec">
  <h2>應試提醒</h2>
  <p>長題先用文字講你要做咩，再寫符號。概率題寫樣本空間或分布名稱。數值要合理小數位。更完整嘅課題說明見<a href="/m1/notes/">單元一筆記</a>。</p>
</section>
{official_links_html("m1")}
"""
    return "/m1/formulas/", render_page(
        path="/m1/formulas/",
        title="DSE 數學 M1 公式溫習表（微積分與統計）｜DSE Hub",
        description="原創整理數學延伸單元一常見微積分同統計關係，並提示應試時要寫嘅步驟。請同時核對官方公式表。",
        crumbs=C(("/m1/", "單元一"), ("/m1/formulas/", None)),
        h1="單元一公式溫習表",
        tagline="用自己嘅措辭整理導數、積分、分布同推斷統計。考試請同時核對官方公式表。",
        body=body, schema_type="Article",
        nav_html=nav([("/m1/", "單元一"), ("/m1/formulas/", "公式表"), ("/m1/notes/", "課題筆記")]),
        footer_back=("/m1/", "返回單元一"),
    )


def page_m1_notes():
    body = f"""
{COPYRIGHT_NOTE}
<section class="res-sec">
  <h2>微積分思路</h2>
  <p>先建立「平均變化率可以縮到瞬間變化率」嘅直覺，再用法則去算。遇到文字題，先指定變量同單位，寫出 s(t)、A(x) 呢類函數，先再微分。增減、凹性同最值要分清楚：導數為零只係候選，唔等於一定係所需答案。</p>
  <p>積分方面，先問自己「呢條函數嘅原函數係咩」，再用代入法處理複合函數。面積題一定要畫圖，交點要解方程，而唔好目測。如果區間內函數係負，面積要用絕對值或分拆區間。</p>
</section>
<section class="res-sec">
  <h2>統計思路</h2>
  <p>每次先命名試驗同隨機變量。二項同幾何等離散模型，要把「成功」定義寫出來。連續模型則注意概率對應面積，單點概率為零。標準化時，方向（大於／小於／之間）會決定你點樣用表。</p>
  <p>推斷統計最易混淆嘅係用語：點估計係一個值，區間估計係一個範圍。解釋置信水平時，重點放喺方法嘅長期表現。假設檢驗如果出現喺課程範圍內，要寫零假設、對立假設、檢定統計量同結論語氣（拒絕或不拒絕，而唔好聲稱證明）。</p>
</section>
<section class="res-sec">
  <h2>常見陷阱</h2>
  <ul>
    <li>微分之後忘記單位，或者把變化率當成總量。</li>
    <li>積分漏咗常數，或者定積分上下限代入次序顛倒。</li>
    <li>把獨立當成互斥，或把樣本標準差同總體參數混為一談。</li>
    <li>常態近似未檢查條件，就直接套用。</li>
  </ul>
  <p>公式速查見<a href="/m1/formulas/">公式溫習表</a>。必修根基（函數、指數、概率）可回到<a href="/math/formulas/">必修公式頁</a>。</p>
</section>
{official_links_html("m1")}
"""
    return "/m1/notes/", render_page(
        path="/m1/notes/",
        title="DSE 數學 M1 課題筆記（微積分與統計）｜DSE Hub",
        description="原創整理單元一微積分應用同統計推斷嘅學習思路、常見陷阱同答題習慣。",
        crumbs=C(("/m1/", "單元一"), ("/m1/notes/", None)),
        h1="單元一課題筆記",
        tagline="由變化率、積分、概率分布到區間估計，用自己嘅話整理學習路線。",
        body=body, schema_type="Article",
        nav_html=nav([("/m1/", "單元一"), ("/m1/formulas/", "公式表"), ("/m1/notes/", "課題筆記")]),
        footer_back=("/m1/", "返回單元一"),
    )


def page_m2_formulas():
    body = f"""
{COPYRIGHT_NOTE}
{FORMULA_DISCLAIMER}
<section class="res-sec">
  <h2>代數</h2>
  <ul>
    <li>數學歸納法：先寫要證命題 P(n) 同起始值；再假設 P(k)，推出 P(k+1)；最後用一句話收束「由起始值同歸納步驟，對所有指定正整數成立」。假設要用得明顯，唔好跳步。</li>
    <li>矩陣：加法同標量乘法按元素進行；乘法要檢查前一個嘅列數等如後一個嘅行數。乘法無交換律，唔好隨便調位。單位矩陣扮演 1 嘅角色；逆矩陣存在先可以解某類方程組。</li>
    <li>行列式（二階或課程範圍內嘅階數）：可用嚟判斷可逆同計算面積或體積相關量，但要跟課程允許嘅方法。</li>
    <li>向量：用分量加減、標量乘法同位置向量去描述點同線。點積可以判斷垂直同求夾角；要分清向量平行同垂直嘅條件。三維範圍以大綱為準。</li>
  </ul>
</section>
<section class="res-sec">
  <h2>微積分</h2>
  <ul>
    <li>標準導數：多項式、指數、對數、三角同反三角（若在範圍內）要熟，並且會用鏈法則。</li>
    <li>積分：除基本形式外，常見技巧包括代換、分部積分同三角恆等變形。定積分仍然要寫上下限轉換。</li>
    <li>應用：切線法線、率變、最值、面積、弧長或體積等，以課程列明者為準。先寫關係式，再先運算。</li>
  </ul>
</section>
<section class="res-sec">
  <h2>應試提醒</h2>
  <p>代數題要有推論句；微積分題要有函數同定義域意識。更完整說明見<a href="/m2/notes/">單元二筆記</a>。</p>
</section>
{official_links_html("m2")}
"""
    return "/m2/formulas/", render_page(
        path="/m2/formulas/",
        title="DSE 數學 M2 公式溫習表（代數與微積分）｜DSE Hub",
        description="原創整理數學延伸單元二矩陣、向量、歸納法同微積分常用關係。請同時核對官方公式表。",
        crumbs=C(("/m2/", "單元二"), ("/m2/formulas/", None)),
        h1="單元二公式溫習表",
        tagline="用自己嘅措辭整理代數同微積分關係。考試請同時核對官方公式表。",
        body=body, schema_type="Article",
        nav_html=nav([("/m2/", "單元二"), ("/m2/formulas/", "公式表"), ("/m2/notes/", "課題筆記")]),
        footer_back=("/m2/", "返回單元二"),
    )


def page_m2_notes():
    body = f"""
{COPYRIGHT_NOTE}
<section class="res-sec">
  <h2>代數學習路線</h2>
  <p>數學歸納法考嘅係結構完整，而唔係文筆。建議每次用同一骨架，但命題內容要抄準，尤其不等式同整除題，歸納步驟裡嘅「多出來嗰截」要處理得乾淨。</p>
  <p>矩陣題先檢查維度。解聯立方程時，寫出矩陣方程，再決定用逆矩陣、列運算定其他允許方法。解釋幾何意義前，先確保運算合法。</p>
  <p>向量題畫一張簡單圖：原點、點嘅位置向量、線嘅方向向量。求夾角先考慮點積；求垂直就驗證點積是否為零；求平行就檢查是否有標量倍數關係。</p>
</section>
<section class="res-sec">
  <h2>微積分學習路線</h2>
  <p>單元二通常要求更熟練嘅技巧。遇到複雜函數，先想「係乘積、商，定係複合」。積分先分類：睇到複合函數嘅內層導數，優先想代換；睇到乘積，先先考慮分部積分。</p>
  <p>證明題同計算題都要有推理鏈。若題目要求「證明某不等式」或「證明某恆等」，每一步都要由已知或已證結果出發，唔好由要證嘅結論倒推當已證。</p>
</section>
<section class="res-sec">
  <h2>常見陷阱</h2>
  <ul>
    <li>歸納法只驗證起始值，中間步驟用了要證結論。</li>
    <li>矩陣乘法維度不合仍然硬乘，或以為 AB = BA。</li>
    <li>向量夾角用錯點積公式，或把方向向量當成位置向量。</li>
    <li>微積分代換之後忘記改上下限，或漏絕對值、定義域。</li>
  </ul>
</section>
{official_links_html("m2")}
"""
    return "/m2/notes/", render_page(
        path="/m2/notes/",
        title="DSE 數學 M2 課題筆記（代數與微積分）｜DSE Hub",
        description="原創整理單元二歸納法、矩陣、向量同微積分技巧嘅學習路線同常見陷阱。",
        crumbs=C(("/m2/", "單元二"), ("/m2/notes/", None)),
        h1="單元二課題筆記",
        tagline="把嚴謹推導同計算技巧分開練習，再合成完整長題答案。",
        body=body, schema_type="Article",
        nav_html=nav([("/m2/", "單元二"), ("/m2/formulas/", "公式表"), ("/m2/notes/", "課題筆記")]),
        footer_back=("/m2/", "返回單元二"),
    )


def page_chem_formulas():
    topics = _topic_links(CHEM_TOPICS)
    body = f"""
{COPYRIGHT_NOTE}
{FORMULA_DISCLAIMER}
<section class="res-sec">
  <h2>同現有化學課題頁一齊用</h2>
  <p>化學科已有多年份試卷同課題頁。呢頁補充原創嘅計算框架、常見離子記憶方法同文字題答法，方便你由概念行返去題目。</p>
  <nav class="res-toc" aria-label="化學課題">{topics}</nav>
</section>
<section class="res-sec">
  <h2>計量同計算框架</h2>
  <ol>
    <li>先寫平衡化學方程式，狀態同系數唔好估完就算。</li>
    <li>把已知量全部轉成摩爾。溶液用濃度乘體積（體積要統一單位）；氣體用題目指定嘅摩爾體積或理想氣體關係，唔好混用未聲明嘅條件。</li>
    <li>用系數比找限制反應物，先再算目標物質。過量物質要交代剩餘。</li>
    <li>產率、濃度或氣體體積喺最後先還原，並檢查有效數字同單位。</li>
  </ol>
</section>
<section class="res-sec">
  <h2>常見離子同物質分類（溫習用）</h2>
  <p>下面係學習上常用嘅離子同類別，方便寫方程式同觀察記錄。正式名單同顏色變化，請以課堂實驗同官方教材為準，唔好把呢頁當成完整點名表。</p>
  <ul>
    <li>常見陽離子：鈉、鉀、鈣、鎂、鋁、鋅、鐵(II)、鐵(III)、銅(II)、鉛(II)、銀、銨。記嘅時候連測試方法一齊記，例如焰色、沉澱或氣體。</li>
    <li>常見陰離子：氯、溴、碘、氫氧、硝酸、硫酸、碳酸、亞硫酸。很多要靠酸化之後放出嘅氣體，或與硝酸銀、氯化鋇等試劑嘅反應去分辨。</li>
    <li>寫離子方程式時，只保留真正參與嘅離子，並檢查電荷同原子數平衡。</li>
  </ul>
</section>
<section class="res-sec">
  <h2>解釋題點寫</h2>
  <ul>
    <li>酸鹼：講清楚質子轉移、強弱酸定義，以及稀釋或中和對 pH 同導電性嘅影響，避免只寫「酸性變弱」。</li>
    <li>氧化還原：指出邊種物種失電子、邊種得電子，氧化數變化要寫出來。</li>
    <li>平衡：用可逆反應同勒沙特列原理時，必須講「已建立平衡之後，改變邊個條件、系統點樣減緩呢個改變」。唔好把速率同平衡位置混為一談。</li>
    <li>結構同鍵合：由電子排列講到鍵型，再講到熔點、導電、硬度等可觀察性質。</li>
  </ul>
</section>
{official_links_html("chem")}
"""
    return "/chem/formulas/", render_page(
        path="/chem/formulas/",
        title="DSE 化學公式、離子同答題框架｜DSE Hub",
        description="原創整理化學計量步驟、常見離子溫習法，以及酸鹼、氧化還原同平衡等解釋題框架，並連去現有課題頁。",
        crumbs=C(("/chem/", "化學"), ("/chem/formulas/", None)),
        h1="化學：公式、離子同答題框架",
        tagline="計算先轉摩爾，解釋先寫原理。請同時核對課堂教材同官方評核大綱。",
        body=body, schema_type="Article",
        nav_html=nav([("/chem/", "化學科目頁"), ("/chem/formulas/", "公式同框架"), ("/resources/", "全科資源")]),
        footer_back=("/chem/", "返回化學科目頁"),
    )


def page_econ_skills():
    topics = _topic_links(ECON_TOPICS)
    body = f"""
{COPYRIGHT_NOTE}
<section class="res-sec">
  <h2>同現有經濟課題頁一齊用</h2>
  <p>經濟科已有課題頁同部分歷屆試卷。呢頁集中講資料回應、短題同較長題嘅作答框架。2028 年起評核框架將有更新，溫習時請核對你應考年份嘅大綱，而唔好假設所有舊卷結構永遠不變。</p>
  <nav class="res-toc" aria-label="經濟課題">{topics}</nav>
</section>
<section class="res-sec">
  <h2>以 2027 年大綱為例嘅卷面</h2>
  <p>卷一通常係必修範圍嘅多項選擇。卷二大致包括必修短題、必修結構或資料回應，以及選修單元題（選答其中一個單元）。時間同確切比重以官方文件為準。</p>
</section>
<section class="res-sec">
  <h2>短題同定義題</h2>
  <ul>
    <li>定義要完整：例如機會成本要包含「被放棄嘅最高價值用途」，而唔係只寫「放棄咗嘅東西」。</li>
    <li>辨識題用課程術語命名現象（短缺、剩餘、公共物品、外部性、名義同實質），再補一個題目情境中嘅證據。</li>
    <li>計算題寫公式、代入、單位，例如指數、乘數或彈性，並說明數值含義。</li>
  </ul>
</section>
<section class="res-sec">
  <h2>資料回應同長題</h2>
  <ol>
    <li>先讀資料標題、單位、年期。圖表講趨勢，文字資料分清事實同意見。</li>
    <li>用經濟學工具分析：供求移動要講邊邊移動、係需求定供給、點解，以及均衡價格與量嘅方向。</li>
    <li>政策題用準則，例如效率、公平、誘因、財政負擔、時間滯後，先再下判斷。兩邊都要寫，結論先有力。</li>
    <li>宏觀題分清名義／實質、短期／長期、開放經濟下嘅泄漏。唔好把所有下跌都叫衰退，而不看定義。</li>
  </ol>
</section>
<section class="res-sec">
  <h2>常見失分</h2>
  <ul>
    <li>把存量同流量、平均同邊際、移動曲線同沿曲線移動搞亂。</li>
    <li>只描述資料（「圖顯示上升」）而沒有經濟學解釋。</li>
    <li>長題沒有段落功能，或者例子同原理互不相干。</li>
  </ul>
</section>
{official_links_html("econ")}
"""
    return "/econ/exam-skills/", render_page(
        path="/econ/exam-skills/",
        title="DSE 經濟資料回應同長題答題框架｜DSE Hub",
        description="原創整理經濟科短題、資料回應同政策長題嘅作答步驟，並連去現有課題頁。請核對應考年份評核大綱。",
        crumbs=C(("/econ/", "經濟"), ("/econ/exam-skills/", None)),
        h1="經濟科應試框架",
        tagline="用經濟學術語同準則去解釋資料，而唔係只複述圖表。",
        body=body, schema_type="Article",
        nav_html=nav([("/econ/", "經濟科目頁"), ("/econ/exam-skills/", "應試框架"), ("/resources/", "全科資源")]),
        footer_back=("/econ/", "返回經濟科目頁"),
    )


# Physics and biology topic pages continue below.
PHYS_NAV = nav([
    ("/phys/", "物理科目頁"),
    ("/phys/formulas/", "公式表"),
    ("/phys/mechanics/", "力學"),
    ("/phys/heat/", "熱與氣體"),
    ("/phys/waves/", "波動"),
    ("/phys/electricity-magnetism/", "電磁"),
    ("/phys/radioactivity/", "放射"),
    ("/phys/energy/", "能量"),
])

BIO_NAV = nav([
    ("/bio/", "生物科目頁"),
    ("/bio/exam-skills/", "應試技巧"),
    ("/bio/cells/", "細胞"),
    ("/bio/genetics/", "遺傳"),
    ("/bio/human-physiology/", "人體生理"),
    ("/bio/ecology/", "生態"),
    ("/bio/evolution/", "演化"),
    ("/bio/biotechnology/", "生物科技"),
])


def page_phys_formulas():
    body = f"""
{COPYRIGHT_NOTE}
{FORMULA_DISCLAIMER}
<section class="res-sec">
  <h2>公開評核同課題範圍</h2>
  <p>以 2027 年大綱為例，物理公開考試包括涵蓋必修部分嘅卷一（選擇同傳統題）同涵蓋選修部分嘅卷二（由若干選修課題中選答指定數目），學校考生另有實驗為本嘅校本評核。必修溫習通常環繞熱同氣體、力和運動、波動、電磁，以及放射同核能等主題；選修可包括原子世界、能量使用、醫學物理或天文學等，以當年大綱為準。</p>
  <p>下面係原創溫習清單，符號以常見課堂寫法表示。考試時要以卷面公式表同題目定義為準。</p>
</section>
<section class="res-sec">
  <h2>力學</h2>
  <ul>
    <li>勻加速直線：位移、初速、末速、加速度、時間五個量，揀一條只用已知量嘅關係，避免循環代入。</li>
    <li>力同運動：合力等於質量乘加速度，對象要畫自由體圖，分清重量同質量、張力、摩擦力方向。</li>
    <li>動量：碰撞前後總動量在無外力（或外力可忽略）時守恆。彈性同非彈性要另外檢查動能係唔係守恆。</li>
    <li>功同能：功係力同位移在力方向上嘅貢獻。機械能守恆只在沒有非守恆力做功（或已計算其功）時使用。</li>
    <li>圓周或萬有引力相關題：先寫向心力來源，再先套關係。唔好把任何彎曲路徑都當成勻速圓周。</li>
  </ul>
  <p>詳見<a href="/phys/mechanics/">力學筆記</a>。</p>
</section>
<section class="res-sec">
  <h2>熱、波、電磁、放射</h2>
  <ul>
    <li>熱：溫升用熱容量或比熱容關係；物態變化用潛熱，過程中溫度可以保持不變。氣體題要分清等壓、等體、等溫，同埋溫度必須用熱力學溫標去入某些關係。</li>
    <li>波：波速等於頻率乘波長。反射、折射、衍射同干涉要先判斷波現象，先再寫條件（例如光程差）。</li>
    <li>電：電流、電位差、電阻之間嘅關係，串聯分壓、並聯分流。電功率要分清用邊組已知量。磁場對電流或運動電荷嘅力，要同時講大小同方向法則。</li>
    <li>放射：半衰期描述尚未衰變核嘅統計行為。活度、衰變常數同核反應質量能關係，要按題目給出嘅量去用，並注意安全同屏蔽係概念題常客。</li>
  </ul>
</section>
<section class="res-sec">
  <h2>答題格式</h2>
  <p>列出已知、所用關係、代入、單位同方向。圖像題先讀斜率同面積代表咩。估算題要寫合理假設。選修題見各選修課堂筆記，本站必修課題頁由力學去到能量。</p>
</section>
{official_links_html("phys")}
"""
    return "/phys/formulas/", render_page(
        path="/phys/formulas/",
        title="DSE 物理公式溫習表｜DSE Hub",
        description="原創整理物理必修常見關係：力學、熱與氣體、波動、電磁同放射，並提示答題格式。請同時核對官方公式表。",
        crumbs=C(("/phys/", "物理"), ("/phys/formulas/", None)),
        h1="物理公式溫習表",
        tagline="用自己嘅措辭整理常考關係。正式考試請同時核對卷面公式表。",
        body=body, schema_type="Article", nav_html=PHYS_NAV, footer_back=("/phys/", "返回物理科目頁"),
    )


PHYS_TOPICS = [
    ("mechanics", "力學（力和運動）", "勻加速、牛頓定律、動量、功與能同圓周運動嘅溫習重點。", [
        ("先畫圖再寫方程", "每題指定研究對象，畫受力或運動草圖，標方向同正方向。先寫原理，再代入數字。"),
        ("運動學", "勻加速先確認加速度真係恆定。自由落體係勻加速嘅特例。圖像中，位移—時間圖斜率係速度，速度—時間圖斜率係加速度，下面面積係位移。"),
        ("動力學", "合力先先分解。摩擦力是唔係已達最大值，決定物體起步定只係有運動趨勢。連接體用同一加速度大小，但張力要分開對象寫。"),
        ("動量同能量", "撞擊、爆炸同反衝優先想動量。能量則用來處理高度、彈簧或速率。兩者可以同時用，但守恆條件要分別檢查。"),
        ("常見失分", "把質量當重量、漏咗一個力、單位用厘米卻當米，或者向量只加大小唔計方向。"),
    ]),
    ("heat", "熱與氣體", "內能、熱容量、潛熱同理想氣體關係嘅學習重點。", [
        ("溫度同內能", "溫度反映粒子平均動能嘅尺度；內能仲包括相互作用相關能量。接觸傳熱、做功都可以改內能。"),
        ("量熱", "熱量傳遞題先寫「邊邊失去、邊邊得到」，再決定用溫升關係定潛熱。有物態變化就唔好全部當成只係溫升。"),
        ("氣體", "把壓強理解成粒子撞擊器壁嘅宏觀效果。使用 pV = nRT 或課程中等價關係時，溫度要用熱力學溫標。過程要分清邊個量被保持不變。"),
        ("常見失分", "攝氏同開爾文混用、忽略散失到周圍嘅熱、或把沸騰當成溫度一定上升。"),
    ]),
    ("waves", "波動", "波的描述、聲與光現象同干涉條件嘅溫習重點。", [
        ("描述波", "先分橫波縱波、機械波電磁波。波長、頻率、振幅、速率要對應到圖中正確位置。"),
        ("波動現象", "反射保留某些性質但可改方向；折射涉及波速變化；衍射在障礙或縫同波長可比時更明顯；干涉要相干源同程差條件。"),
        ("聲音同光", "聲音需要介質；電磁波不必。討論音調、響度或音色時，分別對應頻率、振幅同波形。光嘅顏色同分光，要同頻率或波長一起講。"),
        ("常見失分", "把波速當成永遠不變，或未檢查干涉係相長定相消就套公式。"),
    ]),
    ("electricity-magnetism", "電與磁", "電路、電功率、磁場同電磁感應嘅溫習重點。", [
        ("電路基礎", "先畫等效電路。串聯電流相同、電壓相加；並聯電壓相同、電流相加。內阻題要把電源同外電路分開寫。"),
        ("電能同功率", "功率可用電位差同電流，或其他等價組合。發熱同電能傳輸要講清楚時間。"),
        ("磁場", "先判斷場嘅來源（永久磁、電流）。力嘅方向用課程教導嘅法則，並註明對正電荷或電流嘅約定。"),
        ("電磁感應", "磁通量變化先產生感應電動勢。要講是邊個量在變：面積、場強定方向。楞次定律用來定方向，抵消「引起它嘅改變」。"),
        ("常見失分", "把電壓電流當成永遠成正比而忽略非歐姆元件，或者感應題不講通量變化。"),
    ]),
    ("radioactivity", "放射與核能", "衰變、半衰期、探測同質量能關係嘅溫習重點。", [
        ("三種常見放射", "比較穿透力、電離本領同在電場磁場中嘅行為時，用對照表記憶，但解釋要講粒子或輻射本身性質。"),
        ("半衰期", "半衰期係大量原子核層面嘅統計規律。剩餘數量、活度隨時間下降，可用倍減或課程允許嘅指數關係。單個核唔可以準確預言幾時衰變。"),
        ("核反應", "質量虧損同能量釋放要分清「失去可量度質量、對應釋放能量」。方程要平衡核子數同電荷數。"),
        ("安全", "時間、距離、屏蔽係概念題常用三重點。判斷題要針對輻射類型選材料，而唔好空講「小心啲」。"),
    ]),
    ("energy", "能量同其使用", "能量形式、守恆、發電同效益嘅溫習重點。", [
        ("守恆同轉移", "能量唔會消失，但可以變得唔再容易做有用功。答題時畫能量流：輸入、有用輸出、損耗。"),
        ("發電", "先講能量源點樣轉成機械能再轉成電能，或光伏等其他路徑。比較發電方式要用準則：可靠性、環境影響、啟動時間、能量密度，而唔好只給偏好。"),
        ("效率", "效率係有用輸出對總輸入嘅比，永遠要講清楚邊個輸出先算有用。單位要一致。"),
        ("同選修嘅關係", "若你選修能量課題，課堂會有更專題嘅內容。呢頁只整理必修裡已經需要嘅能量思路，方便卷一作答。"),
    ]),
]


def _topic_page(prefix, nav_html, parent_name, parent_path, slug, title, desc, sections, af, extra_head=""):
    parts = [COPYRIGHT_NOTE, extra_head]
    for i, (h, p) in enumerate(sections, 1):
        parts.append(f'<section class="res-sec" id="s{i}"><h2>{h}</h2><p>{p}</p></section>')
    body = "\n".join(parts) + official_links_html(af)
    path = f"{parent_path}{slug}/"
    return path, render_page(
        path=path,
        title=f"DSE {parent_name}課題筆記：{title}｜DSE Hub",
        description=f"原創整理 DSE {parent_name}「{title}」溫習重點、常見陷阱同答題習慣。不含官方試題原文。",
        crumbs=C((parent_path, parent_name), (path, None)),
        h1=title,
        tagline=desc,
        body=body,
        schema_type="Article",
        nav_html=nav_html,
        footer_back=(parent_path, f"返回{parent_name}科目頁"),
    )


def phys_topic_pages():
    pages = []
    for slug, title, desc, sections in PHYS_TOPICS:
        pages.append(_topic_page("phys", PHYS_NAV, "物理", "/phys/", slug, title, desc, sections, "phys"))
    return pages


BIO_TOPICS = [
    ("cells", "細胞同生命分子", "細胞結構、膜運輸同基本生化過程嘅溫習重點。", [
        ("由分子到細胞", "先把握水、糖、脂質、蛋白質同核酸喺結構同功能上嘅分工，再連到細胞器。答題時「結構如何服務功能」係主軸。"),
        ("膜同運輸", "磷脂雙層同蛋白質令膜有選擇通透性。擴散、滲透、協助擴散同主動運輸，要比較是否需要能量同載體。畫箭嘴前先判斷濃度梯度。"),
        ("酶同代謝", "酶係生物催化劑，活性受溫度、pH 同抑制劑影響。解釋時用形狀互補同變性，而唔好只寫「酶死咗」。"),
        ("光合同呼吸嘅位置", "能指出主要場所同「儲存／釋放可利用能量」已經可以應付好多綜合題；細節深度跟課程要求，唔好背無上下文嘅長流程。"),
    ]),
    ("genetics", "遺傳", "染色體、孟德爾遺傳、變異同基因表達嘅溫習重點。", [
        ("分裂", "有絲分裂保存遺傳組成，減數分裂產生遺傳上多樣嘅配子。講清染色體數目變化，畫圖要標明同源染色體。"),
        ("遺傳圖同概率", "先寫清楚顯性隱性、基因型表現型。兩對性狀要確認是否獨立分配。性連鎖要畫出性染色體。"),
        ("DNA 同蛋白質", "遺傳訊息如何經轉錄翻譯走向性狀，係解釋題常用橋樑。突變可以改氨基酸序列，但唔係每次都改表現型。"),
        ("常見失分", "把配子當成二倍體、把比例當成一定出現嘅人數，或無視性別同世代。"),
    ]),
    ("human-physiology", "人體生理", "循環、氣體交換、神經、激素同恆常性嘅溫習重點。", [
        ("系統觀", "先問「邊個系統負責運輸、交換、協調或排泄」，再進入器官水平。綜合題經常跨系統，例如運動時循環同呼吸同時改變。"),
        ("恆常性", "負回饋係常見模式：偏差被偵測，效應器作出相反方向調整。寫例子時要包括感受器、控制中樞、效應器。"),
        ("協調", "神經快而針對；激素較慢而廣泛。兩者可以合作。畫反射弧時方向要正確。"),
        ("選修提示", "人體生理調節如果係你嘅選修，課堂會有更專題嘅機制。呢頁整理卷一已經常用嘅思路。"),
    ]),
    ("ecology", "生態同環境", "能量流、物質循環、種群同保育嘅溫習重點。", [
        ("能量流", "生產者固定能量，之後沿食物鏈遞減。金字塔要用題目給嘅量（數量、生物量或能量），唔好三種混用。"),
        ("循環同人為影響", "碳、氮或水循環題，先畫庫同流，再指出人類活動改咗邊一條流。"),
        ("種群同群落", "出生死亡遷移決定種群變化。種間關係要用證據，而唔好只貼標籤。"),
        ("保育", "建議要對應題目中嘅衝突（發展、生計、多樣性），提出可操作、可監測嘅做法。"),
    ]),
    ("evolution", "演化同多樣性", "自然選擇、適應同分類思路嘅溫習重點。", [
        ("自然選擇", "變異先存在，環境再選擇較能生存繁殖嘅性狀，種群基因頻率先先改變。唔好寫成個體為了生存而決定進化。"),
        ("證據", "化石、比較解剖、分子證據等，要說明「點樣支持共同由來或環境適應」。"),
        ("多樣性", "分類係幫助組織多樣性嘅工具。解釋學名或特徵表時，用可觀察性狀，避免循環定義。"),
        ("同遺傳嘅連結", "沒有可遺傳變異，選擇就難以累積。跨課題題要用呢條橋。"),
    ]),
    ("biotechnology", "生物科技同健康", "基礎技術原理、應用同風險討論嘅溫習重點。", [
        ("原理先於商品名", "解釋某技術時，先講用咗邊個生物過程或工具（例如切割、複製、分離），再講應用場景。"),
        ("健康同疾病", "免疫、疫苗、抗菌素要分清預防同治療，以及點解濫用會帶來抗藥性。"),
        ("倫理同風險", "討論題用準則：安全、知情、公平、環境影響。兩邊都寫，結論先穩。"),
        ("選修提示", "生物科技若係選修，會有更專門操作同例子。卷一亦可能用基礎概念設題，所以呢頁對所有考生都有用。"),
    ]),
]


def page_bio_skills():
    cards = "\n".join(
        card_link(f"/bio/{s}/", "課題", t, d) for s, t, d, _ in BIO_TOPICS
    )
    body = f"""
{COPYRIGHT_NOTE}
<section class="res-sec">
  <h2>卷面概況（以 2027 年大綱為例）</h2>
  <p>卷一涵蓋必修，通常包括選擇同傳統題，時間約兩小時三十分鐘；卷二涵蓋選修，考生由若干選修課題中選答指定數目。學校考生另有實驗技巧同探究報告嘅校本評核。自修生安排以官方說明為準。</p>
</section>
<section class="res-sec">
  <h2>傳統題點寫</h2>
  <ul>
    <li>定義用精確術語。比較題用表或對照句，每點都兩邊寫。</li>
    <li>實驗題寫清自變項、應變項、控制項、量度方法同重覆。解釋結果時連返原理，而唔好只重述表格數字。</li>
    <li>圖表題先讀軸同單位，描述趨勢再用生物學原因解釋。</li>
    <li>計算題（例如放大率、速率、能量傳遞）寫公式、代入、單位。</li>
  </ul>
</section>
<section class="res-sec">
  <h2>本站課題筆記</h2>
  <div class="res-grid">{cards}</div>
</section>
{official_links_html("bio")}
"""
    return "/bio/exam-skills/", render_page(
        path="/bio/exam-skills/",
        title="DSE 生物應試技巧同課題入口｜DSE Hub",
        description="原創整理生物科傳統題、實驗題同圖表題答法，並連去細胞、遺傳、生理、生態等課題筆記。",
        crumbs=C(("/bio/", "生物"), ("/bio/exam-skills/", None)),
        h1="生物應試技巧",
        tagline="用精確術語、實驗邏輯同圖表證據作答。課題細節見各篇筆記。",
        body=body, schema_type="Article", nav_html=BIO_NAV, footer_back=("/bio/", "返回生物科目頁"),
    )


def bio_topic_pages():
    pages = []
    for slug, title, desc, sections in BIO_TOPICS:
        pages.append(_topic_page("bio", BIO_NAV, "生物", "/bio/", slug, title, desc, sections, "bio"))
    return pages


def all_pages():
    pages = [
        page_math_formulas(),
        page_m1_landing(), page_m1_formulas(), page_m1_notes(),
        page_m2_landing(), page_m2_formulas(), page_m2_notes(),
        page_chem_formulas(),
        page_econ_skills(),
        page_phys_formulas(),
        page_bio_skills(),
    ]
    pages.extend(phys_topic_pages())
    pages.extend(bio_topic_pages())
    return pages
