# -*- coding: utf-8 -*-
"""English and Citizenship and Social Development pages."""
from .template import COPYRIGHT_NOTE, card_link, official_links_html, render_page

HUB = ("/hub/", "DSE Hub")


def C(*p):
    return [HUB, *p]


def nav(links):
    items = "\n".join(f'        <a href="{h}">{n}</a>' for h, n in links)
    return f'<nav class="strand-nav" aria-label="科目資源">\n{items}\n        </nav>'


def _eng_nav():
    return nav([
        ("/resources/", "全科資源"),
        ("/eng/", "英國語文"),
        ("/eng/writing/", "寫作框架"),
        ("/eng/speaking/", "說話技巧"),
    ])


def page_eng_landing():
    body = f"""
{COPYRIGHT_NOTE}
<section class="res-sec">
  <h2>科目簡介</h2>
  <p>英國語文係甲類核心科目，公開評核包括閱讀、寫作、聆聽及綜合能力、說話，學校考生另有校本評核。優化之後，寫作卷二乙部可選題目數量已減少，但任務寫作嘅核心不變：先認清讀者、目的同文體，再組織內容。</p>
  <p>本站唔會轉載閱讀卷篇章、聆聽錄音或任何歷屆試題。下面用自己嘅話概括 2027 年評核大綱常見結構，實際時間、比重同可選部分請核對該年官方文件。</p>
</section>
<section class="res-sec">
  <h2>公開評核（以 2027 年大綱為例）</h2>
  <div class="res-table-wrap"><table>
    <thead><tr><th>部分</th><th>內容</th><th>大致安排</th></tr></thead>
    <tbody>
      <tr><td>卷一</td><td>Reading</td><td>約 1.5 小時。甲部必答，乙部要喺較易同較難兩組之中選一組。選較易一組通常未能達到最高等級，細節以大綱為準。</td></tr>
      <tr><td>卷二</td><td>Writing</td><td>約 2 小時。甲部短篇引導寫作；乙部較長、較開放，由若干題選一題。</td></tr>
      <tr><td>卷三</td><td>Listening and Integrated Skills</td><td>約 2 小時。甲部必答，乙部同樣有較易／較難選擇，並要整合聽力同閱讀材料去完成任務。</td></tr>
      <tr><td>卷四</td><td>Speaking</td><td>約 20 分鐘，包括小組討論同個人回應。</td></tr>
      <tr><td>校本評核</td><td>School-based Assessment</td><td>學校考生須完成。自修生安排以官方說明為準。</td></tr>
    </tbody>
  </table></div>
</section>
<section class="res-sec">
  <h2>本站資源</h2>
  <div class="res-grid">
    {card_link("/eng/writing/","Writing","寫作框架","article、letter、proposal、speech、report 等任務寫作步驟。")}
    {card_link("/eng/speaking/","Speaking","說話同小組討論","如何展開討論、回應、不同意同收束，而唔係背稿。")}
  </div>
</section>
{official_links_html("eng")}
"""
    return "/eng/", render_page(
        path="/eng/",
        title="免費 DSE 英國語文溫習資源（寫作同說話框架）｜DSE Hub",
        description="為 DSE 英國語文提供公開評核概覽，以及寫作文體框架、說話同小組討論嘅原創應試技巧。",
        crumbs=C(("/eng/", None)),
        h1="DSE 英國語文溫習資源",
        tagline="由任務寫作同口語互動入手，幫你處理 Paper 2 同 Paper 4。真題同錄音請用官方刊物。",
        body=body,
        schema_type="CollectionPage",
        nav_html=_eng_nav(),
        cta_html='<p class="page-cta"><a href="/eng/writing/">寫作框架</a> · <a href="/eng/speaking/">說話技巧</a> · <a href="/resources/">全科資源</a></p>',
        keywords="DSE English, writing, speaking, group discussion, 免費",
    )


def page_eng_writing():
    body = f"""
{COPYRIGHT_NOTE}
<section class="res-sec">
  <h2>所有文體共通嘅五步</h2>
  <ol>
    <li>Audience and purpose：你為邊個寫、要對方做咩或信咩。</li>
    <li>Genre features：信要有稱謂同收束，建議書要有背景同可行建議，演講要有呼應聽眾嘅開場。</li>
    <li>Content plan：甲部跟提示逐點完成；乙部用 3 至 4 個主段，每段一個功能，避免重複同一例子。</li>
    <li>Tone and register：正式程度要穩。投訴可以堅定，但唔好無禮；演講可以生動，但唔好變成口號堆砌。</li>
    <li>Accuracy last, but not optional：留幾分鐘查主語動詞一致、冠詞、標點同段落。華麗詞彙用錯，分會低過清楚英語。</li>
  </ol>
  <p>2027 年大綱中，甲部係較短嘅引導寫作，乙部較長，由若干題選一。字數只係參考規模，完整完成任務同篇章組織更重要。以下框架用自己嘅話整理，並唔係官方評卷參考。</p>
</section>
<section class="res-sec">
  <h2>常見文體點起步</h2>
  <div class="res-card"><h3>Article / blog / magazine feature</h3>
  <p>開首用具體場面或問題吸引讀者，中段用小標題或清楚段落展開兩個至三個角度，結尾俾讀者一個可記住嘅判斷或行動。唔好寫成學校週記，亦唔好全程抽象講道理。</p></div>
  <div class="res-card"><h3>Letter or email</h3>
  <p>先分清正式／半正式。開頭表明身份同寫信原因，中段每段處理一個訴求或理據，結尾講清楚期望對方做嘅事同禮貌收束。投訴信要有事實、影響同合理要求；友情信都要有細節，唔好空喊情緒。</p></div>
  <div class="res-card"><h3>Proposal or report</h3>
  <p>用標題同小節：背景、現況問題、建議、預期好處、實行步驟或限制。建議要具體到「邊個、幾時、點做、點量度」，避免只寫 should improve communication。報告語氣比建議書更克制，結論要對應前文資料。</p></div>
  <div class="res-card"><h3>Speech or debate</h3>
  <p>開場稱呼聽眾並亮出立場，中段兩至三個論點，每點用一個具體例子。適當預想反對意見並簡短回應。結尾重申立場並俾聽眾一個清楚呼籲。書面講稿都要讀得出節奏，句子唔好過長。</p></div>
  <div class="res-card"><h3>Story</h3>
  <p>如果題目容許叙事，先定衝突同轉折，唔好流水帳由起床寫到訓覺。對話要短，細節要指向主題（例如壓力、誤會、責任）。結局可以開放，但讀者要感覺事件有改變。</p></div>
</section>
<section class="res-sec">
  <h2>乙部點揀題</h2>
  <ul>
    <li>揀你有具體例子可寫嘅題，而唔係看起來「高級」但內容空洞嘅題。</li>
    <li>睇清文體限制。題目叫 proposal，就唔好寫成隨筆。</li>
    <li>用一分鐘列三個主段；列唔出第三個有用角度，就換題。</li>
  </ul>
</section>
<section class="res-sec">
  <h2>語言質素</h2>
  <p>變化句式同準確連接詞，比堆砌生字重要。段落之間用功能句過渡，但唔好機械重複。完成後默讀一次，專抓漏字同唔自然嘅翻譯腔。</p>
</section>
{official_links_html("eng")}
"""
    return "/eng/writing/", render_page(
        path="/eng/writing/",
        title="DSE 英文寫作框架（Article、書信、建議書、演講）｜DSE Hub",
        description="原創整理 DSE English Paper 2 常見文體嘅任務步驟、語氣同揀題方法。不含歷屆試題。",
        crumbs=C(("/eng/", "英國語文"), ("/eng/writing/", None)),
        h1="英國語文寫作框架",
        tagline="先完成任務同讀者意識，再追求文采。適用於引導短篇同較長嘅開放寫作。",
        body=body,
        schema_type="Article",
        nav_html=_eng_nav(),
        footer_back=("/eng/", "返回英國語文"),
    )


def page_eng_speaking():
    body = f"""
{COPYRIGHT_NOTE}
<section class="res-sec">
  <h2>小組討論在考乜</h2>
  <p>說話卷四通常包括小組討論同個人回應。評核重點係溝通能力：可唔可以理解題目、提出相關意見、回應其他人、在有限時間推進討論，而唔係背一篇演講稿。實際流程同準備時間請以當年指示為準。</p>
  <ul>
    <li>開場：用一句複述題目範圍，再提出第一個可討論角度，邀請其他人補充。避免一開口講三分鐘。</li>
    <li>發展：每點用「意見 + 理由 + 短例子」。例子要具體，但唔好變成長篇故事。</li>
    <li>互動：同意時要加新資訊；唔同意時先概括對方意思，再講分歧同替代方案。只講 I disagree 會好弱。</li>
    <li>時間管理：如果討論停喺同一點，主動轉去題目另一部分，或者總結已有共識再往前。</li>
    <li>收束：留少少時間歸納兩至三個重點，而唔係突然停止。</li>
  </ul>
</section>
<section class="res-sec">
  <h2>有用、但唔好變成套語嘅功能句</h2>
  <p>下面只係功能方向，請用自己嘅字改寫，避免全組人講同一句。</p>
  <ul>
    <li>邀請：Maybe we could start with… / Would you like to add something about…</li>
    <li>澄清：If I understand you correctly… / Do you mean that…</li>
    <li>推進：Another issue the question asks us to consider is…</li>
    <li>溫和異議：I see your point, but one risk is… A possible alternative is…</li>
    <li>總結：So far we seem to agree on… We still need to decide…</li>
  </ul>
</section>
<section class="res-sec">
  <h2>個人回應</h2>
  <p>個人短答要直接回應提問，結構可用「立場或判斷 + 兩個理由 + 一句限制或例子」。唔好重覆小組討論已經講過嘅長段。如果問題要求你評估某個建議，記得兩邊都略為照顧，再先下結論。</p>
</section>
<section class="res-sec">
  <h2>練習方法</h2>
  <ul>
    <li>用一個社會或校園議題，限時討論四至五分鐘，錄音之後只檢查：有冇喺聽人、有冇壟斷、有冇離題。</li>
    <li>練習轉述別人意見，訓練自己唔好只等發言空隙。</li>
    <li>語氣自然、音量清楚、眼神照顧組員，比語氣演戲更重要。</li>
  </ul>
</section>
{official_links_html("eng")}
"""
    return "/eng/speaking/", render_page(
        path="/eng/speaking/",
        title="DSE 英文說話同小組討論技巧｜DSE Hub",
        description="原創整理 DSE English Paper 4 小組討論同個人回應嘅互動步驟、功能句同練習方法。",
        crumbs=C(("/eng/", "英國語文"), ("/eng/speaking/", None)),
        h1="說話同小組討論技巧",
        tagline="把討論當成共同完成任務，而唔係輪流背稿。重點係回應、推進同清楚表達。",
        body=body,
        schema_type="Article",
        nav_html=_eng_nav(),
        footer_back=("/eng/", "返回英國語文"),
    )


def _csd_nav():
    return nav([
        ("/resources/", "全科資源"),
        ("/csd/", "公民與社會發展"),
        ("/csd/themes/", "主題筆記"),
        ("/csd/exam-skills/", "資料回應技巧"),
    ])


def page_csd_landing():
    body = f"""
{COPYRIGHT_NOTE}
<section class="res-sec">
  <h2>科目簡介</h2>
  <p>公民與社會發展（下稱公民科）取代通識教育，成為甲類核心科目。成績匯報只設「達標」一級，低於該水平則標示為「未達標」，並唔採用第 1 至 5 級。課程圍繞香港、國家同當代世界三個主題，並包括內地考察等學習經歷；考察本身唔等於公開試卷，但主題知識同資料處理能力會喺筆試呈現。</p>
</section>
<section class="res-sec">
  <h2>公開評核（以 2027 年大綱為例）</h2>
  <p>公開考試只設一卷，時間約兩小時，全部為資料回應題，考生須就提供嘅資料回答全部題目。題型可以包括選擇、短答同短文章，視乎資料同課題性質而定。資料可以係文字、報道、圖表、地圖、漫畫或對話等。本站只解釋答題方法，唔會轉載任何試卷資料。</p>
</section>
<section class="res-sec">
  <h2>本站資源</h2>
  <div class="res-grid">
    {card_link("/csd/themes/","主題","三個主題溫習筆記","用自己嘅話整理「一國兩制」、改革開放以來嘅國家，以及互聯相依嘅當代世界。")}
    {card_link("/csd/exam-skills/","應試","資料回應答題框架","點樣讀資料、引用、比較同寫短文章，而唔係背標準答案。")}
  </div>
</section>
{official_links_html("csd")}
"""
    return "/csd/", render_page(
        path="/csd/",
        title="免費 DSE 公民與社會發展溫習資源｜DSE Hub",
        description="為 DSE 公民科提供三個主題嘅原創筆記，以及資料回應題答題框架。成績以達標／未達標匯報。",
        crumbs=C(("/csd/", None)),
        h1="DSE 公民與社會發展溫習資源",
        tagline="先掌握三個主題嘅基本概念，再用資料回應框架把概念寫入題目。請同時核對評核大綱。",
        body=body,
        schema_type="CollectionPage",
        nav_html=_csd_nav(),
        cta_html='<p class="page-cta"><a href="/csd/themes/">主題筆記</a> · <a href="/csd/exam-skills/">資料回應技巧</a> · <a href="/resources/">全科資源</a></p>',
    )


def page_csd_themes():
    body = f"""
{COPYRIGHT_NOTE}
<section class="res-sec">
  <h2>點樣用呢頁筆記</h2>
  <p>以下按課程常見嘅三個主題，用自己嘅話整理溫習線索。呢啲唔係官方課程指引摘要，亦唔取代教科書或內地考察經歷。讀每個主題時，練習用「事實概念 + 一個具體例子 + 對香港／國家／世界嘅意義」去記，考試先容易寫得準。</p>
</section>
<section class="res-sec" id="t1">
  <h2>主題一：香港特別行政區的「一國兩制」</h2>
  <p>呢個主題要求你理解香港作為國家不可分離部分，點樣喺「一國兩制」之下運作。溫習時可分成幾條線，而唔好背散亂時事：</p>
  <ul>
    <li>憲制秩序：憲法同《基本法》構成香港特區嘅憲制基礎；「一國」係前提，「兩制」係喺呢個前提下保持香港既有制度同生活方式。</li>
    <li>政權機構同法治：行政、立法、司法之間嘅關係，同特區政府依法施政。答題時用準確名稱，避免口語化空話。</li>
    <li>權利同義務：居民依法享有權利，亦有維護國家安全同遵守法律嘅責任。討論權利時要同時見到法律框架。</li>
    <li>國家安全同發展：理解維護國家安全同香港繁榮穩定之間嘅關係，用規範概念去寫，而唔好改寫成個人宣洩。</li>
    <li>參與同治理：認識特區嘅公共事務參與途徑，以及青年同社會喺建設香港中可以扮演嘅角色。</li>
  </ul>
</section>
<section class="res-sec" id="t2">
  <h2>主題二：改革開放以來的國家</h2>
  <p>焦點係 1978 年以來國家喺政治、經濟、社會同對外關係上嘅發展路徑。建議按「改革開放前嘅背景—政策方向—具體領域變化—對香港同世界嘅意義」去整理。</p>
  <ul>
    <li>發展道路：理解中國特色社會主義發展階段，以及改革開放點樣改變生產力同人民生活。</li>
    <li>經濟同民生：工業化、城市化、科技創新、脫貧同共同富裕等議題，要用可觀察嘅改變去說明，而唔好只寫「進步咗好多」。</li>
    <li>國家治理同法治建設：認識國家機構同政策如何應對大型治理課題。</li>
    <li>文化自信同民族關係：尊重中華文化同各族群共同發展，避免刻板印象。</li>
    <li>香港同國家發展：把握香港喺國家發展大局中嘅功能，例如專業服務、國際聯繫同創新科技合作等，用具體領域去寫。</li>
  </ul>
</section>
<section class="res-sec" id="t3">
  <h2>主題三：互聯相依的當代世界</h2>
  <p>呢個主題睇當代世界點樣因為經濟、科技、公共衛生、環境同國際組織而互相影響。答題時要同時見到機遇同風險，避免單一故事。</p>
  <ul>
    <li>經濟全球化：貿易、產業鏈、金融流動可以帶來增長，亦可能放大衝擊。要用「互相依賴」去解釋，而唔係只讚或只罵全球化。</li>
    <li>科技同資訊：科技加速交流，亦帶來網絡安全、私隱同數碼鴻溝等課題。</li>
    <li>公共衛生同環境：流行病、氣候變化同可持續發展，說明單一地區難以獨自解決。</li>
    <li>國際合作同秩序：認識國際組織同多邊合作嘅功能同限制，評論時要有根據。</li>
    <li>青年同世界：理解全球議題點樣影響日常生活，並思考負責任參與嘅方式。</li>
  </ul>
</section>
<section class="res-sec">
  <h2>跨主題連結</h2>
  <p>公開卷常常用一組資料同時觸及本地、國家同世界。溫習時預先準備兩至三個可以橫跨主題嘅例子，例如公共衛生事件、科技合作或經貿聯繫，但例子要服務題目，唔好硬套。答題步驟見<a href="/csd/exam-skills/">資料回應技巧</a>。</p>
</section>
{official_links_html("csd")}
"""
    return "/csd/themes/", render_page(
        path="/csd/themes/",
        title="DSE 公民科三個主題溫習筆記｜DSE Hub",
        description="用自己嘅話整理公民與社會發展三個主題：一國兩制、改革開放以來的國家、互聯相依的當代世界。",
        crumbs=C(("/csd/", "公民與社會發展"), ("/csd/themes/", None)),
        h1="公民科主題筆記",
        tagline="按三個主題整理概念線索同可寫入資料題嘅角度。請同時參閱課程指引同課堂材料。",
        body=body,
        schema_type="Article",
        nav_html=_csd_nav(),
        footer_back=("/csd/", "返回公民與社會發展"),
        cta_html='<p class="page-cta"><a href="#t1">主題一</a> · <a href="#t2">主題二</a> · <a href="#t3">主題三</a> · <a href="/csd/exam-skills/">答題框架</a></p>',
    )


def page_csd_skills():
    body = f"""
{COPYRIGHT_NOTE}
<section class="res-sec">
  <h2>先讀資料，再寫概念</h2>
  <p>公民科全卷都要根據題目提供嘅資料作答。高分答案通常不是背誦長段課文，而係：準確讀懂資料、用課程概念命名你見到嘅現象，再按題目指令比較、解釋或提出看法。以下框架適合選擇題之外嘅短答同短文章。</p>
  <ol>
    <li>審題動詞：指出、說明、比較、解釋、討論、評鑑，要求嘅深度唔同。「指出」要精準；「評鑑」要有準則同正反。</li>
    <li>標記資料：每則資料用一句话寫「佢主張／顯示咩」。圖表先讀標題、單位、趨勢，先再下判斷。</li>
    <li>對應概念：問自己呢則資料屬於邊個主題、邊個概念（例如法治、權利義務、改革開放、相互依存）。概念名稱要準確。</li>
    <li>引用方法：用「資料 X 顯示…，呢點可以說明…」把證據同概念接起來。只抄資料或只寫概念，兩者都唔夠。</li>
    <li>短文章：用兩至三段，每段一個功能。結論回應題目，唔好突然引入從未討論嘅新例子。</li>
  </ol>
</section>
<section class="res-sec">
  <h2>常見失分</h2>
  <ul>
    <li>忽略資料限制：一張圖只涵蓋某時段或某地，就唔好推成全世界永遠如此。</li>
    <li>立場先行：未處理資料就宣示態度，或者把試卷寫成情緒表達。</li>
    <li>概念錯配：用錯名稱，或者把不同層次嘅制度概念混為一談。</li>
    <li>比較題只寫 A，漏咗 B，或者沒有共同準則。</li>
  </ul>
</section>
<section class="res-sec">
  <h2>選擇題同短答</h2>
  <p>選擇題先排除明顯同資料相反嘅選項，再睇剩餘選項係唔係「講得通但越權推斷」。短答先寫關鍵句，再補一個資料證據，避免空泛形容詞。</p>
</section>
{official_links_html("csd")}
"""
    return "/csd/exam-skills/", render_page(
        path="/csd/exam-skills/",
        title="DSE 公民科資料回應答題框架｜DSE Hub",
        description="原創整理公民與社會發展資料回應題嘅審題、引用、比較同短文章寫作步驟。",
        crumbs=C(("/csd/", "公民與社會發展"), ("/csd/exam-skills/", None)),
        h1="公民科資料回應技巧",
        tagline="把資料證據同課程概念接起來，先寫得準、寫得夠。",
        body=body,
        schema_type="Article",
        nav_html=_csd_nav(),
        footer_back=("/csd/", "返回公民與社會發展"),
    )


def all_pages():
    return [
        page_eng_landing(),
        page_eng_writing(),
        page_eng_speaking(),
        page_csd_landing(),
        page_csd_themes(),
        page_csd_skills(),
    ]
