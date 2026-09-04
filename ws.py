"""ws.py

Connects to wss://cs2skin.com/api/ws/universal using a Cookie header and prints all incoming messages.

Requires the `websockets` package: pip install websockets
"""

import asyncio
import signal
import sys
import websockets

URL = "wss://cs2skin.com/api/ws/universal"
COOKIE = "cs2skin_auth=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHBpcmVzIjoxNzg5MTAxNDMyLjYzMTVhODQ5Y5NiwidXNlcklkSjo2MzI3N30.CP6xJpILOIHhRRgTtx3hu4qxqrl_a-J5mXE8WNDGo38"

async def listen():
    """Keep a persistent connection, print every message, and reconnect on errors."""
    while True:
        try:
            extra_headers = [("Cookie", COOKIE)]
            async with websockets.connect(URL, extra_headers=extra_headers) as ws:
                print(f"Connected to {URL}")
                async for message in ws:
                    # Print raw message; you can modify to parse JSON if needed
                    print(message)
        except websockets.ConnectionClosed as e:
            print(f"Connection closed: {e}. Reconnecting in 5s...")
            await asyncio.sleep(5)
        except Exception as e:
            print(f"Error: {e}. Reconnecting in 5s...", file=sys.stderr)
            await asyncio.sleep(5)

async def shutdown(loop):
    tasks = [t for t in asyncio.all_tasks(loop) if t is not asyncio.current_task()]
    for t in tasks:
        t.cancel()
    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()

def main():
    loop = asyncio.get_event_loop()
    try:
        # Install signal handlers to allow clean shutdown on Ctrl+C
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, lambda: asyncio.ensure_future(shutdown(loop)))
    except NotImplementedError:
        # add_signal_handler may not be implemented on some platforms (e.g., Windows with ProactorEventLoop)
        pass

    try:
        loop.run_until_complete(listen())
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
