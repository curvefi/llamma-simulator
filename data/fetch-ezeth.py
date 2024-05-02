#!/usr/bin/env python3

import datetime
import requests
import json
import time

pair1 = 'EZETHETH'
pair2 = 'ETHCRVUSD'
pair = 'EZETHCRVUSD'

EZETH_URI_TEMPLATE = 'https://prices.curve.fi/v1/ohlc/ethereum/0x85dE3ADd465a219EE25E04d22c39aB027cF5C12E?main_token=0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2&reference_token=0xbf5495Efe5DB9ce00f80364C8B423567e58d2110&agg_number=1&agg_units=minute&start={start}&end={end}'
ETH_URI_TEMPLATE = 'https://prices.curve.fi/v1/ohlc/ethereum/0x4eBdF703948ddCEA3B11f675B4D1Fba9d2414A14?main_token=0xf939E0A03FB07F59A73314E73794Be0E57ac1b4E&reference_token=0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2&agg_number=1&agg_units=minute&start={start}&end={end}'
CHUNKS_IN_DAY = 5
data1 = []
data2 = []
data = []

s = requests.session()
begin = datetime.datetime(year=2024, month=2, day=1)
start = datetime.datetime.utcnow()
dt = (start - begin)
for i in range(-dt.days * CHUNKS_IN_DAY, 0):
    d = int((start + datetime.timedelta(days=1) * i / CHUNKS_IN_DAY).timestamp())
    uri_pufeth = EZETH_URI_TEMPLATE.format(start=d, end=d + 86400 // CHUNKS_IN_DAY - 1)
    uri_wsteth = ETH_URI_TEMPLATE.format(start=d, end=d + 86400 // CHUNKS_IN_DAY - 1)
    while True:
        try:
            time.sleep(0.1)
            resp_pufeth = s.get(uri_pufeth, timeout=10).json()
            resp_wsteth = s.get(uri_wsteth, timeout=10).json()
            break
        except Exception as e:
            print(e)
            time.sleep(30)
    print(pair1, pair2, datetime.datetime.fromtimestamp(d), len(resp_pufeth['data']), len(resp_wsteth['data']))
    if len(resp_pufeth['data']) == len(resp_wsteth['data']):
        data1 += [[rp['time'] * 1000, rp['open'], rp['high'], rp['low'], rp['close'], 1000000]
                  for rp in resp_pufeth['data']]
        data2 += [[rs['time'] * 1000, rs['open'], rs['high'], rs['low'], rs['close'], 1000000]
                  for rs in resp_wsteth['data']]
        data += [[rp['time'] * 1000, rp['open'] * rs['open'], rp['high'] * rs['high'], rp['low'] * rs['low'], rp['close'] * rs['close'], 1000000]
                 for rp, rs in zip(resp_pufeth['data'], resp_wsteth['data'])]

with open(pair1.lower() + '.json', 'w') as f:
    json.dump(data1, f)
with open(pair2.lower() + '.json', 'w') as f:
    json.dump(data2, f)
with open(pair.lower() + '.json', 'w') as f:
    json.dump(data, f)
