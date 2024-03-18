#!/usr/bin/env python3

import datetime
import requests
import json
import time

pair = 'SUSDUSDT'

URI_TEMPLATE = 'https://prices.curve.fi/v1/ohlc/ethereum/0xA5407eAE9Ba41422680e2e00537571bcC53efBfD?main_token=0xdAC17F958D2ee523a2206206994597C13D831ec7&reference_token=0x57Ab1ec28D129707052df4dF418D58a2D46d5f51&agg_number=1&agg_units=minute&start={start}&end={end}'
CHUNKS_IN_DAY = 5
data = []

s = requests.session()
begin = datetime.datetime(year=2020, month=10, day=15)
start = datetime.datetime.utcnow()
dt = (start - begin)
for i in range(-dt.days * CHUNKS_IN_DAY, 0):
    d = int((start + datetime.timedelta(days=1) * i / CHUNKS_IN_DAY).timestamp())
    uri = URI_TEMPLATE.format(start=d, end=d + 86400 // CHUNKS_IN_DAY - 1)
    while True:
        try:
            time.sleep(0.1)
            resp = s.get(uri).json()
            break
        except Exception as e:
            print(e)
            time.sleep(30)
    print(pair, datetime.datetime.fromtimestamp(d), len(resp['data']))
    data += [[r['time'] * 1000, r['open'], r['high'], r['low'], r['close'], 1000000] for r in resp['data']]

with open(pair.lower() + '.json', 'w') as f:
    json.dump(data, f)
