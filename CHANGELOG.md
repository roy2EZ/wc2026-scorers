# Changelog · 更新日志

All notable changes to **wc2026-scorers** are documented here.
本项目的重要变更都记录在此。版本号见根目录 `VERSION` 文件，并显示在网站页脚。

The version in `VERSION` is the single source of truth; `update_data.py` reads it into `data.json`, and the site footer shows it.
`VERSION` 文件是版本号的唯一来源；`update_data.py` 会把它写进 `data.json`，网站页脚也会显示。

---

## v1.11.1

- **进球时间分布·折线图重构为五阶段**：上半场 → **45+ 补时** → 下半场 → **90+ 补时** → **加时赛 ET**，各阶段整段背景着色区分（上半场青 / 下半场蓝 / 加时紫），补时段用更深同色并标注「补时 Stoppage」，「上半场 / 下半场 / 加时赛」阶段提示词同色显示；曲线从开场（0'）连续起步、各段首尾相连。90+ 补时与真正的加时赛（91-120'）在数据层彻底分开统计。
  Rebuilt the Goal Timing line chart into five phases (1H → 45+ stoppage → 2H → 90+ stoppage → extra time), each with its own tinted background and bilingual labels; second-half stoppage and real extra time are now tracked separately in the data.

## v1.11.0

- **「最新进球」板块升级为「最新赛果 Latest Results」**：此前只显示有进球的比赛，0-0（含淘汰赛点球决胜的 0-0）会被整场跳过。现在**所有已完赛比赛无论比分都收录**，无进球的场次显示「🚫 本场无进球 · No goals」占位行，点球大战比分照常展示。
  The "Latest Goals" section is now "Latest Results": every finished match is listed regardless of score. Goalless matches (including 0-0 decided on penalties) now appear with a "No goals" placeholder row instead of being skipped.

## v1.10.1

- **修复排行榜默认档位漏铜牌**：当进球/助攻数出现断档（如最高档是 7、6、4，缺 5）时，旧的"按数值 max-2"默认阈值会把铜牌档挡在门外。改为默认 = **第 3 高的实际档位**，保证金/银/铜三档始终露出，且与发牌口径一致。射手榜、助攻榜、进球大战统一。
  Fixed ranking boards hiding the bronze tier by default when values have gaps; the default threshold is now the 3rd-highest actual tier, so gold/silver/bronze always show.
- **柱状图奖牌支持并列**：进球来自哪里的国家队/联赛/俱乐部三张图，金/银/铜改为**按数值发牌**——同一数值并列的条目共享同一枚奖牌（此前按位置发牌，并列会错位）。
  Goal Origins charts now award medals by value, so tied entries share the same medal (previously assigned by position).

## v1.10.0

- **新增「助攻榜 Top Assists」板块**（射手榜正下方）：数据取自 **ESPN 官方赛事助攻榜**，全部解析到球员主库，显示中文名·俱乐部·联赛旗，并同时标注进球数；金/银/铜档位配色，配**动态档位筛选按钮**（与射手榜同一套金银铜逻辑）。
  Added a **Top Assists** board right below Top Scorers, sourced from ESPN's official tournament assist leaders, resolved to the player database (Chinese name · club · league) with goals shown alongside; gold/silver/bronze tiers and adaptive filter chips.
- **射手榜同分并列按助攻排序**：进球数相同时，助攻多者靠前（贴近 FIFA 金靴奖并列规则第 2 顺位），奖牌仍按进球档位发放。
  Ties in Top Scorers are now broken by assists (per FIFA Golden Boot rule 2); medals still follow the goal tier.
- **进球时间分布·每分钟折线图重构**：上半场补时 **45+**、下半场补时 **90+** 各自单独成段并着色标注、与正常时间连续不断线；统一为 **3 分钟**尺度；横坐标简化为 15/30/45/60/75/90。
  Rebuilt the per-minute line chart: first-half (45+) and second-half (90+) stoppage each shown as its own marked, connected segment; unified 3-minute scale; cleaner x-axis.
- **筛选按钮默认阈值改为按数值取金银铜**（`最高档-2`，如最高 8 → 默认 6+），中间断档也能正确露出前三档。
  Filter chips now default to the top-three tiers by value (`max-2`), robust to gaps.
- 「射手榜领跑者」更名为「**射手榜**」，与助攻榜对齐；隐藏「进球大战」板块；README 同步（删进球大战、加助攻榜）。
  Renamed the "Top Scorers" heading, hid the "Goal Fests" section, updated README accordingly.
- 数据修正：法国 Michael Olise 中文名改为「奥利塞」。
  Data fix: Michael Olise's Chinese name → 奥利塞.

## v1.9.5

**All Players — adaptive goal filter / 全部球员查询·自适应档位**
- The personal-goal threshold buttons now extend automatically with the current maximum (6+, 7+…), matching Top Scorers and Goal Fests; the default stays "All".
  个人进球总数档位按钮随当前最高进球数自动扩展（6+、7+…），与射手榜领跑者、进球大战一致；默认仍为「全部」。

**README**
- Merged the screenshots into the feature table (feature text left, screenshot right); Goal Origins is featured larger and split into three separate images (by Nation / League / Club).
  README 把截图并入功能表格（左文右图）；Goal Origins 放大并拆成三张独立截图（按国家队 / 联赛 / 俱乐部）。

## v1.9.4

**Goal Origins — per-chart controls / 进球来自哪里·每图独立**
- Each of the three charts (Nation / League / Club) now has its own Goals ↔ Scorers toggle, instead of one global switch — you can view different metrics side by side.
  三张图（国家队 / 联赛 / 俱乐部）各自拥有独立的「进球数 / 进球人数」切换，不再是一个全局开关——可并排对比不同口径。
- Changing one chart's filter (metric or Top-N, or the league drill-down) now re-renders only that chart, not all three.
  改动某张图的筛选（口径 / Top-N / 联赛下钻）只重画那一张，不再三张一起重渲染。

## v1.9.3

**Adaptive filters / 自适应筛选**
- Top Scorers and Goal Fests now build their threshold buttons dynamically from the data (e.g. 6+, then 7+ as goals climb), and default to a threshold that always keeps the top three tiers (gold/silver/bronze) visible.
  射手榜领跑者与进球大战的档位按钮改为按数据动态生成（如 6+，进球更多再加 7+），默认阈值始终露出前三档（金/银/铜）。
- Multi-goal Players and Goal Fests now list the most recent occurrence first within each tier.
  单场多球与进球大战：每个档位内最近发生的排在最上。

**Goal Timing line / 进球时间分布折线**
- The per-minute trend now handles stoppage time correctly: first-half stoppage counts at 45' (it can't extend into the second half), while second-half stoppage extends naturally past 90' (90+1→91'…) instead of piling into a single spike.
  每分钟趋势线修正补时处理：上半场补时并入 45'（不能外延到下半场），下半场补时按真实分钟向 90 后自然延伸（90+1→91'…），不再堆成一根尖刺。

## v1.9.2

**Dual-source results / 双源比赛结果**
- Added ESPN as an auxiliary results feed: openfootball stays the record source, and ESPN fills in matches openfootball hasn't logged yet (so results appear sooner). Team names from any source normalize to one canonical key; scorer names resolve to player IDs accent-insensitively. If ESPN is unavailable the run falls back to openfootball only.
  新增 ESPN 作为辅助结果源：openfootball 仍为记录源，ESPN 补齐它还没录入的场次（结果更快出现）。任何源的队名归一化到统一键，进球者名以重音无关方式解析到球员 ID；ESPN 不可用时自动退回纯 openfootball。
- README rewritten with a full screenshot section (one per feature) and dual-source data notes. Raúl Jiménez → 希门尼斯.
  README 重写，加入按功能分节的完整截图区与双源说明；劳尔·希门尼斯译名修正为希门尼斯。

## v1.9.1

**Latest Goals feed — polish / 最新进球时间流·打磨**
- Days fold into per-day accordion panels colored by their stage — group rounds (1/2/3 = teal/blue/purple) and knockout rounds (R32 gold → final red); the latest day stays open by default. Match headers now show Match #, Round + Group on separate lines, two-color scoreline, host city (English over Chinese), and a penalty-shootout line with the goal-net icon aligned under the score. Penalty goals show the ⚽ pip plus a red "点球 Penalty" label; long nation names wrap instead of truncating.
  最新进球按天折叠成面板、按阶段着色（小组 1/2/3 = 青/蓝/紫，淘汰赛 32 强金→决赛红），最新一天默认展开。比赛组头显示 Match 编号、Round 与 Group 分两行、两色比分、主办城市（英文上中文下），以及与比分对齐的点球大战行（🥅）。点球进球显示 ⚽ + 红色「点球 Penalty」；长国名换行不截断。
- Fixed the group-round计算 (each group's 6 games split 2-per-round by date order, so rounds are 1/2/3 — not inflated by split-date fixtures).
  修复小组轮次计算（每组 6 场按时间每 2 场一轮，得 1/2/3；不再因同轮分两天而虚增）。

**Data fixes / 数据修复**
- Own goal by Morocco's keeper now resolves to 博诺 (Yassine Bono / "Bounou"); Morocco's Issa → 迪奥普 (Issa Diop, Fulham). Scoreboard first card: "games" (dropped "played") and "Round of 32" (dropped "Now").
  摩洛哥门将乌龙球正确解析为博诺（Yassine Bono / 源写作 Bounou）；摩洛哥 Issa → 迪奥普（Issa Diop，富勒姆）。记分板第一卡："games"（去 played）、"Round of 32"（去 Now）。

## v1.9.0

**Latest Goals feed / 最新进球时间流**
- New section at the top: every goal grouped by match, newest first. The latest match day is expanded by default (and can be collapsed); earlier days fold behind one "Earlier days" toggle, each day expandable on its own. Each match header shows Match #, group/round, the two teams (flag + zh/en) with a two-color scoreline (each team's flag color), and the host city; goals list minute (colored by the scoring team), scorer (zh/en), and club (league flag + zh/en). Scorelines are aligned across cards.
  顶部新增板块：全部进球按比赛分组、最新在前。最新比赛日默认展开（可收起），更早的折进一个"查看更早"按钮、每天独立展开。每场组头含 Match 编号、小组/淘汰赛阶段、两队（旗+中英）与两色比分（各取本队旗色）、主办城市；进球行含分钟（按进球方上色）、球员（中英）、俱乐部（联赛旗+中英）。各卡比分对齐。

**Goal Timing — per-minute line / 进球时间分布·每分钟折线**
- Added a smoothed per-minute line chart (3-minute bins) by actual elapsed minute, including stoppage time and extra time, with hydration-break markers on the axis.
  新增每分钟进球折线图（3 分钟聚合）：按真实累计分钟、含补时与加时，横轴标出补水时间。

**Fixes & polish / 修复与打磨**
- Fixed league flags missing site-wide after the earlier league-name shortening (flag table re-keyed to current names); long nation name "Bosnia & Herzegovina" shows as "Bosnia"; All Players feed/table column alignment tightened.
  修复联赛名缩短后全站联赛国旗丢失的问题（旗帜表改用当前短名）；波黑英文统一显示 Bosnia；最新进球与全部球员表的列对齐优化。

## v1.8.0

**No more built-in snapshot / 移除内置快照**
- The page no longer ships an embedded scorer snapshot. Data now comes solely from `data.json`: the first paint shows a loading state, then renders; if `data.json` can't be fetched it shows a clear failure message. This removes the brief "flash of stale data" and shrinks the HTML.
  网页不再内置一份冻结的射手快照。数据完全来自 `data.json`：首屏显示加载状态、随后渲染；拉取失败则显示明确的失败提示。消除了"闪一下旧数据"的问题，HTML 也更小。

**All Players table — width-friendly redesign / 全部球员表 · 省宽重排**
- Club and League merged into one column, so the table is now four columns (Player / Nation / Goals / Club·League). Long fields stack vertically instead of overflowing: player name splits Chinese (on ·) and English (given/surname) onto separate lines, the nation column puts jersey number and position on their own lines, and Club·League shows club zh / club en / league (with league flag) / league en. Fixed single-source column widths adapt cleanly to phones.
  俱乐部与联赛合并为一列，表格变为四列（球员 / 国家队 / 进球 / 俱乐部·联赛）。长内容改为纵向堆叠而非溢出：球员名中文按「·」、英文按名/姓分行；国家队列号码与位置各占一行；俱乐部·联赛分四行（俱乐部中/英、联赛带国旗/英）。固定的单一来源列宽在手机上自适应良好。
- Headers are now bilingual two-line (Chinese over English) with the sort arrow on the Chinese line; goal tallies are larger and brighter with a tier-colored glow, matching the other sections; jersey numbers shown as badges.
  表头改为中文一行、英文一行（排序箭头在中文行）；进球数字加大加亮、带档位同色微光，与其他板块统一；号码以徽章显示。

**Links & footer / 链接与页脚**
- All links use the gold theme color with no underline; the footer reads `version · build · data updated` (dropped the duplicate version, ID-architecture label and player/club counts). README refreshed and slimmed for v1.7.0+; unused screenshots removed.
  全站链接统一金色、无下划线；页脚精简为 `版本 · 构建 · 数据更新`。README 重写精简，删除无用截图。

## v1.7.0

**Official WC26 black-and-gold theme / 官方黑金主题**
- Recolored the whole site around the official FIFA World Cup 26 identity: the key-visual multicolor palette (red / orange / lime / teal / blue / purple) drives scoreboard accents and data bars, while titles, section headings, filter buttons and links share a black-and-gold treatment inspired by the trophy and the FIFA Fan ID. Goal-count numbers share one tier color scale across Top Scorers, Multi-goal, Goal Fests and the All Players table.
  全站围绕 FIFA World Cup 26 官方视觉重新配色：取自主视觉的多彩色板（红/橙/柠绿/青/蓝/紫）用于记分板强调条与数据柱；标题、版块标题、筛选按钮与链接统一为呼应大力神杯与 FIFA Fan ID 的黑金风格。进球数数字在领跑者 / 单场多球 / 进球大战 / 全部球员表中统一为同一套档位色阶。

**Layout & sections / 布局与板块**
- New header order: title → live/updated line → six stat cards → concise bilingual bullet intro. Sections reordered (Top Scorers → Goal Origins → All Players → Multi-goal → Goal Fests → Goal Timing) with a clearer gold divider between them.
  页头重排：标题 → 实时追踪/更新 → 六张卡 → 精简双语要点；板块顺序调整，板块之间用更清晰的金色分隔线。
- Goal Fests cards align the scoreline across cards and reflow to two rows on narrow screens; Goal Timing labels left-aligned with an aligned time column; goal-origin chart titles enlarged and two-tone.
  进球大战卡片比分跨卡对齐、窄屏两行布局；进球时间分布成语左对齐、时间列对齐；进球来自哪里图表标题加大并双色。

**Data & fixes / 数据与修复**
- English club names render consistently everywhere via one abbreviation pass (PSG spelled out; very long names like Wolves / M'gladbach stay short); long league names normalized to short forms; Manchester City → 曼城; Pafos FC Chinese name added.
  俱乐部英文名经统一缩写规则处处一致（PSG 全写；狼队 / 门兴等超长名保持短写）；长联赛名规范化为短名；曼彻斯特城→曼城；补 Pafos FC 中文名。
- Fixed combobox dropdown not reopening after clearing a filter; jersey numbers shown as badges in Top Scorers cards and the All Players table; row-count line now reads logically when "All" includes 0-goal players; All Players table uses a single-source fixed column layout; Own Goals section hidden.
  修复 combo 清除后下拉不再弹出的 bug；领跑者卡片与全部球员表以徽章显示国家队号码；选「全部」含 0 球球员时计数文案改为合理表述；全部球员表改为单一来源固定列宽；乌龙球板块隐藏。

## v1.6.2

**Searchable filters / 可搜索筛选**
- The All Players search is rebuilt as four independent comboboxes — Player / Nation Team / League / Club — that combine free-text fuzzy search with a pick-from-list dropdown (the league filter is now type-to-search too). Player is typeahead-only (bilingual suggestions as you type); the other three open a filterable list. Filters stack (AND), each with a clear button and full keyboard nav. A "Goals" threshold (All / 1+…5+) rounds it out.
  全部球员查询的搜索改为四个独立可搜索下拉——球员 / 国家队 / 联赛 / 俱乐部——把"打字模糊查找"与"下拉点选"合二为一（联赛也能输入筛选了）。球员为纯输入式 typeahead（边打边出双语建议），其余三个可点开筛选列表。多条件叠加（AND），各带清除按钮与完整键盘操作，外加个人进球总数档位（全部 / 1+…5+）。

**Charts / 图表**
- The three Goal Origins charts get taller rows and larger bilingual labels with a content-aware left gutter; the Goal Timing histogram bars are taller too.
  三个进球来自哪里柱状图行更高、双语标签更大、左侧留白按最长中文名自适应；进球时间分布柱条也加高。

---

## v1.6.1

**Layout & readability polish / 布局与可读性打磨**
- Reworked the header into a concise Chinese-then-English lead (no more language ping-pong), PST update time on two lines, openfootball credit and a star link to the repo. The top scoreboard is reordered (Total goals first, schedule last) with English-over-Chinese labels and per-card accent colours.
  页头重排为先中后英的简洁引言，更新时间按美西时区分两行，致谢 openfootball 并附仓库 Star 链接。顶部数据条重新排序（总进球在前、赛程在最后），标签英文在上中文在下，每张卡片彩色边条。
- **Top Scorers** and **Goal Fests** now group cards by goal total — same tally shares a row (up to 2 wide), a different tally starts a new row. **Multi-goal** is a tidy two-line tab bar (brace / hat-trick / haul / glut) with a 2-up grid and goal-count-keyed card borders.
  **领跑榜**与**进球大战**按进球数分组——同数同一行（最多两列），不同数另起一行。**单场多球**改为整齐的双行标签栏，两列网格，卡片边框按进球数上色。
- The three **Goal Origins** charts get taller rows, larger bilingual labels and a content-aware left gutter so long Chinese names (e.g. 巴黎圣日耳曼) show in full.
  三个**进球来自哪里**柱状图行更高、双语标签更大、左侧留白按最长中文名自适应，长名（如巴黎圣日耳曼）完整显示。

**Data / 数据**
- **Goal Timing now includes own goals** (they're goals too) — totals rise accordingly. Famous players are shown by surname where convention dictates (特罗萨德, 卢卡库, 萨拉赫…) while common surnames keep the given name (乔纳森·戴维, 路易斯·迪亚斯). Venue names dropped the parenthetical suffix.
  **进球时间分布纳入乌龙球**（乌龙也是进球），总数相应上升。按足球圈惯例，姓氏独特者用单姓（特罗萨德、卢卡库、萨拉赫…），姓氏常见者保留名（乔纳森·戴维、路易斯·迪亚斯）。场地名去掉括号后缀。

---

## v1.6.0

**New stat sections / 新增统计板块**
- **Multi-goal Games / 单场多球**: tabbed board (brace / hat-trick / haul / glut) listing every multi-goal performance — player, matchup with score, venue & date, penalty pips, card border colour-keyed to the goal count (same scale as the Top Scorers board). Tabs show live counts.
  **单场多球**：标签页切换（梅开二度 / 帽子戏法 / 大四喜 / 五子登科），列出每场多球表演——球员、对阵比分、场地与日期、点球标识，卡片边框按进球数上色（与领跑榜同一色阶）。标签显示实时数量。
- **Goal Timing / 进球时间分布**: a 7-phase heat-mapped histogram by match stage (闪电进球 / 初见端倪 / 中盘厮杀 / 再接再厉 / 放手一搏 / 终场绝杀 / 一战再战) plus the tournament's earliest & latest goal.
  **进球时间分布**：按比赛阶段分 7 段的热力图柱状图，外加全届最早 / 最晚进球。
- **Goal Fests / 进球大战**: highest-scoring matches with a 4+/5+/6+/7+ threshold filter, symmetric bilingual matchup, score, venue, match number.
  **进球大战**：单场进球最多的比赛，含 4+/5+/6+/7+ 档位筛选、对称中英对阵、比分、场地、场次。
- **Top Scorers / 射手榜领跑者** gains a per-league filter (个人 league leaderboards) and the three **Goal Origins** charts gain 🥇🥈🥉 medals on each top 3 (dynamic with filters).
  **射手榜领跑者**新增按联赛筛选（各联赛个人榜），三个**进球来自哪里**柱状图前三名加金银铜牌（随筛选动态）。

**Data integrity / 数据整治**
- Fixed 6 NUL-byte-corrupted names (Benfica, Sheffield United, Vélez Sarsfield, Kifisia + 2 players), merged 6 duplicate club entries (457 → 451 clubs), added Chinese names for 200+ major-league clubs, and English labels for all 58 leagues; normalized stray league/venue strings. `update_data.py` now emits a `funstats` block (multi-goal, timing, extremes, big matches) and per-match numbering. Consistency check green (1248 / 451 / 48).
  修复 6 处 NUL 字节损坏名（本菲卡、谢菲尔德联、贝莱斯、基菲西亚 + 2 名球员），合并 6 对重复俱乐部（457→451），补 200+ 主流联赛俱乐部中文名、58 个联赛英文名；归一游离联赛/场地写法。`update_data.py` 新增 `funstats`（多球 / 时间 / 最早最晚 / 大战）与比赛编号。一致性校验全绿（1248 / 451 / 48）。

**Header & polish / 页头与打磨**
- Rewrote the intro as a concise Chinese-then-English lead with thanks to the open-source openfootball project and a star link to this repo; trimmed the footer; many responsive type/colour/layout refinements across all cards.
  开场白重写为先中后英的简洁引言，致谢开源项目 openfootball 并附本仓库 Star 链接；精简页脚；各卡片大量响应式字号 / 配色 / 布局打磨。

---

## v1.5.6

**Responsive overhaul: Top Scorers, All Players table & charts / 响应式大改：领跑榜、球员表与图表**
- **Top Scorers board** now stacks each scorer over four lines — Chinese name (largest) / English name / Chinese club / English club — so long names and clubs are never truncated on narrow phones.
  **领跑榜**每位球员改为四行堆叠——中文名（最大）/ 英文名 / 中文俱乐部 / 英文俱乐部——窄屏手机上长名字和俱乐部不再被省略号截断。
- **All Players table** merges Nation + squad number + position into one column (number·position shown as a small line under the nation), narrows the Goals column, and uses a best-practice responsive width: fills the container with proportioned columns (Player 25% · Nation 18% · Goals 7% · Club 30% · League 20%), capped at the 1180px content width and scaling down to phones.
  **全部球员表**把国家队+号码+位置合并为一列（号码·位置作为国家队下方小字），收窄进球列，并采用最佳实践的响应式宽度：按比例填满容器（球员 25%·国家队 18%·进球 7%·俱乐部 30%·联赛 20%），上限 1180px 并向手机等比缩放。
- **The three bar charts** ("goals by nation / league / club") now adapt cleanly to any width: the left-label gutter steps down across four breakpoints, an `onResize` hook re-positions the overlay labels instantly, value numbers flip inside the bar when there's no room, and a CSS grid `min-width:0` fix stops the cards from overflowing narrow phones.
  **三个柱状图**（按国家队/联赛/俱乐部）现可干净适配任意宽度：左侧标签留白按四档收窄、`onResize` 即时重定位叠加标签、柱尾数字没空间时翻入柱内、并以 grid `min-width:0` 修复窄屏卡片溢出。

**Data / 数据**
- Added English names/abbreviations for all 25 previously-unmapped leagues (Algeria, South Africa, A-League, J1, K League, Eredivisie-tier, etc.) — every league now shows a bilingual label. Normalized a stray "墨西哥联赛" club to the canonical "墨超" (Liga MX) in `clubs.json`. Consistency check green (1248 / 457 / 48 / 133).
  为此前缺失的 25 个联赛全部补上英文名/缩写（阿尔及利亚、南非、澳超、日职联、韩K联等）——所有联赛均显示双语标签。把 `clubs.json` 中游离的「墨西哥联赛」归一为标准「墨超」(Liga MX)。一致性校验全绿（1248 / 457 / 48 / 133）。

---

## v1.5.5

**"Updated" date now bilingual with year / "更新于"日期改为中英双语带年份**
- The header's *Updated* line now shows the full date in both languages — Chinese **2026年6月27日** (prominent) followed by English **Jun 27th, 2026** (with the correct ordinal suffix, auto 1st/2nd/3rd/…) — instead of the previous month-day-only `6月27日`. Time and Live/Snapshot tag unchanged.
  顶部"数据更新于"一行改为中英双语完整日期——中文 **2026年6月27日**（醒目）+ 英文 **Jun 27th, 2026**（自动正确的序数后缀 1st/2nd/3rd…），取代原先只有月日的 `6月27日`。时间与 Live/Snapshot 标记不变。

---

## v1.5.4

**Tournament progress card / 赛程进展卡片**
- The header scoreboard gains a **Schedule** card showing the current stage (e.g. *Group R3 / 小组赛第3轮*, knockout rounds, or *Completed / 已结束*) and matches played vs. total (e.g. 66/104). Stage is derived in `update_data.py` from the openfootball fixture list — group rounds are inferred per group, knockout rounds mapped bilingually — and written to a new `schedule` block in `data.json`.
  顶部数据条新增 **赛程 Schedule** 卡片，显示当前阶段（如 *小组赛第3轮 / Group R3*、淘汰赛轮次，或 *已结束 / Completed*）与已踢/总场次（如 66/104）。阶段由 `update_data.py` 从 openfootball 赛程推断（小组赛按各组分轮、淘汰赛中英对照），写入 `data.json` 新增的 `schedule` 字段。

**Top Scorers board redesign / 射手榜改版**
- Replaced the per-row progress bar with a cleaner **tier-tinted full row** plus a left accent bar, and added a dedicated **nation column** (flag + Chinese name) so the country reads at a glance. Medals are now awarded **by goal tier** — players tied on goals share the same medal — and the goal tally is larger and right-aligned.
  移除每行进度条，改为更克制的**整行档位底色** + 左侧强调条，并新增独立**国家列**（国旗 + 中文名）让国别一目了然。奖牌改为**按进球档位发放**——同球数并列同牌——进球数字加大并右对齐。

**All Players table / 全部球员表**
- Goal totals now carry a small magenta **“P” superscript** marking penalty goals (e.g. `3ᴾ²` = 3 goals incl. 2 penalties), with a bilingual note. The **Goals column moved up** next to Nation for faster scanning.
  进球数右上角新增品红 **“P” 角标**标注点球（如 `3ᴾ²` 表示 3 球含 2 点球），并加双语说明。**进球数列前移**至国家队旁，更易扫读。

**Misc / 杂项**
- The "Updated" line now shows the date prominently with a muted time. Fixed Jonathan David's Chinese name (乔纳森·戴维). Consistency check green (1248 / 457 / 48 / 133).
  "数据更新于" 一行突出日期、弱化时间。修正 Jonathan David 中文名（乔纳森·戴维）。一致性校验全绿（1248 / 457 / 48 / 133）。

---

## v1.5.3

**Top Scorers visual upgrade / 射手榜可视化升级**
- The Top Scorers board now renders each player's goals as actual football ⚽ icons (one per goal), with **medals** (🥇🥈🥉) for the top three and a **progress bar** in each row scaled to the leader's tally. Default threshold stays 3+ with the existing All / 2+ / 3+ / 4+ / 5+ chips.
  射手榜领跑者现在把每位球员的进球渲染成真实足球 ⚽ 图案（一球一个），前三名加**奖牌**（🥇🥈🥉），每行加按领跑者标定的**进度条**。默认仍为 3+，保留 全部/2+/3+/4+/5+ 筹码切换。
- **Penalty goals are now distinguished** with a magenta ring and a “P” badge, plus a bilingual legend below the board.
  **点球单独区分**：品红圆环 + “P” 角标，榜下附双语图例。
- The All Players table gains a subtle goal-tier **background gradient** for rows with 2+ goals (0–1 goal rows stay clean), echoing the board's color system.
  全部球员查询表为进球 ≥2 的行加了克制的档位**背景渐变**（0–1 球保持干净），与领跑榜配色呼应。

**Data / 数据**
- `update_data.py` now captures penalty goals from the openfootball source into a new `pens` field per player (plus a `totalPens` summary); `data.json` regenerated accordingly. Consistency check still green (1248 players / 457 clubs / 48 nations / 133 scorer-map).
  `update_data.py` 从 openfootball 源采集点球，写入每名球员的新字段 `pens`（并汇总 `totalPens`）；`data.json` 已重新生成。一致性校验仍全绿（1248 球员 / 457 俱乐部 / 48 国 / 133 映射）。
- Removed a stray duplicate `update.yml` from the repository root; the active workflow lives only at `.github/workflows/update.yml`.
  删除仓库根目录冗余的 `update.yml` 副本；生效的工作流仅在 `.github/workflows/update.yml`。

## v1.5.0

**Architecture / 架构升级（根治多语言与重复问题）**
- Introduced a proper relational design with **master tables**: `clubs.json` (every club once, with a canonical English name, Chinese name, and all alias spellings) and `nations.json` (code, EN, ZH, flag). Players now reference a club via `club_id` instead of storing a club-name string, so a club's name and Chinese translation are defined in exactly one place.
  引入规范的关系型设计与**主表**：`clubs.json`（每家俱乐部仅一条，含标准英文名、中文名、所有别名写法）与 `nations.json`（国家码、英文、中文、国旗）。球员通过 `club_id` 关联俱乐部，不再各自存俱乐部名字符串——俱乐部名与中文译名只在一处定义。
- This permanently fixes the recurring "same club shown under two names" problem (e.g. 皇马 / 皇家马德里). Real Madrid now consistently displays its full name **皇家马德里** everywhere.
  这从根本上修复了反复出现的「同一俱乐部两个名字」问题（如 皇马 / 皇家马德里）。皇马现在各处统一显示全称**皇家马德里**。
- Added `validate_db.py`, a **build-time consistency check** that must pass before data ships: it enforces unique ids, no orphan `club_id`, no duplicate clubs (by normalized name), full nation coverage, and Chinese-name coverage for everyone who has scored. If anything is inconsistent it errors out instead of shipping bad data.
  新增 `validate_db.py`，**构建时强制一致性校验**，数据上线前必须通过：检查 id 唯一、无孤儿 `club_id`、无重复俱乐部（按归一名）、国家完整、所有进球者有中文名。任何不一致就直接报错，绝不带病上线。
- `update_data.py` now JOINs player → `club_id` → `clubs.json` to expand club name / Chinese name / league at build time; the front end reads these expanded fields directly (no more runtime name-guessing).
  `update_data.py` 现在做 球员 → `club_id` → `clubs.json` 的 JOIN，在构建时展开俱乐部名/中文/联赛；前端直接读取展开字段（不再运行时猜名字）。

## v1.4.2

**Fixes / 修复**
- Unified duplicate club names: the same club no longer appears under two different names (e.g. 皇马 / 皇家马德里, FC Barcelona / Barcelona). All club English names are normalized to one canonical form in `players.json`, and Chinese names are deduplicated — so the "by Club" chart and the table now aggregate each club correctly.
  统一重复的俱乐部名：同一家俱乐部不再出现两个名字（如 皇马 / 皇家马德里、FC Barcelona / Barcelona）。`players.json` 里所有俱乐部英文名归一为唯一标准写法，中文名也去重——「按俱乐部」图表与表格现在能正确合并同一俱乐部。
- Added accurate Chinese names for all clubs that have scorers (28 more, e.g. 马德里竞技, 尤文图斯, 曼城, 狼队).
  为所有有进球者的俱乐部补全准确中文名（新增 28 个，如 马德里竞技、尤文图斯、曼城、狼队）。

## v1.4.1

**Fixes / 修复**
- Added the 5 missing national-team flags (Belgium, Türkiye, Ecuador, Panama, Curaçao); all 48 teams now show a flag.
  补全缺失的 5 面国家队国旗（比利时、土耳其、厄瓜多尔、巴拿马、库拉索），48 队国旗全部齐全。
- Smarter auto-matching for new goalscorers: name-similarity + uniqueness disambiguation, and the nation EN→ZH map is now built dynamically from `players.json` so no team is ever missed. Most new scorers (e.g. De Bruyne, Baena) now resolve automatically without manual mapping.
  增强新进球者自动匹配：名字相似度 + 唯一性消歧，且国家中英映射改为从 `players.json` 动态构建，任何队都不会漏。绝大多数新进球者（如德布劳内、巴埃纳）无需手动加映射即可自动解析。
- Fixed the GitHub Actions workflow failing on `club_overrides.json` (the file was removed); the commit step now stages only `data.json`.
  修复 GitHub Actions 因 `club_overrides.json`（已删除）报错失败的问题；提交步骤改为只暂存 `data.json`。
- Corrected Álex Baena (ESP-15) whose surname wasn't fully parsed from the squad PDF.
  修正巴埃纳（ESP-15）——其姓氏未能从名单 PDF 完整解析。

## v1.4.0

**Architecture / 架构重构**
- Rebuilt around a **single source of truth**: `players.json`, a master database of all 1,248 players, each with a stable `id` (nation-code + shirt number), Chinese & English name, number, position, nation, club, league.
  重构为**单一数据源**：`players.json` 权威数据库，收录全部 1248 名球员，每人有稳定 `id`（国家码+号码）、中英文名、号码、位置、国家队、俱乐部、联赛。
- Goals now attach to players **by id** via `scorer_map.json` (a verified, locked-in name→id map) instead of fuzzy name-matching each run — so number / position / club can no longer get lost or mismatched.
  进球改为通过 `scorer_map.json`（验证并锁定的 名字→id 映射）**按 id** 叠加，不再每次靠模糊匹配——号码/位置/俱乐部不会再丢失或错配。
- The site now reads Chinese names straight from the data (`nameZh`), so names are maintained in one place.
  网站直接从数据读取中文名（`nameZh`），译名只需在一处维护。
- Consolidated the old `roster.json` / `names_zh.json` / `club_overrides.json` / `squad_db.json` into `players.json` (these legacy files were later removed from the repo).
  把旧的 `roster.json` / `names_zh.json` / `club_overrides.json` / `squad_db.json` 合并进 `players.json`（这些历史文件随后从仓库删除）。

## v1.3.x

**Features & fixes / 功能与修复**
- "All Scorers" table upgraded to an **All Players database** of all 1,248 players, including those with 0 goals; added squad number & position columns, a three-level row count, and All / 1+ / 2+ / 3+ / 4+ / 5+ goal filters (default: All).
  「全部进球者」升级为**全部球员查询数据库**，收录全部 1248 人（含 0 球球员）；新增号码、位置列，三层计数，及 全部 / 1+ / 2+ / 3+ / 4+ / 5+ 进球筛选（默认：全部）。
- Search autocomplete dropdown (nations / clubs / players) with exact filtering on selection; fixed the search placeholder.
  搜索自动补全下拉（国家队 / 俱乐部 / 球员），点选即精确筛选；修正搜索框提示文案。
- Chinese names for all 1,248 players; corrected Japan & Korea names to proper kanji/hanja (e.g. 上田绮世, 孙兴慜) instead of transliteration.
  全部 1248 人中文名；修正日韩球员为正确汉字原名（如 上田绮世、孙兴慜），不再音译。
- Selected filter buttons now highlighted; added a footer version tag (`vX.Y.Z · build … · data …`) for easy cache/version checking.
  选中的筛选按钮高亮；页脚新增版本标记（`vX.Y.Z · build … · data …`），便于排查缓存/版本。
- Fixed Türkiye / Bosnia nation names and several mismatches (e.g. Vinícius, Raúl Jiménez vs. a goalkeeper, Gonzalo Plata's nationality).
  修正土耳其/波黑队名及多处错配（如维尼修斯、劳尔·希门尼斯撞门将、Gonzalo Plata 国籍）。

## v1.0 – v1.2

**Initial build / 初版**
- Bilingual goalscorer dashboard: Top Scorers, Goal Origins (by nation / league / club, Goals vs Scorers toggle), stats overview.
  中英双语进球榜：射手榜领跑者、进球来自哪里（按国家队/联赛/俱乐部，进球数/进球人数切换）、统计概览。
- Daily auto-update pipeline: GitHub Actions + `update_data.py` pulling free public data (openfootball), served via GitHub Pages.
  每日自动更新管线：GitHub Actions + `update_data.py` 抓取免费公开数据（openfootball），经 GitHub Pages 托管。
- App Store–style promo graphics and a bilingual README.
  App Store 风格宣传图与中英双语 README。
