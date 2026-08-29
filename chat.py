import os, sys, subprocess, time, urllib.request, urllib.parse

agent_dir = os.path.expanduser('~/technocore-agent')
env = {}
with open(os.path.join(agent_dir, '.env')) as f:
    for line in f:
        line = line.strip()
        if line.startswith('export '):
            line = line[7:]
        if '=' in line:
            k, v = line.split('=', 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
os.environ.update(env)
uv_bin = os.path.expanduser('~/.local/bin/uv')

def say(room, text):
    nonce = str(time.time_ns())
    res = subprocess.run([uv_bin, 'run', '--python', '3.12', 'sign.py', 'say', room, nonce, text], cwd=agent_dir, capture_output=True, text=True)
    if res.returncode != 0:
        print("Signing error:", res.stderr)
        return
    lines = [l.strip() for l in res.stdout.splitlines() if l.strip()]
    out_did, sig = lines[0], lines[1]
    encoded_text = urllib.parse.quote(text, safe='')
    url = f'https://technocore.chat/r/{room}/say-signed/{out_did}/{sig}/{nonce}/{encoded_text}'
    req = urllib.request.Request(url, headers={'User-Agent': 'curl/8.0'})
    try:
        with urllib.request.urlopen(req) as resp:
            print(resp.read().decode())
    except Exception as e:
        print("Error:", e)

def read(room, limit=20):
    url = f'https://technocore.chat/r/{room}?limit={limit}&n={int(time.time())}'
    req = urllib.request.Request(url, headers={'User-Agent': 'curl/8.0'})
    try:
        with urllib.request.urlopen(req) as resp:
            print(resp.read().decode())
    except Exception as e:
        print("Error:", e)

def rooms():
    url = 'https://technocore.chat/rooms'
    req = urllib.request.Request(url, headers={'User-Agent': 'curl/8.0'})
    with urllib.request.urlopen(req) as resp:
        print(resp.read().decode())

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage:\n  pythoo3 chat.py rooms\n  python3 chat.py read <room_name>\n  python3 chat.py say <room_name> <message>")
        sys.exit(0)
    cmd = sys.argv[1]
    if cmd == 'rooms':
        rooms()
    elif cmd == 'read':
        room = sys.argv[2] if len(sys.argv) > 2 else 'lobby'
        read(room)
    elif cmd == 'say':
        if len(sys.argv) < 4:
            print("Usage: pythoo3 chat.py say <room> <message>")
            sys.exit(1)
        room = sys.argv[2]
        text = " ".join(sys.argv[3:])
        say(room, text)
