# FIFA World Cup 2026 Scorers · 2026 世界杯射手榜

A **bilingual (English / Chinese)** goalscorer dashboard for the 2026 FIFA World Cup, backed by a full **1,248-player database** and styled in the official **WC26 black-and-gold** look. Updates daily, hosted free on GitHub Pages.

**中英双语**的 2026 美加墨世界杯进球榜，背后是 **1248 名球员的完整数据库**，黑金主题、每日自动更新、托管在 GitHub Pages，零成本。

🔗 **Live / 在线**: https://roy2ez.github.io/wc2026-scorers/

![App preview](screenshots/promo-en.png)

> Screenshots are being refreshed for the v1.7.0 black-and-gold redesign.
> 截图正在按 v1.7.0 黑金改版更新中。

---

## Features / 功能

- **Top Scorers / 射手榜领跑者** — goal ranking (All / 2+…5+), grouped by goal count; cards auto-colored by tier, with jersey number and penalty marks. 进球数排名，按进球数分组、自动上色，含号码与点球标记。
- **Goal Origins / 进球来自哪里** — three charts by Nation / League / Club, with a Goals ↔ Scorers toggle and Top 10/15/20/All. 三张图（国家队 / 联赛 / 俱乐部），可切换进球数/进球人数。
- **Multi-goal & Goal Fests / 单场多球 & 进球大战** — braces and hat-tricks per match, and the highest-scoring matches. 单场梅开二度/帽子戏法，以及单场进球最多的比赛。
- **Goal Timing / 进球时间分布** — all goals by match phase, plus the earliest and latest goal. 全部进球按阶段分布，并标出最早/最晚进球。
- **All Players / 全部球员查询** — searchable database of all 1,248 players (incl. 0-goal), with four stacking comboboxes (Player / Nation / League / Club). 可查询全部 1248 名球员（含 0 球），四个可叠加的搜索下拉。

Fully bilingual and responsive (phone / tablet / desktop). The footer shows `version · build · data-updated` for cache checks.
全站双语、自适应手机/平板/电脑；页脚显示 `版本 · 构建 · 数据更新` 便于排查缓存。

---

## Data architecture / 数据架构

**Single source of truth**: a master player database with stable IDs. Goals attach to players **by ID**, never by guessing names — so number, position, club and Chinese name never get lost or mismatched.

**单一数据源**：带稳定 ID 的球员主表。进球按 **ID** 精确叠加、绝不猜名字，号码/位置/俱乐部/中文名不会错配。

```
players.json + clubs.json + nations.json + scorer_map.json
        │  update_data.py  (fetch goals → resolve by id → tally → fun-stats)
        ▼
     data.json  (scorers + roster + funstats)
        │
        ▼
   index.html  renders everything
```

---

## Auto-update / 自动更新

- **Source / 来源**: [openfootball/worldcup.json](https://github.com/openfootball/worldcup.json) — public domain, no API key.
- **Schedule / 定时**: GitHub Actions runs `update_data.py` daily and commits only when data changes; can also be run manually (**Actions → Update WC2026 scorers → Run workflow**). 每天跑一次，有变化才提交，也可手动运行。
- **Front end / 前端**: ships a built-in snapshot, then fetches `data.json` for the latest. 内置快照秒显，再抓取最新数据覆盖。
- If a new scorer can't be matched, the log prints `WARNING: unresolved scorer` — add a line to `scorer_map.json` (`"Name": "player-id"`). 新进球者无法匹配时按日志提示补一行映射。
- **After the tournament / 赛事结束后**: once totals are confirmed against FIFA's official data, the scheduled job is disabled (manual run kept). 与 FIFA 官方核对一致后停用定时任务。

---

## File structure / 文件结构

| File | Description / 说明 |
|---|---|
| `index.html` | The site — front end + built-in snapshot + data loading / 网站本体 |
| `players.json` | Player master table (1,248) / 球员主表 |
| `clubs.json` · `nations.json` | Club & nation master tables / 俱乐部、国家主表 |
| `scorer_map.json` | Scorer name → player id map / 进球者名→id 映射 |
| `update_data.py` | Fetches goals, generates `data.json` / 抓取并生成数据 |
| `validate_db.py` | Build-time consistency check / 一致性校验 |
| `data.json` | Generated data (`scorers` + `roster` + `funstats`) / 数据产物 |
| `VERSION` | Single source of the version number / 版本号来源 |
| `.github/workflows/` | Scheduled update workflow / 定时任务 |

---

## Notes / 数据口径

- Goals from official FIFA data and post-match reports (via openfootball). 进球来自 FIFA 官方数据与赛后报道（经 openfootball 整理）。
- Club = the player's registered club in their squad. 俱乐部 = 球员国家队名单登记的球会。
- Own goals are **not** credited to individuals (still counted in timing). 乌龙球不计入个人进球（但计入时间分布）。

## Tech stack / 技术栈

Pure static site: HTML + vanilla JS + [Chart.js](https://www.chartjs.org/); Python data pipeline (stdlib only); GitHub Actions + Pages. No backend, no database, no API key.
纯静态：HTML + 原生 JS + Chart.js；Python 数据管线（仅标准库）；GitHub Actions + Pages。无后端、无数据库、无 API key。
