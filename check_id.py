import os, json, urllib.request, urllib.parse
KEY = os.environ["APISPORTS_KEY"]
def api(path, **p):
    url = "https://v3.football.api-sports.io"+path+"?"+urllib.parse.urlencode(p)
    req = urllib.request.Request(url, headers={"x-apisports-key": KEY})
    return json.load(urllib.request.urlopen(req))
# 列出名字带 World Cup 的联赛
r = api("/leagues", search="World Cup")
for x in r.get("response", []):
    lg = x["league"]; seasons = [s["year"] for s in x.get("seasons", [])]
    print(lg["id"], "|", lg["name"], "|", lg.get("type"), "| seasons:", seasons[-6:])
