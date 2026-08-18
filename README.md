# W1D3 afternoon: your team's server

Only what you already have: Linux commands, Python's standard library, your team
repository, one container. No `pip install`, no `curl`, no framework.

**Nothing reaches `main` except through a pull request. Nobody edits `server.py`.**

---

## Stage 1 · The scaffold — owner only

Add the three files from Discord on a branch, open a pull request, get one
approval, merge.

```
.gitignore   server.py   routes/_example.py
```

Everyone else is blocked until this lands, so do it first and tell your team.

**Evidence:** the merged pull request.

---

## Stage 2 · Your endpoint

```bash
cd ~/aidc-bootcamp/aidc-<team>-warmup
git checkout main && git pull origin main
git checkout -b <username>-route
cp routes/_example.py routes/<username>.py
```

Open your new file. Set `PATH` to `/<username>` and fill in the fields. The
leading `_` on `_example.py` is why it is not already an endpoint, so your copy
must not have one.

```bash
git add routes/<username>.py
git commit -m "add /<username> endpoint"
git push -u origin <username>-route
```

Open the pull request, get one teammate to approve, the owner merges. Your file
is yours alone, so you cannot conflict with anyone.

**Evidence:** `routes/` on `main`, with a file for every member.

---

## Stage 3 · Run it

Pull everyone's work, then serve it:

```bash
git checkout main && git pull origin main
docker run --rm -it -p 8000:8000 -e PYTHONUNBUFFERED=1 \
  -v "$PWD:/app" -w /app python:3.11-slim python server.py
```

PowerShell: `${PWD}` rather than `"$PWD"`.

Open `http://localhost:8000/` in a browser. Every teammate who merged is listed.
Click one. Then ask for a path nobody wrote and watch the terminal:

```
  "GET /najd HTTP/1.1" 200 -
  "GET /nonsense HTTP/1.1" 404 -
```

`-p 8000:8000` is the flag that matters. The server listens inside the container
and that flag publishes the port to your machine. Take it off and the server runs
perfectly while nothing can reach it. Try that.

### Prove it is a process on a Linux box

Leave the server running. Second terminal:

```bash
docker exec -it $(docker ps -q --filter ancestor=python:3.11-slim) bash
apt-get update && apt-get install -y procps iproute2
ps aux
ss -tlnp
```

One process, listening on 8000, as PID 1. That is this morning, applied.

**Evidence:** a screenshot of `/` listing your whole team, plus your `ss` output.

---

## Stage 4 · The pull

One member stops. The others merge one more change. That member then runs, **without
restarting the server**:

```bash
git checkout main && git pull origin main
```

Refresh the browser. The new endpoint is there. Nobody restarted anything and
nobody touched anyone else's machine: the code travelled through GitHub.

**Evidence:** `/` before and after, and confirmation the server kept running.

---

## If you finish early

**Find the bug.** `server.py` is forty lines and it has at least three real
weaknesses. One of them lets a single teammate take the whole team's server down,
including everyone else's endpoints. Find it, work out what happens, and say how
you would fix it.

**Read the log properly.** What status does your server return for a path nobody
wrote, and which line in the terminal proves it?

**Leave `main` clean.** `git status` should have nothing to say.

## One thing that will catch you

Your container runs as root and writes a root-owned `__pycache__` into your
repository. That is what the `.gitignore` is for. If it appears anyway:
`sudo rm -rf routes/__pycache__`.

## Hand in on Discord

Team name, repository URL, the stages you are claiming with evidence, and any
bonuses.
