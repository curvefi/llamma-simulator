#!/usr/bin/env python3

import datetime
import time
import requests
import json

pair = 'FXSUSDT'

URI_TEMPLATE = 'https://api.binance.com/api/v1/klines?symbol=%s&interval=1m&limit=500&startTime={start}&endTime={end}' % pair
data = []

begin = datetime.datetime(year=2022, month=6, day=15)
start = datetime.datetime.utcnow()
dt = (start - begin)
for i in range(-dt.days * 5, 0):
    d = int((start + datetime.timedelta(days=1) * i / 5).timestamp()) * 1000
    uri = URI_TEMPLATE.format(start=d, end=d + 86400 * 1000 // 5 - 1)
    resp = requests.get(uri).json()
    print(pair, datetime.datetime.fromtimestamp(d // 1000), len(resp))
    data += resp
    time.sleep(0.1)

with open(pair.lower() + '.json', 'w') as f:
    json.dump(data, f)
