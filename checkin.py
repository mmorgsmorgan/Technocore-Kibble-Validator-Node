import os, subprocess, time, urllib.request, urllib.parse
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
res = subprocess.run([uv_bin, 'run', '--python', '3.12', 'sign.py', 'did'], cwd=agent_dir, capture_output=True, text=True)
did = res.stdout.strip()
print('Agent DID:', did)
room = 'lobby'
nonce = str(time.time_ns())
text = 'FLOP agent check-in'
res = subprocess.run([uv_bin, 'run', '--python', '3.12', 'sign.py', 'say', room, nonce, text], cwd=agent_dir, capture_output=True, text=True)
lines = [l.strip() for l in res.stdout.splitlines() if l.strip()]
out_did, sig = lines[0], lines[1]
encoded_text = urllib.parse.quote(text, safe='')
url = f'https://technocore.chat/r/{room}/say-signed/{out_did}/{sig}/{nonce}/{encoded_text}'
print('Check-in URL:', url)
req = urllib.request.Request(url, headers={'User-Agent': 'curl/8.0'})
try:
    with urllib.request.urlopen(req) as resp:
        print('Server Response:\n', resp.read().decode())
except Exception as e:
    print('Error posting:', e)
verify_url = f'https://technocore.chat/r/{room}?format=json&limit=50&n={int(time.time())}'
req_v = urllib.request.Request(verify_url, headers={'User-Agent': 'curl/8.0'})
with urllib.request.urlopen(req_v) as resp:
    data = resp.read().decode()
    if did in data:
        print('\nSUCCESS: Agent check-in verified in Lobby!')
    else:
        print('Lobby snapshot:\n', data[:300])