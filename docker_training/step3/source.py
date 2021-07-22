import os
import http.server as s
from urllib.parse import urlparse
from urllib.parse import parse_qs

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

import base64 
FLAG = b'kurenaifCTF{CBC_PADDING_ORACLE}'
# key = get_random_bytes(16)
key = b'\x07\xf4\xc7/\x0f\x14_\xad\x0f\xa5\xb3\x8d\x01.\xca\x9b'

class MyHandler(s.BaseHTTPRequestHandler):
    def do_GET(self):

        cipher = AES.new(key, AES.MODE_CBC)
        iv = cipher.iv
        flag_cipher = cipher.encrypt(pad(FLAG, AES.block_size))
        body = b'cipher = ' + base64.urlsafe_b64encode(flag_cipher)
        print(base64.urlsafe_b64encode(flag_cipher))

        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        if 'c' in params:
            cipher = AES.new(key, AES.MODE_CBC, iv=iv)
            req_cipher = params['c'][0].encode('utf-8')
            
            req_cipher += b'=' * (-len(req_cipher) % 4)
            m = cipher.decrypt(base64.urlsafe_b64decode(req_cipher))
            try:
                unpad(m, AES.block_size)
                body = b'ok'
            except:
                body = b'error'

        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.send_header('Content-length', len(body))
        self.end_headers()
        self.wfile.write(body)

host = '0.0.0.0'
port = 8000
httpd = s.HTTPServer((host, port), MyHandler)
httpd.serve_forever()
