#!/usr/bin/env python3

import datetime
import requests
import json
import time

pair = 'FRAXUSDC'
pool = "0xDcEF968d416a41Cdac0ED8702fAC8128A64241A2"
base_token = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
collateral_token = "0x853d955aCEf822Db058eb8505911ED77F175b99e"
begin = datetime.datetime(year=2022, month=8, day=1)

URI_TEMPLATE = 'https://prices.curve.fi/v1/ohlc/ethereum/%s?main_token=%s&reference_token=%s&agg_number=1&agg_units=minute&start={start}&end={end}' % (pool, base_token, collateral_token)
CHUNKS_IN_DAY = 5
data = []

s = requests.session()
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
