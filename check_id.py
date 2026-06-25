import os, json, urllib.request, urllib.parse
KEY = os.environ["APISPORTS_KEY"]
def api(path, **p):
    url = "https://v3.football.api-sports.io"+path+"?"+urllib.parse.urlencode(p)
    req = urllib.request.Request(url, headers={"x-apisports-key": KEY})
    return json.load(urllib.request.urlopen(req))

for season in ("2026", "2022"):
    r = api("/fixtures", league="1", season=season)
    fx = r.get("response", [])
    print(f"season={season}: errors={r.get('errors')} results={r.get('results')} fixtures={len(fx)}")
    for f in fx[:5]:
        print("   ", f["fixture"]["date"], "|", f["fixture"]["status"]["short"],
              "|", f["teams"]["home"]["name"], "vs", f["teams"]["away"]["name"])
