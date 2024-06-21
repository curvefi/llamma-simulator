#!/usr/bin/env python3

import datetime
import requests
import json
import time

pair = 'USDEUSDC'
pool = "0x02950460E2b9529D0E00284A5fA2d7bDF3fA4d72"
base_token = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
collateral_token = "0x4c9EDD5852cd905f086C759E8383e09bff1E68B3"
begin = datetime.datetime(year=2023, month=12, day=17)

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
