#!/usr/bin/env python3
"""
update_data.py — 每天抓取一次世界杯进球数据，生成 data.json 供前端读取。

数据源：API-Football (https://www.api-sports.io/)  —— 免费档每天 100 次请求。
本脚本按“每天一次、当天比赛全部结束后”运行设计，请求量很小：
  1 次取赛程 + 仅对“当天新结束的比赛”各取 1 次进球事件。
已结束的比赛会缓存在 state.json，不重复请求。

环境变量：
  APISPORTS_KEY   必填，API-Football 的 key
  WC_LEAGUE_ID    选填，世界杯 league id（API-Football 里通常是 1）
  WC_SEASON       选填，默认 2026

输出：
  data.json            前端读取的进球榜
  state.json           已统计过的比赛缓存（下次增量更新用）
  club_overrides.json  人工/缓存的“球员→俱乐部/联赛”覆盖表（自动补全新球员）
"""
import os, json, sys, time
from datetime import datetime, timezone
import urllib.request, urllib.parse

KEY      = os.environ.get("APISPORTS_KEY", "").strip()
LEAGUE   = os.environ.get("WC_LEAGUE_ID", "1").strip()
SEASON   = os.environ.get("WC_SEASON", "2026").strip()
BASE     = "https://v3.football.api-sports.io"

DATA_F, STATE_F, OVR_F = "data.json", "state.json", "club_overrides.json"

# 英文联赛名 -> 中文（用于把 API 返回的俱乐部所属联赛转成中文显示）
LEAGUE_ZH = {
 "Major League Soccer":"美职联","Serie A":"意甲","La Liga":"西甲","Premier League":"英超",
 "Bundesliga":"德甲","Ligue 1":"法甲","Ligue 2":"法乙","Championship":"英冠","Eredivisie":"荷甲",
 "Primeira Liga":"葡超","Premiership":"苏超","Pro League":"沙特职业联赛","Stars League":"卡塔尔星级联赛",
 "Süper Lig":"土超","Russian Premier League":"俄超","Persian Gulf Pro League":"伊朗波斯湾联赛",
 "Super Liga":"塞尔维亚超","Liga Profesional Argentina":"阿甲","Czech Liga":"捷克甲级",
 "Superligaen":"丹麦超","Liga I":"罗马尼亚甲级","Prva Liga":"斯洛文尼亚甲级","Serie A Brazil":"巴西甲级",
 "Super League":"瑞士超","Ligat ha'Al":"以色列超","Stars League Iraq":"伊拉克星级联赛",
 "Bundesliga Austria":"奥地利甲级","NB I":"匈牙利甲级","Liga MX":"墨超","First Division":"塞浦路斯甲级",
 "Pro League UAE":"阿联酋联赛",
}
# 英文国家队 -> 中文（前端也有兜底，这里尽量补全）
NATION_ZH = {
 "Argentina":"阿根廷","Canada":"加拿大","USA":"美国","Germany":"德国","Sweden":"瑞典","New Zealand":"新西兰",
 "Norway":"挪威","France":"法国","England":"英格兰","Switzerland":"瑞士","Morocco":"摩洛哥","Brazil":"巴西",
 "Netherlands":"荷兰","Spain":"西班牙","Uruguay":"乌拉圭","Japan":"日本","Mexico":"墨西哥","Czechia":"捷克",
 "Czech Republic":"捷克","South Korea":"韩国","Korea Republic":"韩国","Bosnia & Herzegovina":"波黑",
 "Bosnia and Herzegovina":"波黑","Paraguay":"巴拉圭","Qatar":"卡塔尔","Scotland":"苏格兰","Australia":"澳大利亚",
 "Curacao":"库拉索","Ivory Coast":"科特迪瓦","Cote d'Ivoire":"科特迪瓦","Tunisia":"突尼斯","Saudi Arabia":"沙特阿拉伯",
 "Iraq":"伊拉克","Egypt":"埃及","Senegal":"塞内加尔","Iran":"伊朗","Austria":"奥地利","Jordan":"约旦",
 "Portugal":"葡萄牙","DR Congo":"刚果(金)","Congo DR":"刚果(金)","Croatia":"克罗地亚","Ghana":"加纳",
 "Colombia":"哥伦比亚","Uzbekistan":"乌兹别克斯坦","Cape Verde":"佛得角","Algeria":"阿尔及利亚",
 "South Africa":"南非","Haiti":"海地",
}

def api(path, **params):
    if not KEY:
        sys.exit("ERROR: 缺少环境变量 APISPORTS_KEY")
    url = BASE + path + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"x-apisports-key": KEY})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r).get("response", [])
        except Exception as e:
            if attempt == 2: raise
            time.sleep(2 + attempt*2)

def load(f, default):
    try:    return json.load(open(f, encoding="utf-8"))
    except Exception: return default

LIVE  = {"1H","HT","2H","ET","BT","P","LIVE"}
FINAL = {"FT","AET","PEN"}

def main():
    state = load(STATE_F, {})            # fixtureId -> {goals:[{player,nation}], status}
    ovr   = load(OVR_F, {})              # player -> [clubEn, leagueZh, nationZh]

    fixtures = api("/fixtures", league=LEAGUE, season=SEASON)
    fetched = 0
    for fx in fixtures:
        fid    = str(fx["fixture"]["id"])
        status = fx["fixture"]["status"]["short"]
        # 已缓存且已是终场 -> 跳过，省请求
        if fid in state and state[fid].get("status") in FINAL:
            continue
        if status not in FINAL and status not in LIVE:
            continue  # 未开赛
        events = api("/fixtures/events", fixture=fid); fetched += 1
        goals = []
        for ev in events:
            if ev.get("type") != "Goal":          continue
            detail = (ev.get("detail") or "")
            if detail in ("Missed Penalty",):     continue
            if detail == "Own Goal":              continue   # 乌龙不计入个人
            player = (ev.get("player") or {}).get("name")
            nation = (ev.get("team")   or {}).get("name")
            if player and nation:
                goals.append({"player": player, "nation": nation})
        state[fid] = {"status": status, "goals": goals}

    # 汇总每名球员进球数
    tally = {}   # (player,nation) -> count
    for fid, info in state.items():
        for g in info["goals"]:
            tally[(g["player"], g["nation"])] = tally.get((g["player"], g["nation"]), 0) + 1

    scorers = []
    for (player, nation), goals in tally.items():
        club = lg = ""
        if player in ovr:
            club, lg = ovr[player][0], ovr[player][1]
        else:
            # 新球员：查其当前俱乐部（仅对未知球员，请求很少）
            try:
                res = api("/players", search=player.split()[-1], season=str(int(SEASON)-1))
                if res:
                    st = max(res[0].get("statistics", []),
                             key=lambda s:(s.get("games",{}) or {}).get("appearences",0) or 0,
                             default=None)
                    if st:
                        club = (st.get("team") or {}).get("name","") or ""
                        lg   = LEAGUE_ZH.get((st.get("league") or {}).get("name",""), "")
            except Exception:
                pass
            ovr[player] = [club, lg, NATION_ZH.get(nation, nation)]  # 缓存，避免重复查
        scorers.append({
            "player": player, "nation": nation,
            "nationZh": NATION_ZH.get(nation, ovr.get(player, ["","",nation])[2] if player in ovr else nation),
            "goals": goals, "club": club, "league": lg,
        })

    scorers.sort(key=lambda x:(-x["goals"], x["player"]))
    out = {
        "updated": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "source": "API-Football, auto-generated",
        "count": len(scorers),
        "totalGoals": sum(s["goals"] for s in scorers),
        "scorers": scorers,
    }
    json.dump(out,   open(DATA_F, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(state, open(STATE_F,"w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(ovr,   open(OVR_F,  "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"OK: {len(scorers)} scorers, {out['totalGoals']} goals, fetched {fetched} fixtures' events")

if __name__ == "__main__":
    main()
