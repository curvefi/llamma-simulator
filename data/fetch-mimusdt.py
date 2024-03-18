#!/usr/bin/env python3

import datetime
import requests
import json
import time

pair = 'MIMUSDT'

URI_TEMPLATE = 'https://prices.curve.fi/v1/ohlc/ethereum/0x5a6A4D54456819380173272A5E8E9B9904BdF41B?main_token=0xdAC17F958D2ee523a2206206994597C13D831ec7&reference_token=0x99D8a9C45b2ecA8864373A26D1459e3Dff1e17F3&agg_number=1&agg_units=minute&start={start}&end={end}'
CHUNKS_IN_DAY = 5
data = []

s = requests.session()
begin = datetime.datetime(year=2021, month=11, day=1)
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
