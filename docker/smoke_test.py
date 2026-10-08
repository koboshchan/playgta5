"""HTTP checks against a running container with synthetic mirror fixtures."""
import gzip
import json
import sys
from urllib.error import HTTPError
from urllib.request import Request, urlopen

base = sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:8000'

def check(path, expected=200, data=None, headers=None):
    request = Request(base + path, data=data, headers=headers or {})
    try:
        response = urlopen(request, timeout=10)
    except HTTPError as error:
        response = error
    with response:
        assert response.status == expected, (path, response.status, expected)
        h = response.headers
        assert h['Cross-Origin-Opener-Policy'] == 'same-origin'
        assert h['Cross-Origin-Embedder-Policy'] == 'require-corp'
        assert h['Cross-Origin-Resource-Policy'] == 'same-origin'
        assert h['Accept-Ranges'] == 'bytes'
        return h, response.read()

assert b'const BASE' in check('/')[1]
assert check('/b/8b0b5899ed/loader.js')[0].get_content_type() == 'text/javascript'
assert check('/data/manifest.json')[0].get_content_type() == 'application/json'
h, body = check('/b/8b0b5899ed/game.wasm')
assert h.get_content_type() == 'application/wasm' and body == b'\0asm\1\0\0\0'
for value, expected in [('bytes=2-5', b'2345'), ('bytes=-3', b'789'), ('bytes=7-', b'789')]:
    h, body = check('/data/smoke.bin', 206, headers={'Range': value})
    assert body == expected and h['Content-Range'].endswith('/10')
check('/data/smoke.bin', 416, headers={'Range': 'bytes=20-30'})
check('/missing', 404)
check('/%2e%2e/serve_local.py', 404)
for suffix in ('', '?gz=1'):
    h, body = check('/data/batch' + suffix, data=json.dumps([['smoke.bin', 1, 3], ['smoke.bin', 8, 20]]).encode(), headers={'Content-Type': 'application/json'})
    if suffix:
        assert h['Content-Encoding'] == 'gzip'
        body = gzip.decompress(body)
    assert body == b'12389' and h['X-Run-Lengths'] == '3,2'
check('/data/batch', 400, data=b'[["../secret",0,1]]')
check('/data/batch', 400, data=b'[["smoke.bin",null,1]]')
print('PASS: index, client routes, isolation, MIME, ranges, batch/gzip, traversal checks')
