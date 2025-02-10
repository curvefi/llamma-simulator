#!/usr/bin/env python3.11

import datetime
import time
import requests
import json

pair = 'FTMUSD'

URI_TEMPLATE = 'https://api-pub.bitfinex.com/v2/candles/trade%3A1m%3At' + pair + '/hist?start={start}&end={end}&sort=1'
data = []

begin = datetime.datetime(year=2021, month=7, day=1)
start = datetime.datetime.utcnow()
dt = (start - begin)
key = None
prev_key = None
R = {}
for i in range(-dt.days * 5, 0):
    d = int((start + datetime.timedelta(days=1) * i / 5).timestamp()) * 1000
    uri = URI_TEMPLATE.format(start=d, end=d + 86400 * 1000 // 5 - 1)
    resp = requests.get(uri).json()
    resp1 = {x[0]: x for x in resp}
    R.update(resp1)
    if not key:
        key = resp[0][0]
    for j in range(288):
        if prev_key:
            key += 60_000
        if key not in resp1:
            resp1[key] = [R[prev_key][0], R[prev_key][4], R[prev_key][4], R[prev_key][4],
                          R[prev_key][4], 0]
            R[key] = resp1[key]
        prev_key = key
    resp1 = list(sorted(resp1.values()))
    print(pair, datetime.datetime.fromtimestamp(resp1[0][0] // 1000), len(resp1))
    time.sleep(2.2)

data = list(sorted(R.values()))

with open(pair.lower() + '.json', 'w') as f:
    json.dump(data, f)
