# CLAUDE.md — 项目说明与维护手册（给 Claude Code 的接手文档）

> 这份文档是项目的"操作手册"。Claude Code 每次会自动读取本文件。
> 它说明项目是什么、数据架构怎么设计、改动时必须遵守的规范，以便无缝接手维护。

---

## 项目概览

**FIFA World Cup 2026 Scorers / 2026 世界杯射手榜**

一个中英双语的 2026 美加墨世界杯进球榜网站，纯静态站点，托管在 GitHub Pages，数据每天通过 GitHub Actions 自动更新。

- 仓库：`roy2EZ/wc2026-scorers`
- 线上：https://roy2ez.github.io/wc2026-scorers/
- 当前版本：见根目录 `VERSION` 文件（当前 v1.5.2）

**重要约定：项目作者主要用中文沟通，所有回复和交付用中文。** 网站本身中英双语。

---

## 数据架构（核心，务必理解后再改）

设计原则见 `ARCHITECTURE.md`。核心是 **单一事实来源 + ID 关联 + 构建时校验**。曾经反复出现"同一俱乐部两个名字（皇马/皇家马德里）""号码丢失""同名球员错配"等问题，就是因为早期数据分散、靠运行时猜名字。现在已重构为关系型主表设计，**不要退回旧模式**。

### 三张主表（单一事实来源）

| 文件 | 作用 | 关键字段 |
|---|---|---|
| `players.json` | 球员主表，1248 人 | `id`(国家码-号码，如 `BRA-7`)、`name`、`nameZh`、`num`、`pos`、`posZh`、`nation`、`nationZh`、`club_id` |
| `clubs.json` | 俱乐部主表，457 家 | `id`(slug，如 `real-madrid`)、`name`(标准英文)、`nameZh`(标准中文)、`league`、`aliases`(所有别名写法) |
| `nations.json` | 国家主表，48 国 | `code`、`en`、`zh`、`flag`、`aliases` |

**关键设计**：
- 球员通过 `club_id` 关联俱乐部，**不存俱乐部名字符串**。俱乐部的名字/中文译名只在 `clubs.json` 定义一次。
- 进球者名 → 球员 id 的映射在 `scorer_map.json`（验证后锁定的确定性锚点）。

### 其他文件

| 文件 | 作用 |
|---|---|
| `scorer_map.json` | 进球者名 → 球员 id 的固定映射（133 条） |
| `data.json` | **产物**，由 `update_data.py` 自动生成。含 `version`、`scorers`（有进球者，已 JOIN 展开俱乐部名/中文/联赛）、`roster`（全员） |
| `update_data.py` | 每日运行：抓 openfootball 进球 → 解析到 player id → 按 id 累加 → JOIN clubs/nations → 写 data.json |
| `validate_db.py` | 构建时强制一致性校验，任何不一致 exit(1) |
| `index.html` | 前端（单文件，含内置快照兜底）。直接读 data.json 展开好的字段 |
| `VERSION` | 版本号单一来源，一行如 `v1.5.2` |
| `CHANGELOG.md` | 双语更新日志 |
| `.github/workflows/update.yml` | GitHub Actions 定时任务 |

---

## 数据流

```
players.json + clubs.json + nations.json + scorer_map.json
        │
        ▼  update_data.py（每日 / 手动）
openfootball 进球 → 解析 player id → 按 id 累加 → JOIN clubs/nations
        │
        ▼
     data.json（scorers + roster，已展开 club/clubZh/league）
        │
        ▼
   index.html 直接渲染（中文名来自 data：pzr=球员、czr=俱乐部、teamZh=国家）
```

---

## 改动时必须遵守的规范

1. **改数据前先理解主表关系**。俱乐部信息改 `clubs.json`，不要去 `players.json` 里加俱乐部名字符串。
2. **任何数据改动后，必须跑校验**：
   ```bash
   python validate_db.py    # 必须输出 ✅ 全部通过，否则不要部署
   python update_data.py     # 重新生成 data.json
   ```
3. **前端名字显示统一走 data.json**：球员用 `pzr(d)`、俱乐部用 `czr(d)` / `clubZhByEn`、国家用 `d.teamZh`。**不要新增临时的名字映射表**——这正是过去 bug 的根源。
4. **版本管理**：发新版时，改 `VERSION`（一处）→ data.json 会自动带上；同步改 `index.html` 顶部的 `APP_VERSION` 和页脚 `buildVer`；在 `CHANGELOG.md` 顶部加一条。三处版本号应一致，页脚会同时显示网页版本和 data 版本，便于排查缓存。
5. **JS 语法自检**：改完 index.html 里的脚本，提取 `<script>` 跑 `node --check`。
6. **新进球者无法自动匹配时**：`update_data.py` 日志会出现 `WARNING: unresolved scorer`。处理：在 `players.json` 按国家+俱乐部找到该球员 id，往 `scorer_map.json` 加一行 `"名字": "球员id"`。注意这是提示、不会让 workflow 失败。
7. **GitHub Pages 缓存**：改完用户需 Ctrl+Shift+R 强刷；页脚版本号用于诊断。
8. **日韩球员中文名用正确汉字原名**（如 上田绮世、孙兴慜），不要音译。

---

## 常见维护任务速查

- **改某俱乐部中文名**：编辑 `clubs.json` 对应条目的 `nameZh` → `python update_data.py` → 全站生效。
- **皇马等知名队**：按作者偏好用**全称**（皇家马德里，不用皇马）。
- **加新进球者映射**：编辑 `scorer_map.json`。
- **改射手榜/表格默认筛选**：index.html 里 `boardMin`（领跑榜，当前默认3）、`minG`（全部球员表，当前默认0=全部含0球）。
- **国旗缺失**：检查 `nations.json` 的 flag，以及 index.html 的 FLAG 表是否覆盖该国（注意带重音的国名如 Türkiye/Curaçao）。
- **发布后**：建议在 GitHub 打 tag（如 `v1.5.2`）存快照。

---

## data.json 自动更新与冲突处理（push 本地改动时照此做）

`data.json` 是**产物**，GitHub Actions 每天会自动重生成并 commit 到 `main`。机器人对自己永远 fast-forward，不会冲突。冲突只在**本地有改动要 push、而机器人在这期间也 push 过**时出现（分支分叉）。这不是 bug，按下面固定流程处理即可，对作者无感：

1. **动手前先同步**：改任何东西前 `git pull`（或 `git fetch`），基于最新 `main` 工作。
2. **push 前再同步一次**：`git fetch` 后若已分叉，用 `git rebase origin/main`。
3. **data.json 冲突一律以"重新生成"解决，不手动拼 JSON**：
   - 冲突时随便取一侧结束 rebase（`git checkout --ours data.json && git add data.json && git rebase --continue`），
   - 然后重跑 `python update_data.py` 用线上最新数据覆盖生成，再 `git add data.json` amend 进发布提交。
   - 产物永远以 `update_data.py` 的输出为准——**绝不手工合并 scorers/roster**。
4. **本地跑 update_data.py 报 SSL 证书错**（sandbox 限制）：先 `export SSL_CERT_FILE=$(python -c "import certifi;print(certifi.where())")` 再跑。CI 环境无此问题。
5. 重生成后照常 `python validate_db.py` 必须全绿，再 push。

---

## 已知边界 / 待办

- **长尾俱乐部中文名**：457 家中约 320+ 家冷门队无中文名（显示英文）。不影响一致性（不会重复），仅缺翻译。有进球者的俱乐部已全部有中文名。若长尾队出现进球者，校验会提示，补一个即可。
- **机器人会自动 commit data.json**：本地/网页改动前先 `git pull`；冲突处理见上方「data.json 自动更新与冲突处理」。
- **workflow 已升级到 Node 24 兼容版**（checkout v5 / setup-python v6）。

---

## 校验通过的当前状态（参考基线）

- players: 1248 ｜ clubs: 457 ｜ nations: 48 ｜ scorer_map: 133
- 一致性审计全绿：0 孤儿 club_id、0 重复俱乐部、0 多中文名、球员中文名 100% 覆盖、进球者俱乐部中文 100% 覆盖。
