# FIFA-World-Cup-2026-Scorers · 2026 世界杯射手榜

A **bilingual (English / Chinese)** goalscorer dashboard for the 2026 FIFA World Cup, backed by a full **1,248-player database** and styled around the official **FIFA World Cup 26 black-and-gold** look. Data updates automatically every day, hosted on GitHub Pages — zero cost, zero maintenance.

一个**中英双语**的 2026 美加墨世界杯（FIFA World Cup 2026）进球榜网站，背后是一个**1248 名球员的完整数据库**，整体采用呼应官方主视觉的**黑金风格**。数据每天自动更新，托管在 GitHub Pages 上，零成本、零维护。

🔗 **Live site / 在线地址**: https://roy2ez.github.io/wc2026-scorers/

![App preview](screenshots/promo-en.png)

![应用预览](screenshots/promo-cn.png)

---

## Screenshots / 截图

> Screenshots are being refreshed for the v1.7.0 black-and-gold redesign — some images below may still show an earlier look.
> 截图正在按 v1.7.0 黑金改版更新中，下面部分图可能仍是旧版界面。

### Hero & stats overview / 顶部与统计概览
Title, live/updated line, and six stat cards: matches played, total goals, scorers, leagues, clubs, and matches with goals. The footer shows the page version, build time and data-update time.
标题、实时追踪/更新时间，以及六张统计卡：比赛进程、总进球、进球球员、涉及联赛、涉及俱乐部、进球场次。页脚显示网页版本、构建时间与数据更新时间。

![Hero & stats](screenshots/hero.png)

### Top Scorers / 射手榜领跑者
Goal ranking with All / 2+ / 3+ / 4+ / 5+ filters, grouped by goal count (each group headed by "N players"). Cards show nation flag + Chinese/English name + jersey number badge, club, and a goal-tally colored by its goal tier; penalty goals are marked.
进球数排名，可按 全部 / 2+ / 3+ / 4+ / 5+ 筛选，并按进球数分组（每组标注"N 人"）。卡片含国旗 + 中英文名 + 号码徽章、俱乐部，进球数按档位自动上色，点球单独标记。

![Top Scorers](screenshots/top-scorers.png)

### Goal Origins — by Goals / 进球来自哪里（进球数口径）
Three charts side by side: by Nation / League / Club. Each has its own Top 10 / 15 / 20 / All selector; the club chart can drill down by league.
三张图并排：按国家队 / 联赛 / 俱乐部。每张图各自可选 Top 10 / 15 / 20 / 全部，俱乐部图还能按联赛下钻。

![Charts by goals](screenshots/charts-goals.png)

### Goal Origins — by Scorers / 进球来自哪里（进球人数口径）
One toggle switches all three charts between "Goals" and "Scorers" (number of distinct players).
顶部一键切换，三张图同时在「进球数」与「进球人数」之间切换。

![Charts by scorers](screenshots/charts-scorers.png)

### All Players database / 全部球员查询数据库
A complete, searchable database of **all 1,248 players** across 48 teams — Chinese name, English name, jersey number, position, nation, club and league for every player, **including those with 0 goals**. Filter by All / 1+ / 2+ / 3+ / 4+ / 5+ goals; sort any column.
覆盖 48 队**全部 1248 名球员**的可查询数据库——每人都有中文名、英文名、号码、位置、国家队、俱乐部、联赛，**包含尚未/没有进球的球员**（进球数记为 0）。可按 全部 / 1+ / 2+ / 3+ / 4+ / 5+ 进球筛选，任意列可排序。

![All Players table](screenshots/table.png)

### Searchable filters / 可搜索筛选下拉
Four independent comboboxes — Player / Nation / League / Club — each combining free-text fuzzy search (English or Chinese) with a pick-from-list dropdown. Filters stack (AND), and the Club list narrows to the chosen League. Searching "Paris" / "巴黎" surfaces every Paris Saint-Germain player at once.
四个独立可搜索下拉——球员 / 国家队 / 联赛 / 俱乐部——每个都把"打字模糊查找"（中英文皆可）与"下拉点选"合二为一。多条件叠加（AND），选定联赛后俱乐部下拉只显示该联赛球队。输入「Paris / 巴黎」即可一次列出所有巴黎圣日耳曼球员。

| Search by club / 按俱乐部搜索 | Filter by league / 按联赛筛选 |
|:---:|:---:|
| ![Search by club](screenshots/search-club.png) | ![Filter by league](screenshots/filter-league.png) |

---

## Features

- **Top Scorers** — goal ranking, filterable by All / 2+ / 3+ / 4+ / 5+ goals and grouped by goal count; each card is auto-colored by its goal tier (the color scale adjusts to the current max, so tiers never clash), shows the player's jersey number, and marks penalty goals.
- **Goal Origins** — three bar charts: by **Nation** / by **League** / by **Club**, with a Goals / Scorers toggle, a Top 10 / 15 / 20 / All selector per chart, and league drill-down on the club chart.
- **Multi-goal Players per Game** — players who scored a brace or hat-trick in a single match (4- and 5-goal tiers appear automatically if anyone reaches them), with the match, scoreline, date and venue.
- **Goal Fests** — single matches with the most goals (4+ / 5+ / 6+ / 7+), shown as aligned bilingual scorelines with date and venue.
- **Goal Timing** — all goals by match phase (lightning start → last gasp → extra time), with hydration-break / half-time / full-time separators, plus the earliest and latest goal of the tournament.
- **All Players database** — every one of the **1,248 players** is searchable, with jersey number, position, nation, club and league; players with 0 goals are included so you can look up anyone. Searchable, league-filterable, goal-filterable and sortable; all columns bilingual.
- **Searchable filters** — four comboboxes (Player / Nation / League / Club), each combining English/Chinese fuzzy search with a pick-from-list dropdown; filters stack and the Club list follows the chosen League.
- **Stats overview** — matches played, total goals, scorers, leagues, clubs, and matches with goals.
- **Official WC26 black-and-gold theme**, **fully bilingual**, responsive across phone / tablet / desktop. A version line in the footer (e.g. `v1.7.0 · build … · data updated …`) makes it easy to confirm the live site is up to date.

## 功能一览

- **射手榜领跑者**：进球数排名，可按 全部 / 2+ / 3+ / 4+ / 5+ 球筛选并按进球数分组；每张卡按进球档位自动上色（色阶随最高进球数动态调整，进多少球都不撞色），显示国家队号码，点球单独标记。
- **进球来自哪里**：三张柱状图——按国家队 / 联赛 / 俱乐部，可切换「进球数 / 进球人数」口径，每张图可选 Top 10 / 15 / 20 / 全部，俱乐部图还能按联赛下钻。
- **单场多球**：单场梅开二度、帽子戏法的球员（若有人单场打进 4、5 球，大四喜 / 五子登科按钮会自动出现），并附比赛、比分、日期与场地。
- **进球大战**：单场总进球最多的比赛（4+ / 5+ / 6+ / 7+），以对齐的中英双语比分加日期、场地呈现。
- **进球时间分布**：全部进球按比赛阶段分布（闪电进球 → 终场绝杀 → 加时），中间有补水时间 / 中场休息 / 常规时间结束分隔，并标出全届最早与最晚的进球。
- **全部球员查询数据库**：**1248 名球员**逐一可查，含号码、位置、国家队、俱乐部、联赛；没进球的球员也收录，任意球员都能查到。可搜索、可按联赛筛选、可按进球数筛选、可排序，所有列中英双语。
- **可搜索筛选**：四个下拉（球员 / 国家队 / 联赛 / 俱乐部），各自把中英文模糊查找与下拉点选合二为一；多条件叠加，俱乐部下拉跟随所选联赛。
- **统计概览**：比赛进程、总进球、进球球员、联赛、俱乐部、进球场次。
- **官方黑金主题**，**全站中英双语**，自适应手机 / 平板 / 电脑。页脚有版本行（如 `v1.7.0 · build … · data updated …`），方便确认线上是否为最新版。

---

## Data architecture / 数据架构

The site is built on a **single source of truth**: one master player database with stable IDs. Goal data is attached to players **by ID**, never by guessing names — so a player's number, position, club and Chinese name can never get lost or mismatched.

网站建立在**单一数据源**之上：一个带稳定 ID 的权威球员数据库。进球数据通过 **ID** 精确叠加到球员上，绝不靠"猜名字"——所以球员的号码、位置、俱乐部、中文名不会丢失或错配。

```
players.json (1,248 players, each with a stable id like "BRA-7")
        |
        |  update_data.py  +  scorer_map.json (scorer name -> player id)
        v
openfootball goals  --resolved by id-->  goals added to each player
        |
        v
     data.json  (scorers = players who scored; roster = all 1,248 players)
        |
        v
   index.html  reads data.json and renders everything
```

1. **`players.json`** — the master database. One record per player: `id` (nation-code + shirt number, e.g. `BRA-7`), English name, Chinese name, number, position, nation, club, league. Built once for the tournament from official FIFA squad lists + curated Chinese names.
2. **`clubs.json` / `nations.json`** — master tables for clubs and nations; players reference a club by `club_id`, so a club's name and Chinese translation are defined exactly once.
3. **`scorer_map.json`** — a verified map from each goalscorer's name (as it appears upstream) to a player `id`. Resolved once and locked in, so the same player is never mismatched again.
4. **`update_data.py`** — fetches goals, resolves each scorer to an `id` (via the map; case/accent-insensitive, with a conservative fuzzy fallback for brand-new names), tallies goals by `id`, computes the fun-stats (multi-goal, goal fests, timing, earliest/latest), and writes `data.json`. Any name it can't resolve is logged so it can be added to the map.
5. **`index.html`** — reads `data.json` and renders the dashboard; Chinese names come straight from the database (`nameZh`).

1. **`players.json`**：权威数据库。每名球员一条记录：`id`（国家码 + 球衣号，如 `BRA-7`）、英文名、中文名、号码、位置、国家队、俱乐部、联赛。整届赛事构建一次，数据来自 FIFA 官方名单 + 人工校对的中文名。
2. **`clubs.json` / `nations.json`**：俱乐部与国家的主表；球员通过 `club_id` 关联俱乐部，俱乐部名字与中文译名只定义一次。
3. **`scorer_map.json`**：进球者名（上游写法）→ 球员 `id` 的验证映射。解析一次后锁定，同一球员不会再错配。
4. **`update_data.py`**：抓取进球，把每个进球者解析成 `id`（走映射表，大小写/音标无关，新球员有保守的兜底匹配），按 `id` 累加进球，计算趣味统计（单场多球、进球大战、时间分布、最早/最晚），写出 `data.json`。解析不了的名字会打印到日志，便于加进映射表。
5. **`index.html`**：读取 `data.json` 渲染页面；中文名直接取自数据库（`nameZh`）。

---

## How auto-update works / 自动更新是怎么跑的

```
GitHub Actions (scheduled)  ->  update_data.py fetches goals  ->  writes data.json  ->  auto-commit
                                                                       |
                                                                       v
                       index.html reads data.json on load and shows the latest data
```

1. **Goal source**: [openfootball/worldcup.json](https://github.com/openfootball/worldcup.json) — public domain, free, no API key, with per-match goalscorers (updated by the author after each match).
2. **Player database**: `players.json`, built from the official FIFA 26-man squad lists (1,248 players).
3. **Fetch script** `update_data.py`: downloads the goal JSON, resolves each scorer to a player id, tallies goals (own goals excluded from individuals), and writes `data.json`.
4. **Scheduled job** `.github/workflows/update.yml`: runs on a daily schedule (cron in UTC) and commits only when data changes. Can also be run manually via **Run workflow**.
5. **Front end** `index.html`: ships a built-in snapshot for offline/instant display, then fetches `data.json` to overwrite with the latest; a `Live` / `Snapshot` marker shows which is in use.

> Data freshness depends on how quickly the upstream author logs each match; once a job succeeds, the site syncs shortly after.

> **After the tournament**: once the final is played and totals are confirmed against FIFA's official data, the scheduled job is disabled (manual run kept for corrections).
> **赛事结束后**：决赛打完、与 FIFA 官方数据核对一致后，会停用定时任务（保留手动运行以备修正）。

---

## File structure / 文件结构

| File | Description / 说明 |
|---|---|
| `index.html` | The site itself — front end + built-in snapshot + data.json loading / 网站本体 |
| `players.json` | **Player master table** — all 1,248 players, each linked to a club by `club_id` / 球员主表 |
| `clubs.json` | **Club master table** — one record per club: canonical names, league, aliases / 俱乐部主表 |
| `nations.json` | **Nation master table** — code, English, Chinese, flag / 国家主表 |
| `scorer_map.json` | Verified map from goalscorer name → player id / 进球者名→球员 id 映射 |
| `validate_db.py` | Build-time consistency check (run before shipping data) / 构建时一致性校验 |
| `data.json` | Current data, auto-generated each run (`scorers` + `roster` + `funstats`) / 当前数据产物 |
| `update_data.py` | Fetches goals and generates data.json, attaching goals by player id / 抓取并生成数据 |
| `VERSION` | Single source of the version number / 版本号唯一来源 |
| `.github/workflows/` | GitHub Actions schedule config / 定时任务配置 |
| `screenshots/` | Images used in this README / README 用图 |

---

## Update the result manually / 手动跑一次数据更新

Repo top → **Actions** → **Update WC2026 scorers** → **Run workflow**. After it finishes, the `Fetch latest goals` step prints something like:

```
OK: 125 scorers, 175 goals, 57 matches with goals.
This run added 3 goal(s):
  + New scorer Daizen Maeda (Japan) 1 goal
  + 1 more goal: Brian Brobbey
```

If a brand-new scorer's name can't be matched automatically, the log shows a `WARNING: unresolved scorer name(s)` line — add that name to `scorer_map.json` (one line: `"Name": "player-id"`) and it's fixed for good.

仓库顶部 Actions → 左侧 Update WC2026 scorers → Run workflow。跑完点进运行记录，`Fetch latest goals` 步骤会打印类似上面的输出。若某个全新进球者无法自动匹配，日志会出现 `WARNING: unresolved scorer name(s)` —— 把该名字加进 `scorer_map.json`（一行：`"名字": "球员id"`）即可永久修复。

---

## Data notes / 数据口径

- Goal data sourced from official FIFA match data and post-match reports (compiled via openfootball). / 进球数据来源：FIFA 官方比赛数据与赛后报道（经 openfootball 整理）。
- Club = the player's registered club in their national-team squad. / 俱乐部 = 球员在各国 26 人名单中登记的所属球会。
- Own goals are **not** credited to individuals (they are still counted in the timing distribution). / 乌龙球不计入个人进球（但仍计入进球时间分布）。

---

## Tech stack / 技术栈

A pure static site: HTML + vanilla JavaScript + [Chart.js](https://www.chartjs.org/); data pipeline in Python (standard library, no third-party deps); GitHub Actions + GitHub Pages. No backend, no database, no API key.

纯静态站点：HTML + 原生 JavaScript + Chart.js；数据管线 Python（标准库，无第三方依赖）；GitHub Actions + GitHub Pages。无后端、无数据库、无 API key。
