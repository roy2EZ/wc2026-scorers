#!/usr/bin/env python3
"""
update_data.py — 每天抓取一次世界杯进球数据，生成 data.json。

数据源：openfootball/worldcup.json（公共领域、免费、无需 key，含逐场进球者）
俱乐部来源（按优先级）：
  1) ALIASES 别名归一
  2) club_overrides.json  —— 人工核对过的覆盖表（最准）
  3) squad_db.json        —— 由 FIFA 官方26人名单解析的全员库(约1248人, 按 国家|姓 匹配)
  4) 都查不到 -> 留空 "—"
无需任何环境变量 / key。
"""
import json, sys, unicodedata, urllib.request, re
from datetime import datetime, timezone

SRC="https://raw.githubusercontent.com/openfootball/worldcup.json/master/2026/worldcup.json"
DATA_F, OVR_F, DB_F = "data.json", "club_overrides.json", "squad_db.json"

ALIASES={"Deniz Undav":"Denis Undav","Giovanni Reyna":"Gio Reyna","Maxi Araújo":"Maximiliano Araujo",
 "Leo Østigard":"Leo Ostigard","Mostafa Zico":"Mostafa Ziko","Hassan Al-Haydos":"Hassan Al Haidos",
 "Mohammad Mohebbi":"Mohamed Mohebi","Agustín Cano":"Agustin Canobbio"}

NATION_ZH={"Argentina":"阿根廷","Canada":"加拿大","USA":"美国","United States":"美国","Germany":"德国",
 "Sweden":"瑞典","New Zealand":"新西兰","Norway":"挪威","France":"法国","England":"英格兰","Switzerland":"瑞士",
 "Morocco":"摩洛哥","Brazil":"巴西","Netherlands":"荷兰","Spain":"西班牙","Uruguay":"乌拉圭","Japan":"日本",
 "Mexico":"墨西哥","Czechia":"捷克","Czech Republic":"捷克","South Korea":"韩国","Korea Republic":"韩国",
 "Bosnia & Herzegovina":"波黑","Bosnia and Herzegovina":"波黑","Paraguay":"巴拉圭","Qatar":"卡塔尔",
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

def main():
    try:
        wc=json.load(urllib.request.urlopen(SRC,timeout=30))
    except Exception as e:
        sys.exit(f"ERROR 下载失败: {e}")
    ovr=load(OVR_F,{})
    db=load(DB_F,{"by_nat_sur":{},"by_sur":{}})
    by_nat_sur=db.get("by_nat_sur",{}); by_sur=db.get("by_sur",{})
    norm_ovr={sa(k).lower():k for k in ovr}

    def from_db(name,team):
        cc=TEAM_CC.get(team); parts=name.split()
        cands=[sa(parts[-1]).lower()]
        if len(parts)>=2: cands.append(sa(" ".join(parts[-2:])).lower())
        for k in cands:
            if cc and f"{cc}|{k}" in by_nat_sur:
                r=by_nat_sur[f"{cc}|{k}"]; return r["club"],r["league"]
        for k in cands:
            if k in by_sur and len(by_sur[k])==1:
                r=by_sur[k][0]; return r["club"],r["league"]
        return "",""

    def resolve(name,team):
        std=ALIASES.get(name,name)
        if std in ovr: return std,ovr[std][0],ovr[std][1]
        hit=norm_ovr.get(sa(std).lower())
        if hit: return hit,ovr[hit][0],ovr[hit][1]
        club,lg=from_db(std,team)
        return std,club,lg

    tally={}
    for mt in wc.get("matches",[]):
        if not mt.get("score",{}).get("ft"): continue
        for side,team in (("goals1",mt.get("team1")),("goals2",mt.get("team2"))):
            for g in mt.get(side,[]):
                if g.get("owngoal") or not g.get("name"): continue
                std,club,lg=resolve(g["name"],team)
                rec=tally.setdefault(std,{"goals":0,"nation":team,"club":club,"league":lg})
                rec["goals"]+=1

    scorers=[]
    for std,rec in tally.items():
        info=ovr.get(std)
        nationZh=(info[2] if info else None) or NATION_ZH.get(rec["nation"],rec["nation"])
        scorers.append({"player":std,"nation":rec["nation"],"nationZh":nationZh,
            "goals":rec["goals"],"club":rec["club"],"league":rec["league"]})
    scorers.sort(key=lambda x:(-x["goals"],x["player"]))
    out={"updated":datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
         "source":"openfootball/worldcup.json + FIFA squad lists, auto-generated",
         "count":len(scorers),"totalGoals":sum(s["goals"] for s in scorers),"scorers":scorers}
    json.dump(out,open(DATA_F,"w",encoding="utf-8"),ensure_ascii=False,indent=1)
    miss=[s["player"] for s in scorers if not s["club"]]
    print(f"OK: {len(scorers)} scorers, {out['totalGoals']} goals. 无俱乐部 {len(miss)} 人: {miss if miss else '无'}")

if __name__=="__main__": main()
