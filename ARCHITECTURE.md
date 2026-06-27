# 数据架构设计 (Architecture Design)

## 核心问题诊断
反复出问题的根源：数据分散、命名不规范、缺少"单一事实来源"的强约束。
具体表现：
1. 俱乐部名一队多写法（Real Madrid / Real Madrid C.F.）→ 显示重复、统计分裂
2. 中文名分散在多处（PZH内嵌、names_zh、CZH），优先级混乱
3. 进球者匹配靠运行时模糊猜测 → 易错配
4. 国家名映射表手维护 → 漏国家

## 设计原则
1. **单一事实来源 (Single Source of Truth)**：每个实体(球员/俱乐部/国家)的所有属性，只在一个地方定义。
2. **ID 优先**：所有关联用稳定 ID，不用名字字符串。
3. **显示与数据分离**：英文名是数据键，中文名是显示属性，一对一绑定。
4. **构建时校验 (Build-time validation)**：数据生成时强制跑一致性检查，不合格就报错，绝不带病上线。
5. **归一在源头**：俱乐部/国家名进库时就归一，不在显示层临时拼。

## 实体设计

### clubs.json —— 俱乐部主表（新增，单一事实来源）
每家俱乐部一条，id 为稳定 slug：
{
  "id": "real-madrid",
  "name": "Real Madrid",          # 标准英文名（唯一）
  "nameZh": "皇家马德里",          # 标准中文名（唯一）
  "league": "西甲",
  "leagueEn": "La Liga",
  "country": "ESP",
  "aliases": ["Real Madrid C. F.", "Real Madrid CF", "Real Madrid Club de Fútbol"]
}

### players.json —— 球员主表
每名球员一条，俱乐部用 club_id 关联（不再存俱乐部名字符串）：
{
  "id": "ESP-7",
  "name": "Ferran Torres",
  "nameZh": "费兰·托雷斯",
  "num": 7, "pos": "FW", "posZh": "前锋",
  "nation": "Spain", "nationZh": "西班牙", "nationCode": "ESP",
  "club_id": "barcelona"           # ← 关联 clubs.json，不存名字
}

### nations.json —— 国家主表（新增）
{ "code": "ESP", "en": "Spain", "zh": "西班牙", "flag": "🇪🇸", "aliases": ["España"] }

### scorer_map.json —— 进球者名→球员id（保留）
{ "Lionel Messi": "ARG-10", ... }

## 数据流
build_db.py (构建期，本地跑一次)
  ├─ 解析 FIFA PDF → 球员原始数据
  ├─ 俱乐部归一：用 clubs.json 的 aliases 把所有写法映射到 club_id
  ├─ 中文名填充：players 的 nameZh、clubs 的 nameZh
  ├─ 强制校验（见下）
  └─ 输出 players.json + clubs.json

update_data.py (每日运行)
  ├─ 读 players.json + clubs.json + nations.json + scorer_map.json
  ├─ 抓 openfootball 进球 → 解析到 player_id
  ├─ 按 id 累加进球
  ├─ JOIN：player → club_id → clubs.json 取俱乐部名/中文/联赛
  └─ 输出 data.json（已展开所有显示字段）

index.html (前端)
  └─ 直接用 data.json 里展开好的字段，不再做任何名字映射/拼接

## 构建时强制校验（不通过就报错，拒绝输出）
1. 唯一性：每个 club_id 唯一；每个 player id 唯一
2. 无孤儿：每个 player.club_id 必须能在 clubs.json 找到
3. 归一完整：不存在两个 club 的归一化名相同（杜绝重复俱乐部）
4. 中文覆盖：所有"有进球者"的俱乐部/球员必须有 nameZh（否则报警）
5. 国家完整：所有 nationCode 必须在 nations.json 中
6. 一队一名：同一 club_id 只有一个 name 和一个 nameZh

## 显示规则（统一，不再有歧义）
- 俱乐部显示：clubs.json 的 nameZh（中文） + name（英文）
- 皇马 → 统一显示「皇家马德里」（用全称，符合你的偏好）
- 球员显示：players.json 的 nameZh + name
