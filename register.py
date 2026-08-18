"""Put a TEAMMATE on the board.

You cannot register yourself. Somebody else has to do it for you, and you have to
do it for somebody else.

Run this inside your container while server.py is running.
Standard library only.
"""
import json, urllib.request, urllib.error

BOARD = "https://aidc.nadir.sh/register"

TEAMMATE = "their-github-username"   # whose endpoint you are reading
ME       = "your-github-username"    # you, doing the registering
TEAM     = "your-team"

def request(url, body=None):
    data = json.dumps(body).encode() if body else None
    headers = {"User-Agent": "aidc-student/1.0"}
    if body:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())

# 1. read your teammate's endpoint, off your own server
status, them = request(f"http://localhost:8000/{TEAMMATE}")
print("my server said", status, them)
if status != 200:
    raise SystemExit("their route is not merged yet, or your server is not running")

# 2. put them on the board
status, reply = request(BOARD, {
    "name": them.get("name", TEAMMATE),
    "team": TEAM,
    "registered_by": ME,
    "says": them.get("wants", ""),
})
print("the board said", status)
print(json.dumps(reply, indent=2))
