# Changelog · 更新日志

All notable changes to **wc2026-scorers** are documented here.
本项目的重要变更都记录在此。版本号见根目录 `VERSION` 文件，并显示在网站页脚。

The version in `VERSION` is the single source of truth; `update_data.py` reads it into `data.json`, and the site footer shows it.
`VERSION` 文件是版本号的唯一来源；`update_data.py` 会把它写进 `data.json`，网站页脚也会显示。

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
