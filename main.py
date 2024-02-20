#!.venv/bin/python3
#from web.main import main,run
#main()
#run()

import asyncio
from binance import AsyncClient, BinanceSocketManager

async def main():
    client = await AsyncClient.create(api_key='<api_key>', api_secret='<api_secret>')
    bm = BinanceSocketManager(client)
    ts = bm.futures_socket()  # Vous pouvez également essayer bm.futures_user_socket()
    async with ts as tscm:
        while True:
            res = await tscm.recv()
            print(res)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())