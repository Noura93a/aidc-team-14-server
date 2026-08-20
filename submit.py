import json
import urllib.request

BOARD = "https://aidc.nadir.sh/model"

TEAM = "14"
BY = "HadeelFahad"
MODEL = "HuggingFaceTB/SmolLM2-360M-Instruct"
IMAGE = "ghcr.io/noura93a/aidc-team-14-server:latest"

headers = {"User-Agent": "aidc-student/1.0"}

# Read /generate from our own server
req = urllib.request.Request(
    "http://localhost:8000/generate",
    headers=headers
)

with urllib.request.urlopen(req) as r:
    result = json.loads(r.read())

# Submit to the board
data = {
    "team": TEAM,
    "by": BY,
    "model": MODEL,
    "image": IMAGE,
    "tokens_per_sec": result["tokens_per_sec"],
    "sample": result["sample"],
}

req = urllib.request.Request(
    BOARD,
    data=json.dumps(data).encode(),
    headers={
        "User-Agent": "aidc-student/1.0",
        "Content-Type": "application/json",
    },
)

with urllib.request.urlopen(req) as r:
    print(r.status)
    print(json.loads(r.read()))