# Changelog · 更新日志

All notable changes to **wc2026-scorers** are documented here.
本项目的重要变更都记录在此。版本号见根目录 `VERSION` 文件，并显示在网站页脚。

The version in `VERSION` is the single source of truth; `update_data.py` reads it into `data.json`, and the site footer shows it.
`VERSION` 文件是版本号的唯一来源；`update_data.py` 会把它写进 `data.json`，网站页脚也会显示。

---

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
