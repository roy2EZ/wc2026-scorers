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

# ---- ESPN 辅助源：补齐 openfootball 还没录入的已完赛场次（openfootball 为主）----
ESPN_BASE="https://site.api.espn.com/apis/site/v2/sports/soccer/fifa.world"
# 各源队名 → 统一归一化键（去重音去非字母 + 少量别名），保证不同源的队名能对上
_TEAMKEY_ALIAS={"unitedstates":"usa","bosniaherzegovina":"bosnia","bosniaandherzegovina":"bosnia",
                "congodr":"drcongo","drcongo":"drcongo","czechia":"czech","czechrepublic":"czech","turkiye":"turkey"}
def team_key(n):
    k=re.sub(r'[^a-z]','',sa(n or "").lower())
    return _TEAMKEY_ALIAS.get(k,k)
def _uget(u,t=25):
    req=urllib.request.Request(u,headers={"User-Agent":"Mozilla/5.0"})
    return json.load(urllib.request.urlopen(req,timeout=t))
def _espn_minute(s):
    return (s or "").replace("'","").strip()   # "45'+5'"→"45+5"，"22'"→"22"
# ESPN 官方赛事榜（含 goalsLeaders/assistsLeaders），用于助攻榜。每条 athlete/team 均为 $ref。
ESPN_LEADERS="https://sports.core.api.espn.com/v2/sports/soccer/leagues/fifa.world/seasons/2026/types/0/leaders"
def fetch_espn_assist_leaders(top=25):
    """返回 [(name, nation, assists)]，按助攻降序；非致命，失败/异常返回 []。
    只拉 athlete $ref（同时含 displayName 与 citizenship=国家），不再拉 team，省一半请求。"""
    lead=_uget(ESPN_LEADERS)
    cats={c.get("name"):c for c in lead.get("categories",[])}
    al=(cats.get("assistsLeaders") or {}).get("leaders",[]) or []
    out=[]
    for l in al[:top]:
        v=int(l.get("value") or 0)
        if v<=0: continue
        aref=(l.get("athlete") or {}).get("$ref")
        if not aref: continue
        try: a=_uget(aref)
        except Exception: continue
        nm=a.get("displayName") or a.get("fullName")
        if nm: out.append((nm, a.get("citizenship") or "", v))
    return out
def merge_espn(all_matches, today):
    """openfootball 里有日期、无 ft 且已到日期的比赛，用 ESPN 已完赛结果+进球补齐。非致命。"""
    missing=[m for m in all_matches if not (m.get("score") or {}).get("ft") and m.get("date") and m["date"]<=today]
    if not missing:
        print("ESPN: openfootball 无待补场次，跳过"); return 0
    by_date={}
    for m in missing: by_date.setdefault(m["date"],[]).append(m)
    filled=0
    for d,ms in sorted(by_date.items()):
        try: sb=_uget(f"{ESPN_BASE}/scoreboard?dates={d.replace('-','')}")
        except Exception as ex: print(f"  ESPN scoreboard {d} 失败: {ex}"); continue
        idx={}
        for e in sb.get("events",[]):
            comp=(e.get("competitions") or [{}])[0]
            names=[team_key((c.get("team") or {}).get("displayName")) for c in comp.get("competitors",[])]
            if len(names)==2: idx[frozenset(names)]=(e,comp)
        for m in ms:
            got=idx.get(frozenset((team_key(m.get("team1")),team_key(m.get("team2")))))
            if not got: continue
            e,comp=got
            if not ((e.get("status") or {}).get("type") or {}).get("completed"): continue
            scmap={team_key((c.get("team") or {}).get("displayName")): c.get("score") for c in comp.get("competitors",[])}
            try: a=int(scmap[team_key(m["team1"])]); b=int(scmap[team_key(m["team2"])])
            except Exception: continue
            try: s=_uget(f"{ESPN_BASE}/summary?event={e.get('id')}")
            except Exception as ex: print(f"  ESPN summary 失败 {m.get('team1')}-{m.get('team2')}: {ex}"); continue
            g1,g2=[],[]; pa=pb=0; k1=team_key(m["team1"]); k2=team_key(m["team2"])
            for k in s.get("keyEvents",[]):
                tt=((k.get("type") or {}).get("text") or ""); tk=team_key((k.get("team") or {}).get("displayName"))
                if k.get("shootout"):
                    if k.get("scoringPlay"):
                        if tk==k1: pa+=1
                        elif tk==k2: pb+=1
                    continue
                if not (k.get("scoringPlay") or tt in ("Goal","Own Goal")): continue
                scorer=((k.get("participants") or [{}])[0].get("athlete") or {}).get("displayName","")
                if not scorer: continue
                gd={"name":scorer,"minute":_espn_minute((k.get("clock") or {}).get("displayValue",""))}
                if tt=="Own Goal": gd["owngoal"]=True
                if "penal" in tt.lower() or k.get("penaltyKick"): gd["penalty"]=True
                (g1 if tk==k1 else g2).append(gd)
            m.setdefault("score",{})["ft"]=[a,b]
            if pa or pb: m["score"]["p"]=[pa,pb]
            m["goals1"]=g1; m["goals2"]=g2; filled+=1
            print(f"  [ESPN补齐] {m['team1']} {a}-{b} {m['team2']}  进球={[x['name'] for x in g1+g2]}")
    print(f"ESPN: 共补齐 {filled} 场")
    return filled

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
    # 国名归一到 players.json 的标准英文名（= 前端 FLAG 键），避免变体（Czech Republic 等）出白旗
    ZH2EN={}
    for p in players: ZH2EN.setdefault(p["nationZh"], p["nation"])
    def canon_nat(team): return ZH2EN.get(nat_zh(team), team)

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

    # 赛程进展：总场次 / 已踢 / 当前阶段（按"下一场未踢"的轮次判定；全部踢完=已结束）
    STAGE_ZH={"Round of 32":"32强","Round of 16":"16强","Quarter-final":"八强",
              "Semi-final":"四强","Match for third place":"季军赛","Final":"决赛"}
    STAGE_EN={"Round of 32":"Round of 32","Round of 16":"Round of 16","Quarter-final":"Quarter-finals",
              "Semi-final":"Semi-finals","Match for third place":"Third place","Final":"Final"}
    all_matches=wc.get("matches",[])
    # ESPN 辅助补齐（openfootball 为主）；整体失败则退回纯 openfootball
    try:
        merge_espn(all_matches, datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    except Exception as ex:
        print("ESPN 合并整体失败，退回纯 openfootball：", ex)
    # 按日期+时间给全部比赛编号（= 第几场）
    match_no={}
    for i,mt in enumerate(sorted(all_matches,key=lambda m:(m.get("date",""),m.get("time","")))):
        match_no[id(mt)]=i+1
    total_m=len(all_matches)
    played_m=sum(1 for m in all_matches if m.get("score",{}).get("ft"))
    # 小组赛轮次：把每个小组的比赛按日期排序，每 2 场为一轮 → 小组赛第1/2/3轮
    def is_group(m):
        r=m.get("round","")
        return bool(m.get("group")) and (not r or r.startswith("Matchday"))
    group_round={}  # id(match) -> 1/2/3
    by_group={}
    for m in all_matches:
        if is_group(m): by_group.setdefault(m.get("group"),[]).append(m)
    for ms in by_group.values():
        for i,m in enumerate(sorted(ms,key=lambda x:(x.get("date",""),x.get("time","")))):
            group_round[id(m)]=i//2+1
    def stage_of(m):
        r=m.get("round","")
        if is_group(m):
            gr=group_round.get(id(m))
            return (f"Group R{gr}" if gr else "Group Stage",
                    f"小组赛第{gr}轮" if gr else "小组赛")
        if not r or r.startswith("Matchday"): return ("Group Stage","小组赛")
        return (STAGE_EN.get(r, r), STAGE_ZH.get(r, r))
    unplayed=sorted([m for m in all_matches if not m.get("score",{}).get("ft") and m.get("date")],
                    key=lambda m:(m.get("date",""),m.get("time","")))
    if unplayed:
        st_en,st_zh=stage_of(unplayed[0]); next_date=unplayed[0].get("date","")
    else:
        st_en,st_zh=("Completed","已结束"); next_date=""
    last_date=max((m.get("date","") for m in all_matches if m.get("score",{}).get("ft")), default="")
    schedule={"total":total_m,"played":played_m,"stageEn":st_en,"stageZh":st_zh,
              "lastDate":last_date,"nextDate":next_date}

    # ---- 趣味统计：多球表演 / 进球时间分布 / 最早最晚 / 进球大战 ----
    def parse_min(s):
        m=re.match(r"(\d+)(?:\+(\d+))?", str(s or ""))
        return int(m.group(1))+(int(m.group(2)) if m.group(2) else 0) if m else None
    def clean_ground(g):
        g=re.sub(r"\s*\(.*?\)","",g or "").strip()   # 去掉括号里的具体郊区名
        return g.replace("New York/New Jersey","New York")
    def resolve(name, team):
        nm=ALIASES.get(name,name)
        return (smap.get(name) or smap.get(nm) or smap_ci.get(sa(name).lower())
                or smap_ci.get(sa(nm).lower()) or fuzzy_id(nm,team))
    # 按比赛阶段分桶（补水时间约 30'/75'）
    PHASES=["1-5","6-22","23-45","46-68","69-90","90+","ET"]
    buckets={b:0 for b in PHASES}
    minuteCounts=[0]*131   # 常规每分钟进球(含乌龙)：1-90（含正好90'）
    stoppage1=[0]*20       # 上半场补时 45+x（前端折线单独成段）
    stoppage2=[0]*20       # 下半场补时 90+x（前端折线单独成段，独立于加时）
    etCounts=[0]*141       # 加时赛 ET：base>=91（含ET补时），按累计分钟索引(91-140)，前端单独成段
    def add_minute(s):
        m=re.match(r"(\d+)(?:\+(\d+))?", str(s or ""))
        if not m: return
        base=int(m.group(1)); extra=int(m.group(2)) if m.group(2) else 0
        if base==45 and extra>0:                    # 上半场补时：单独成段
            if 1<=extra<len(stoppage1): stoppage1[extra]+=1
            return
        if base==90 and extra>0:                    # 下半场补时 90+：单独成段
            if 1<=extra<len(stoppage2): stoppage2[extra]+=1
            return
        if base>=91:                                # 加时赛(含ET补时)：单独成段
            t=base+extra
            if 91<=t<len(etCounts): etCounts[t]+=1
            return
        t=base+extra                                # 常规 1-90
        if 1<=t<=90: minuteCounts[t]+=1
    def phase_of(s):
        m=re.match(r"(\d+)(?:\+(\d+))?", str(s or ""))
        if not m: return None
        base=int(m.group(1)); extra=int(m.group(2)) if m.group(2) else 0
        if base>=91: return "ET"            # 加时（淘汰赛）
        if base==45 and extra>0: return "23-45"  # 上半场补时
        if base==90 and extra>0: return "90+"    # 终场补时绝杀
        t=base+extra
        if t<=5: return "1-5"
        if t<=22: return "6-22"
        if t<=45: return "23-45"
        if t<=68: return "46-68"
        if t<=90: return "69-90"
        return "90+"
    multi=[]; earliest=None; latest=None
    for mt in all_matches:
        ft=mt.get("score",{}).get("ft")
        if not ft: continue
        t1,t2=mt.get("team1"),mt.get("team2"); mdate=mt.get("date","")
        for side,team,oppo,persp in (("goals1",t1,t2,f"{ft[0]}-{ft[1]}"),
                                     ("goals2",t2,t1,f"{ft[1]}-{ft[0]}")):
            pc={}
            for g in mt.get(side,[]):
                ph=phase_of(g.get("minute"))
                if ph: buckets[ph]+=1          # 时间分布：含乌龙球（乌龙也是进球）
                add_minute(g.get("minute"))   # 常规分钟 / 补时（各半场补时单独统计）
                if g.get("owngoal") or not g.get("name"): continue   # 以下仅限有射手的进球
                mn=parse_min(g.get("minute"))
                pid=resolve(g["name"],team); p=by_id.get(pid) if pid else None
                en=p["name"] if p else g["name"]
                zh=(p.get("nameZh") if p else "") or g["name"]
                if mn is not None:
                    rec={"player":en,"nameZh":zh,"nation":canon_nat(team),"nationZh":nat_zh(team),
                         "oppo":canon_nat(oppo),"oppoZh":nat_zh(oppo),"score":persp,"date":mdate,
                         "min":mn,"minDisp":(str(g.get("minute"))+"'" if g.get("minute") else "")}
                    if earliest is None or mn<earliest["min"]: earliest=rec
                    if latest is None or mn>latest["min"]: latest=rec
                e=pc.setdefault(pid or en,{"n":0,"pens":0,"en":en,"zh":zh})
                e["n"]+=1
                if g.get("penalty"): e["pens"]+=1
            for e in pc.values():
                if e["n"]>=2:
                    multi.append({"n":e["n"],"pens":e["pens"],"player":e["en"],"nameZh":e["zh"],
                        "nation":canon_nat(team),"nationZh":nat_zh(team),
                        "oppo":canon_nat(oppo),"oppoZh":nat_zh(oppo),"score":persp,
                        "date":mdate,"ground":clean_ground(mt.get("ground",""))})
    multi.sort(key=lambda x:(x["n"], x["date"]), reverse=True)  # 档位降序 + 同档位最近在前
    bigm=[]
    for mt in all_matches:
        ft=mt.get("score",{}).get("ft")
        if not ft: continue
        bigm.append({"t1":canon_nat(mt.get("team1")),"t1Zh":nat_zh(mt.get("team1")),
            "t2":canon_nat(mt.get("team2")),"t2Zh":nat_zh(mt.get("team2")),
            "ft":f"{ft[0]}-{ft[1]}","total":ft[0]+ft[1],"date":mt.get("date",""),
            "ground":clean_ground(mt.get("ground","")),"num":match_no.get(id(mt),"")})
    bigm.sort(key=lambda x:(x["total"], x["date"]), reverse=True)  # 总进球降序 + 同档位最近在前
    bigm=[m for m in bigm if m["total"]>=4]   # 进球大战：保留总进球≥4（前端再按档位筛选）
    # 乌龙球：记在受益方名下，乌龙球员属于对手队（nation=对手）
    ownGoals=[]
    for mt in all_matches:
        ft=mt.get("score",{}).get("ft")
        if not ft: continue
        t1,t2=mt.get("team1"),mt.get("team2"); mdate=mt.get("date","")
        for side,benef,oppo in (("goals1",t1,t2),("goals2",t2,t1)):
            for g in mt.get(side,[]):
                if not g.get("owngoal"): continue
                nm=g.get("name") or ""
                pid=resolve(nm,oppo); p=by_id.get(pid) if pid else None
                ownGoals.append({"player":(p["name"] if p else nm),"nameZh":(p.get("nameZh") if p else "") or nm,
                    "nation":canon_nat(oppo),"nationZh":nat_zh(oppo),"benef":canon_nat(benef),"benefZh":nat_zh(benef),
                    "minute":(str(g.get("minute"))+"'" if g.get("minute") else ""),"min":parse_min(g.get("minute")) or 0,
                    "t1":canon_nat(t1),"t1Zh":nat_zh(t1),"t2":canon_nat(t2),"t2Zh":nat_zh(t2),
                    "ft":f"{ft[0]}-{ft[1]}","date":mdate,"ground":clean_ground(mt.get("ground",""))})
    ownGoals.sort(key=lambda x:(x["date"],x["min"]))
    # 进球时间流：所有有进球的比赛按场分组，最新比赛在前；组内进球按分钟正序。可一直回看至本届首球
    HOST={"Atlanta":"USA","Boston":"USA","Dallas":"USA","Houston":"USA","Kansas City":"USA","Los Angeles":"USA",
          "Miami":"USA","New York":"USA","Philadelphia":"USA","San Francisco Bay Area":"USA","Seattle":"USA",
          "Guadalajara":"Mexico","Mexico City":"Mexico","Monterrey":"Mexico","Toronto":"Canada","Vancouver":"Canada"}
    HOSTINFO={"USA":("🇺🇸","美国"),"Mexico":("🇲🇽","墨西哥"),"Canada":("🇨🇦","加拿大")}
    CITY_ZH={"Atlanta":"亚特兰大","Boston":"波士顿","Dallas":"达拉斯","Guadalajara":"瓜达拉哈拉","Houston":"休斯顿",
        "Kansas City":"堪萨斯城","Los Angeles":"洛杉矶","Mexico City":"墨西哥城","Miami":"迈阿密","Monterrey":"蒙特雷",
        "New York":"纽约","Philadelphia":"费城","San Francisco Bay Area":"旧金山湾区","Seattle":"西雅图","Toronto":"多伦多","Vancouver":"温哥华"}
    # 小组内真实轮次：每组 6 场、每轮 2 场，按(日期,编号)排序后 index//2+1 得 1/2/3
    # （不能按"不同日期"算——同一轮两场可能分在两天）
    grp_matches={}
    for mt in all_matches:
        g=mt.get("group")
        if g: grp_matches.setdefault(g,[]).append(mt)
    grp_round={}
    for g,ms in grp_matches.items():
        for idx,mt in enumerate(sorted(ms,key=lambda x:(x.get("date",""), x.get("num") or 0))):
            grp_round[(g,mt.get("date"),mt.get("team1"),mt.get("team2"))]=idx//2+1
    goalFeed=[]
    for idx,mt in enumerate(all_matches):
        ft=mt.get("score",{}).get("ft")
        if not ft: continue
        t1,t2=mt.get("team1"),mt.get("team2"); glist=[]
        for side,team,oppo in (("goals1",t1,t2),("goals2",t2,t1)):
            for g in mt.get(side,[]):
                nm=g.get("name") or ""; og=bool(g.get("owngoal"))
                who=oppo if og else team   # 乌龙球员属于对手队
                pid=resolve(nm,who); p=by_id.get(pid) if pid else None
                c=club_by_id.get(p.get("club_id")) if p else None
                glist.append({"player":(p["name"] if p else nm),"nameZh":(p.get("nameZh") if p else "") or nm,
                    "nation":canon_nat(who),"nationZh":nat_zh(who),
                    "clubZh":(c.get("nameZh") if c else "") or "","club":(c.get("name") if c else "") or "","league":(c.get("league") if c else "") or "",
                    "minute":(str(g.get("minute"))+"'" if g.get("minute") else ""),"min":parse_min(g.get("minute")) or 0,
                    "pen":bool(g.get("penalty")),"og":og})
        # 最新赛果：所有已完赛的比赛都收录（含 0-0 / 无进球场次），glist 可为空
        glist.sort(key=lambda x:x["min"])
        grd=clean_ground(mt.get("ground","")); hf,hz=HOSTINFO.get(HOST.get(grd,""),("",""))
        goalFeed.append({"date":mt.get("date",""),"num":mt.get("num") or (idx+1),
            "group":mt.get("group","") or "","round":mt.get("round","") or "",
            "mday":(grp_round.get((mt.get("group"),mt.get("date"),mt.get("team1"),mt.get("team2"))) if mt.get("group") else None),
            "t1":canon_nat(t1),"t1Zh":nat_zh(t1),"t2":canon_nat(t2),"t2Zh":nat_zh(t2),
            "ft":f"{ft[0]}-{ft[1]}","ground":grd,"cityZh":CITY_ZH.get(grd,""),"hostFlag":hf,"hostZh":hz,
            "shootout":(mt.get("score",{}).get("p") or None),"goals":glist})
    goalFeed.sort(key=lambda m:(m["date"],m["num"]), reverse=True)
    funstats={"multiGoals":multi,"timeBuckets":buckets,"minuteCounts":minuteCounts,"stoppage1":stoppage1,
              "stoppage2":stoppage2,"et":etCounts,"ownGoals":ownGoals,
              "goalFeed":goalFeed,
              "earliest":earliest,"latest":latest,"bigMatches":bigm}

    # 助攻榜：直接引用 ESPN 官方赛事 assistsLeaders（权威、无需逐场累加）；解析到球员库拿中文名/俱乐部。非致命。
    assists=[]
    try:
        unresolved_a=[]
        for nm,nation,v in fetch_espn_assist_leaders():
            pid=resolve(nm,nation); p=by_id.get(pid) if pid else None
            if p:
                rec=expand(p, goals_by_id.get(p["id"],0), pens_by_id.get(p["id"],0))
            else:
                unresolved_a.append(f"{nm}({nation})")
                rec={"player":nm,"nameZh":"","num":"","pos":"","posZh":"",
                     "nation":canon_nat(nation),"nationZh":nat_zh(nation),
                     "goals":0,"pens":0,"club":"—","clubZh":"","league":"—","club_id":"","id":""}
            rec["assists"]=v; assists.append(rec)
        assists.sort(key=lambda x:(-x["assists"], -x["goals"], x["player"]))
        print(f"助攻榜：{len(assists)} 人（ESPN assistsLeaders）"
              + (f"；未匹配到球员库: {', '.join(unresolved_a)}" if unresolved_a else "；全部已匹配"))
    except Exception as ex:
        print("助攻榜抓取失败（非致命，跳过）：", ex); assists=[]

    # 把助攻数回填进 scorers：射手榜同进球档内按“助攻多者靠前”（贴近 FIFA 金靴并列规则第2顺位）
    amap={r["id"]:r["assists"] for r in assists if r.get("id")}
    for s in scorers: s["assists"]=amap.get(s["id"],0)

    out={"version":read_version(),
         "updated":datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
         "source":"openfootball/worldcup.json + FIFA squad lists (id-based), auto-generated",
         "count":len(scorers),"totalGoals":sum(s["goals"] for s in scorers),
         "totalPens":sum(s["pens"] for s in scorers),
         "matchesWithGoals":matches_with_goals,"schedule":schedule,"funstats":funstats,"scorers":scorers,
         "assists":assists,"assistsCount":len(assists),
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
