#!/usr/bin/env python3

import datetime
import requests
import json
import time

pair1 = 'YCRVCRV'
pair2 = 'CRVCRVUSD'
pair = 'YCRVCRVUSD'

YCRV_URI_TEMPLATE = 'https://prices.curve.fi/v1/ohlc/ethereum/0x99f5aCc8EC2Da2BC0771c32814EFF52b712de1E5?main_token=0xD533a949740bb3306d119CC777fa900bA034cd52&reference_token=0xFCc5c47bE19d06BF83eB04298b026F81069ff65b&agg_number=1&agg_units=minute&start={start}&end={end}'
CRV_URI_TEMPLATE = 'https://prices.curve.fi/v1/ohlc/ethereum/0x4eBdF703948ddCEA3B11f675B4D1Fba9d2414A14?main_token=0xf939E0A03FB07F59A73314E73794Be0E57ac1b4E&reference_token=0xD533a949740bb3306d119CC777fa900bA034cd52&agg_number=1&agg_units=minute&start={start}&end={end}'
CHUNKS_IN_DAY = 5
data1 = []
data2 = []
data = []

s = requests.session()
begin = datetime.datetime(year=2023, month=8, day=1)
start = datetime.datetime.utcnow()
dt = (start - begin)
for i in range(-dt.days * CHUNKS_IN_DAY, 0):
    d = int((start + datetime.timedelta(days=1) * i / CHUNKS_IN_DAY).timestamp())
    uri_ycrv = YCRV_URI_TEMPLATE.format(start=d, end=d + 86400 // CHUNKS_IN_DAY - 1)
    uri_crv = CRV_URI_TEMPLATE.format(start=d, end=d + 86400 // CHUNKS_IN_DAY - 1)
    while True:
        try:
            time.sleep(0.1)
            resp_ycrv = s.get(uri_ycrv, timeout=10).json()
            resp_crv = s.get(uri_crv, timeout=10).json()
            break
        except Exception as e:
            print(e)
            time.sleep(30)
    print(pair1, pair2, datetime.datetime.fromtimestamp(d), len(resp_ycrv['data']), len(resp_crv['data']))
    if len(resp_ycrv['data']) == len(resp_crv['data']):
        data1 += [[rp['time'] * 1000, rp['open'], rp['high'], rp['low'], rp['close'], 1000000]
                  for rp in resp_ycrv['data']]
        data2 += [[rs['time'] * 1000, rs['open'], rs['high'], rs['low'], rs['close'], 1000000]
                  for rs in resp_crv['data']]
        data += [[rp['time'] * 1000, rp['open'] * rs['open'], rp['high'] * rs['high'], rp['low'] * rs['low'], rp['close'] * rs['close'], 1000000]
                 for rp, rs in zip(resp_ycrv['data'], resp_crv['data'])]

with open(pair1.lower() + '.json', 'w') as f:
    json.dump(data1, f)
with open(pair2.lower() + '.json', 'w') as f:
    json.dump(data2, f)
with open(pair.lower() + '.json', 'w') as f:
    json.dump(data, f)
