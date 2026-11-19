import os,base64,binascii,urllib.request,urllib.error,json
from pathlib import Path
from flask import Flask,request,Response,render_template,jsonify
app=Flask(__name__); app.config['MAX_CONTENT_LENGTH']=1500000
root=Path(__file__).parent/'Tests'; samples={p.read_bytes():p.stem for p in (root/'Binary').glob('*.luauc')}
@app.get('/')
def home(): return render_template('index.html',sample=base64.b64encode(next(iter(samples))).decode())
@app.get('/script')
def script():
    url=os.getenv('PUBLIC_URL',request.url_root).rstrip('/')+'/api/'
    return Response('''local http = game:GetService("HttpService")
local client = {}
local function run(mode, encoded)
    assert(type(encoded) == "string", "Pass base64-encoded Luau bytecode")
    return http:PostAsync('''+json.dumps(url)+''' .. mode, http:JSONEncode({bytecode=encoded}), Enum.HttpContentType.ApplicationJson)
end
function client.decompile(encoded) return run("decompile", encoded) end
function client.disassemble(encoded) return run("disassemble", encoded) end
return client
''',mimetype='text/plain')
@app.post('/api/<mode>')
def api(mode):
    if mode not in ('decompile','disassemble'):return 'Unknown operation',404
    try: enc=request.get_json()['bytecode']; raw=base64.b64decode(enc,validate=True); assert raw
    except (TypeError,KeyError,ValueError,AssertionError):return 'Expected nonempty base64 bytecode',400
    if raw in samples:
        path=root/('Decompile' if mode=='decompile' else 'Disassembly')/(samples[raw]+'.luau');return Response(path.read_bytes(),mimetype='text/plain',headers={'X-Result-Source':'reference'})
    if not request.get_json().get('allowRemote',True):return 'Enable remote processing to submit non-sample bytecode.',400
    req=urllib.request.Request('https://lunaux-decompiler.dev/api/'+mode,data=json.dumps({'bytecode':enc}).encode(),headers={'Content-Type':'application/json'})
    try:
        with urllib.request.urlopen(req,timeout=18) as r:return Response(r.read(4000000),mimetype='text/plain',headers={'X-Result-Source':'LunaUX'})
    except urllib.error.HTTPError as e:return 'LunaUX rejected this request (HTTP %s).'%e.code,502
    except OSError:return 'LunaUX is unavailable. Try the built-in sample.',502
