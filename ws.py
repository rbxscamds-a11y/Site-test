import websocket, ssl

def on_message(ws, msg): print('MSG:', msg[:300])

def on_error(ws, err): print('ERR:', err)

def on_open(ws): print('CONNECTED')

ws = websocket.WebSocketApp('wss://cs2skin.com/api/ws/universal',
    header=['Cookie: cs2skin_auth=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHBpcmVzIjoxNzg5MTAxNDMyLjYzMTVhODQ5Y5NiwidXNlcklkSjo2MzI3N30.CP6xJpILOIHhRRgTtx3hu4qxqrl_a-J5mXE8WNDGo38', 'Origin: https://cs2skin.com'],
    on_message=on_message, on_error=on_error, on_open=on_open)
ws.run_forever(sslopt={'cert_reqs': ssl.CERT_NONE})
