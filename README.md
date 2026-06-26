# wc2026-scorers · 2026 世界杯射手榜

一个**中英双语**的 2026 美加墨世界杯（FIFA World Cup 2026）进球榜网站，数据**每天自动更新**，托管在 GitHub Pages 上，零成本、零维护。

🔗 **在线地址**：https://roy2ez.github.io/wc2026-scorers/

---

## 功能一览

- **射手榜领跑者**：进球数排名，可按 全部 / 2+ / 3+ / 4+ / 5+ 球筛选；每行按进球档位自动上色（色阶随最高进球数动态调整，进多少球都不撞色）。
- **进球来自哪里**：三张柱状图——按**国家队** / 按**联赛** / 按**俱乐部**，可切换「进球数 / 进球人数」口径，每张图可选 Top 10 / 15 / 20 / 全部，俱乐部图还能按联赛下钻。
- **全部进球者**：可搜索、可按联赛筛选、可排序的完整表格，球员 / 国家队 / 俱乐部 / 联赛五列均中英双语。
- **统计概览**：总进球、进球球员、俱乐部、联赛、进球场次。
- **全站中英双语**，自适应手机 / 平板 / 电脑。

---

## 自动更新是怎么跑的

```
GitHub Actions (定时)  →  update_data.py 抓取数据  →  写入 data.json  →  自动提交
                                                              |
                                                              v
                          网页 index.html 加载时读取 data.json 显示最新数据
```

1. **数据源**：[openfootball/worldcup.json](https://github.com/openfootball/worldcup.json) —— 公共领域、免费、无需 API key，含每场逐个进球者（作者每场赛后更新）。
2. **抓取脚本** `update_data.py`：下载该 JSON，统计每名球员进球数（乌龙球不计入个人），解析所属俱乐部与联赛，写出 `data.json`。
3. **定时任务** `.github/workflows/update.yml`：比赛日**美西 9:00–23:00 之间每 30 分钟**跑一次（cron 用 UTC）。数据有变化才提交，无变化不提交。
4. **前端** `index.html`：内置一份快照可离线/秒显，加载时再抓取 `data.json` 覆盖为最新；页面顶部「更新于…」结尾会显示 `自动同步 Live`（已读到最新数据）或 `内置快照 Snapshot`（兜底）。

> 数据新鲜度取决于上游作者多久录入；任务跑成功后，最多 30 分钟内同步到网站。

---

## 文件结构

| 文件 | 说明 |
|---|---|
| `index.html` | 网站本体（前端 + 内置快照 + 读取 data.json 逻辑） |
| `data.json` | 当前进球数据，由脚本自动生成 |
| `update_data.py` | 每次运行抓取并生成 data.json 的脚本 |
| `club_overrides.json` | 人工核对的「球员 -> 俱乐部 / 联赛 / 国家队」对照表（最高优先级） |
| `squad_db.json` | 由 FIFA 官方 26 人名单解析的全员库（约 1248 人），新进球者俱乐部自动兜底 |
| `.github/workflows/update.yml` | GitHub Actions 定时任务配置 |

### 俱乐部解析优先级
`别名归一` -> `club_overrides.json`（人工核对，最准）-> `squad_db.json`（全员库，按 国家+姓 匹配）-> 留空「—」

---

## 手动跑一次（想立刻更新时）

仓库顶部 **Actions** -> 左侧 **Update WC2026 scorers** -> **Run workflow**。
跑完点进运行记录，`Fetch latest goals` 步骤会打印类似：

```
OK: 115 scorers, 160 goals, 54 matches with goals. 无俱乐部 0 人: 无
本次新增 3 球：
  + 新进球者 前田大然 (日本) 1 球
  ↑ Brian Brobbey +1 球
```

---

## 维护提示

- **新进球者没有中文名**：属正常（冷门球员译名表不可能全），在 `index.html` 的 `PZH`（球员）/ `CZH`（俱乐部）映射里补一条即可，补一次长期有效。
- **新进球者俱乐部显示「—」**：先看 `squad_db.json` 是否覆盖；如需精确，往 `club_overrides.json` 加 `"球员名":["俱乐部英文","中文联赛","中文国家队"]`。
- **时区**：`update.yml` 的 cron 按美西夏令时（PDT = UTC-7）换算。本届世界杯 7 月 19 日结束，不涉及冬令时切换。

---

## 数据口径

- 进球数据来源：FIFA 官方比赛数据与赛后报道（经 openfootball 整理）。
- 俱乐部 = 球员在各国 26 人名单中登记的所属球会。
- **乌龙球不计入**个人进球。
- 当前快照：**115 名进球者 · 160 粒进球 · 来自 54 场比赛**（会随自动更新变化）。

---

## 技术栈

纯静态站点：HTML + 原生 JavaScript + [Chart.js](https://www.chartjs.org/)；数据管线 Python（标准库，无第三方依赖）；GitHub Actions + GitHub Pages。无后端、无数据库、无 API key。
