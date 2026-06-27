#!/usr/bin/env python3
"""validate_db.py — 数据库一致性强制校验。任何一项不过就 exit(1)，拒绝带病上线。"""
import json,sys,re,unicodedata
def sa(s): return ''.join(c for c in unicodedata.normalize('NFD',s) if unicodedata.category(c)!='Mn')
SUF={"fc","cf","sc","afc","cd","sk","fk","ac","as","ssc","jk","cfc","scc","gf","sco",
"aj","ae","af","cp","rc","ca","cs","ud","sd","ec","bk","if","aik","de","the","of",
"und","och","club","ks","oh","kv","rkc","psv","vfb","vfl","tsg","sv","fsv","spvgg"}
def cnorm(c):
    c=sa(c).lower(); c=re.sub(r"[^a-z0-9 ]"," ",c)
    return "".join(w for w in c.split() if w not in SUF and len(w)>1)

def main():
    players=json.load(open("players.json"))
    clubs=json.load(open("clubs.json"))
    nations=json.load(open("nations.json"))
    sm=json.load(open("scorer_map.json"))
    errors=[]; warnings=[]

    club_by_id={c["id"]:c for c in clubs} if isinstance(clubs,list) else clubs
    if isinstance(clubs,dict): clubs_list=list(clubs.values())
    else: clubs_list=clubs; club_by_id={c["id"]:c for c in clubs}

    # 1. club_id 唯一
    ids=[c["id"] for c in clubs_list]
    if len(ids)!=len(set(ids)): errors.append(f"club id 重复: {[x for x in ids if ids.count(x)>1]}")

    # 2. player id 唯一
    pids=[p["id"] for p in players]
    if len(pids)!=len(set(pids)): errors.append(f"player id 重复")

    # 3. 无孤儿：每个 player.club_id 必须存在
    orphans=[p["id"] for p in players if p.get("club_id") not in club_by_id]
    if orphans: errors.append(f"{len(orphans)} 名球员的 club_id 找不到对应俱乐部: {orphans[:5]}")

    # 4. 归一完整：不存在两家俱乐部归一名相同（杜绝重复俱乐部）
    norm_map={}
    for c in clubs_list:
        n=cnorm(c["name"])
        if n in norm_map: errors.append(f"俱乐部重复(归一名相同): {c['name']!r} 与 {norm_map[n]!r}")
        else: norm_map[n]=c["name"]

    # 5. 一队一名：每个 club 只有一个 name 和一个 nameZh（结构保证，检查非空 name）
    for c in clubs_list:
        if not c.get("name"): errors.append(f"俱乐部 {c['id']} 缺英文名")

    # 6. 国家完整：players 的 nationZh 必须在 nations 里
    nat_zh=set(n["zh"] for n in nations)
    bad_nat=set(p["nationZh"] for p in players if p["nationZh"] not in nat_zh)
    if bad_nat: errors.append(f"球员国家中文名不在 nations.json: {bad_nat}")

    # 7. 中文覆盖（有进球者的俱乐部/球员必须有中文）— 警告级
    id2p={p["id"]:p for p in players}
    scorer_pids=set(sm.values())
    for pid in scorer_pids:
        p=id2p.get(pid)
        if not p: warnings.append(f"scorer_map 指向不存在的球员 {pid}"); continue
        if not p.get("nameZh"): warnings.append(f"进球者无中文名: {p['name']}")
        c=club_by_id.get(p["club_id"])
        if c and not c.get("nameZh"): warnings.append(f"进球者俱乐部无中文名: {c['name']}")

    # 报告
    print("="*50)
    print(f"球员:{len(players)} 俱乐部:{len(clubs_list)} 国家:{len(nations)} 进球映射:{len(sm)}")
    if warnings:
        print(f"\n⚠️  {len(warnings)} 个警告:")
        for w in warnings[:20]: print("  -",w)
    if errors:
        print(f"\n❌ {len(errors)} 个错误（必须修复）:")
        for e in errors: print("  -",e)
        print("\n校验未通过。")
        sys.exit(1)
    print("\n✅ 所有强制校验通过。")

if __name__=="__main__": main()
