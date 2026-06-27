#!/usr/bin/env python3
"""
update_data.py — 每天抓取一次世界杯进球数据，按"球员唯一ID"叠加，生成 data.json。

新架构（单一数据源）：
  players.json    —— 权威全员数据库：每名球员一条完整档案，含唯一 id(国家码-号码)、
                     中文名、号码、位置、国家队、俱乐部、联赛。整届赛事固定，构建一次。
  scorer_map.json —— 进球者名(openfootball) → 球员id 的固定映射，验证一次后锁定，
                     避免每次靠"猜名字"匹配导致的错配（号码/位置丢失、同名撞车等）。
  本脚本：抓 openfootball 进球 → 用 scorer_map 把进球者名解析成 id → 按 id 累加进球
          → 输出 data.json（scorers = 有进球的球员完整档案+进球数；roster = 全员+进球数）。
  新出现、map 里没有的进球者：用兜底模糊匹配解析，并在日志中提示加入 scorer_map。
无需任何环境变量 / key。
"""
import json, sys, unicodedata, urllib.request, re
from datetime import datetime, timezone

SRC="https://raw.githubusercontent.com/openfootball/worldcup.json/master/2026/worldcup.json"
DATA_F="data.json"; PLAYERS_F="players.json"; SMAP_F="scorer_map.json"; VERSION_F="VERSION"
CLUBS_F="clubs.json"; NATIONS_F="nations.json"

def read_version():
    """从 VERSION 文件读版本号（单一事实来源）。读不到则回退 'unknown'。"""
    try:
        return open(VERSION_F, encoding="utf-8").read().strip() or "unknown"
    except Exception:
        return "unknown"

ALIASES={"Deniz Undav":"Denis Undav","Giovanni Reyna":"Gio Reyna","Maxi Araújo":"Maximiliano Araujo",
 "Leo Østigard":"Leo Ostigard","Mostafa Zico":"Mostafa Ziko","Hassan Al-Haydos":"Hassan Al Haidos",
 "Mohammad Mohebbi":"Mohamed Mohebi","Agustín Cano":"Agustin Canobbio"}

NATION_ZH={"Argentina":"阿根廷","Canada":"加拿大","USA":"美国","United States":"美国","Germany":"德国",
 "Sweden":"瑞典","New Zealand":"新西兰","Norway":"挪威","France":"法国","England":"英格兰","Switzerland":"瑞士",
 "Morocco":"摩洛哥","Brazil":"巴西","Netherlands":"荷兰","Spain":"西班牙","Uruguay":"乌拉圭","Japan":"日本",
 "Mexico":"墨西哥","Czechia":"捷克","Czech Republic":"捷克","South Korea":"韩国","Korea Republic":"韩国",
 "Bosnia & Herzegovina":"波黑","Bosnia and Herzegovina":"波黑","Paraguay":"巴拉圭","Qatar":"卡塔尔",
 "Turkey":"土耳其","Türkiye":"土耳其","Turkiye":"土耳其",
 "Scotland":"苏格兰","Australia":"澳大利亚","Curaçao":"库拉索","Curacao":"库拉索","Ivory Coast":"科特迪瓦",
 "Tunisia":"突尼斯","Saudi Arabia":"沙特阿拉伯","Iraq":"伊拉克","Egypt":"埃及","Senegal":"塞内加尔","Iran":"伊朗",
 "Austria":"奥地利","Jordan":"约旦","Portugal":"葡萄牙","DR Congo":"刚果(金)","Congo DR":"刚果(金)",
 "Croatia":"克罗地亚","Ghana":"加纳","Colombia":"哥伦比亚","Uzbekistan":"乌兹别克斯坦","Cape Verde":"佛得角",
 "Cabo Verde":"佛得角","Algeria":"阿尔及利亚","South Africa":"南非","Haiti":"海地","Ecuador":"厄瓜多尔",
 "Panama":"巴拿马"}

TEAM_CC={"Algeria":"ALG","Argentina":"ARG","Australia":"AUS","Austria":"AUT","Belgium":"BEL","Brazil":"BRA",
 "Canada":"CAN","Cape Verde":"CPV","Cabo Verde":"CPV","Colombia":"COL","Croatia":"CRO","Curaçao":"CUW",
 "Curacao":"CUW","Czech Republic":"CZE","Czechia":"CZE","DR Congo":"COD","Ecuador":"ECU","Egypt":"EGY",
 "England":"ENG","France":"FRA","Germany":"GER","Ghana":"GHA","Haiti":"HAI","Iran":"IRN","Iraq":"IRQ",
 "Ivory Coast":"CIV","Japan":"JPN","Jordan":"JOR","Mexico":"MEX","Morocco":"MAR","Netherlands":"NED",
 "New Zealand":"NZL","Norway":"NOR","Panama":"PAN","Paraguay":"PAR","Portugal":"POR","Qatar":"QAT",
 "Saudi Arabia":"KSA","Scotland":"SCO","Senegal":"SEN","South Africa":"RSA","South Korea":"KOR",
 "Korea Republic":"KOR","Spain":"ESP","Sweden":"SWE","Switzerland":"SUI","Tunisia":"TUN","USA":"USA",
 "United States":"USA","Uruguay":"URU","Uzbekistan":"UZB"}
def sa(s): return ''.join(c for c in unicodedata.normalize('NFD',s) if unicodedata.category(c)!='Mn')
def load(f,d):
    try: return json.load(open(f,encoding="utf-8"))
    except Exception: return d

STOP={"junior","jr","de","da","do","dos","al","el","van","von","der","den","bin","ibn"}
def toks(n):
    n=sa(n).lower().replace("-"," ").replace("'"," ")
    return [t for t in n.split() if len(t)>=3 and t not in STOP]
def cnorm(c):
    return re.sub(r'\b(fc|cf|sc|afc|cd|sk|fk|ac|as|ssc|club|de|the)\b','',sa(c or "").lower()).replace(" ","")

def main():
    try:
        wc=json.load(urllib.request.urlopen(SRC,timeout=30))
    except Exception as e:
        sys.exit(f"ERROR 下载失败: {e}")

    players=load(PLAYERS_F,[])
    if not players: sys.exit("ERROR: players.json 缺失或为空")
    clubs_list=load(CLUBS_F,[])
    if not clubs_list: sys.exit("ERROR: clubs.json 缺失或为空")
    club_by_id={c["id"]:c for c in clubs_list}
    nations_list=load(NATIONS_F,[])
    nat_by_zh={n["zh"]:n for n in nations_list}
    smap=load(SMAP_F,{})                       # 进球者名 -> 球员id（固定映射）
    smap_ci={sa(k).lower():v for k,v in smap.items()}   # 大小写/音标无关查找
    by_id={p["id"]:p for p in players}
    by_nat={}
    for i,p in enumerate(players): by_nat.setdefault(p["nationZh"],[]).append(i)
    # 国家英文名 -> 中文名：直接从 players.json 动态构建（权威），NATION_ZH 仅作补充。
    NAT_EN2ZH=dict(NATION_ZH)
    for p in players: NAT_EN2ZH.setdefault(p["nation"], p["nationZh"])

    def nat_zh(team): return NAT_EN2ZH.get(team, NATION_ZH.get(team, team))

    def expand(p, goals, pens=0):
        """把球员档案 JOIN clubs.json，展开成 data.json 用的完整记录。pens=其中的点球数。"""
        c=club_by_id.get(p.get("club_id"), {})
        return {"player":p["name"],"nameZh":p.get("nameZh",""),"num":p["num"],
            "pos":p["pos"],"posZh":p["posZh"],"nation":p["nation"],"nationZh":p["nationZh"],
            "goals":goals,"pens":pens,
            "club":c.get("name","—"),"clubZh":c.get("nameZh",""),"league":c.get("league","—"),
            "club_id":p.get("club_id",""),"id":p["id"]}

    def fuzzy_id(name, team):
        """map 里没有的新进球者：在该国队内按名字相似度自动匹配球员id。
        策略：算每名同国球员的相似度，取最高分；只要最高分明显领先第二名
        （唯一性强，不会误配同名），就自动采用。能自动解决绝大多数新进球者。"""
        nz=nat_zh(team); st=set(toks(name))
        if not st: return None
        ssur=toks(name)[-1]; sgiven=toks(name)[0]
        ranked=[]
        for pi in by_nat.get(nz,[]):
            p=players[pi]; ptk=toks(p["name"]); pt=set(ptk)
            if not pt: continue
            ov=len(st&pt)
            if ov==0: continue
            psur=ptk[-1]; pgiven=ptk[0]
            # 相似度：token重叠为主，姓一致/名一致加权
            score=ov*10 + (15 if ssur==psur else 0) + (6 if sgiven==pgiven else 0)
            # 覆盖率：进球者名的 token 有多少被该球员覆盖（Baena 的姓没解析全时，名覆盖也算）
            cover=ov/len(st)
            score += int(cover*8)
            ranked.append((score,p["id"]))
        if not ranked: return None
        ranked.sort(reverse=True)
        top=ranked[0]
        second=ranked[1][0] if len(ranked)>1 else 0
        # 自动采用条件：最高分>=12 且 明显领先第二名(>=8分差，即唯一性强)
        if top[0]>=12 and (top[0]-second)>=8:
            return top[1]
        # 次强：最高分很高(姓一致+重叠)即使有并列也采用
        if top[0]>=25:
            return top[1]
        return None

    prev=load(DATA_F,{})
    prev_goals={s["player"]:s["goals"] for s in prev.get("scorers",[])}

    # 抓进球，按 球员id 累加
    goals_by_id={}; pens_by_id={}; matches_with_goals=0; unresolved=set()
    for mt in wc.get("matches",[]):
        if not mt.get("score",{}).get("ft"): continue
        had=False
        for side,team in (("goals1",mt.get("team1")),("goals2",mt.get("team2"))):
            for g in mt.get(side,[]):
                if g.get("owngoal") or not g.get("name"): continue
                had=True
                nm=ALIASES.get(g["name"],g["name"])
                pid=smap.get(g["name"]) or smap.get(nm) or smap_ci.get(sa(g["name"]).lower()) or smap_ci.get(sa(nm).lower()) or fuzzy_id(nm,team)
                if not pid:
                    unresolved.add(g["name"]); continue
                goals_by_id[pid]=goals_by_id.get(pid,0)+1
                if g.get("penalty"): pens_by_id[pid]=pens_by_id.get(pid,0)+1
        if had: matches_with_goals+=1

    # 组装 scorers（有进球的球员完整档案）与 roster（全员）—— 用 expand() JOIN clubs.json
    scorers=[]
    for pid,g in goals_by_id.items():
        p=by_id.get(pid)
        if not p: continue
        scorers.append(expand(p,g,pens_by_id.get(pid,0)))
    scorers.sort(key=lambda x:(-x["goals"],x["player"]))

    roster=[expand(p, goals_by_id.get(p["id"],0), pens_by_id.get(p["id"],0)) for p in players]
    roster.sort(key=lambda x:(-x["goals"], x["player"]))

    out={"version":read_version(),
         "updated":datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
         "source":"openfootball/worldcup.json + FIFA squad lists (id-based), auto-generated",
         "count":len(scorers),"totalGoals":sum(s["goals"] for s in scorers),
         "totalPens":sum(s["pens"] for s in scorers),
         "matchesWithGoals":matches_with_goals,"scorers":scorers,
         "rosterCount":len(roster),"roster":roster}
    json.dump(out,open(DATA_F,"w",encoding="utf-8"),ensure_ascii=False,indent=1)

    # 日志
    new_scorers=[s for s in scorers if s["player"] not in prev_goals]
    up=[(s["player"],s["goals"]-prev_goals[s["player"]]) for s in scorers
        if s["player"] in prev_goals and s["goals"]>prev_goals[s["player"]]]
    added=sum(n for _,n in up)+sum(s["goals"] for s in new_scorers)
    print(f"[{out['version']}] OK: {len(scorers)} scorers, {out['totalGoals']} goals, {matches_with_goals} matches with goals.")
    if unresolved:
        print(f"WARNING: {len(unresolved)} unresolved scorer name(s) -> add to scorer_map.json: {sorted(unresolved)}")
    if prev_goals:
        if new_scorers or up:
            print(f"This run added {added} goal(s):")
            for s in new_scorers:
                print(f"  + New scorer {s['player']} ({s['nation']}) {s['goals']} goal{'s' if s['goals']!=1 else ''}")
            for name,n in up:
                print(f"  + {n} more goal{'s' if n!=1 else ''}: {name}")
        else:
            print("No new goals this run.")

if __name__=="__main__": main()
