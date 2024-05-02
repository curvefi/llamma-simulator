#!/usr/bin/env python3

import datetime
import requests
import json
import time

pair1 = 'PUFETHWSTETH'
pair2 = 'WSTETHCRVUSD'
pair = 'PUFETHCRVUSD'

PUFETH_URI_TEMPLATE = 'https://prices.curve.fi/v1/ohlc/ethereum/0xEEda34A377dD0ca676b9511EE1324974fA8d980D?main_token=0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0&reference_token=0xD9A442856C234a39a81a089C06451EBAa4306a72&agg_number=1&agg_units=minute&start={start}&end={end}'
WSTETH_URI_TEMPLATE = 'https://prices.curve.fi/v1/ohlc/ethereum/0x2889302a794dA87fBF1D6Db415C1492194663D13?main_token=0xf939E0A03FB07F59A73314E73794Be0E57ac1b4E&reference_token=0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0&agg_number=1&agg_units=minute&start={start}&end={end}'
CHUNKS_IN_DAY = 5
data1 = []
data2 = []
data = []

s = requests.session()
begin = datetime.datetime(year=2024, month=3, day=23)
start = datetime.datetime.utcnow()
dt = (start - begin)
for i in range(-dt.days * CHUNKS_IN_DAY, 0):
    d = int((start + datetime.timedelta(days=1) * i / CHUNKS_IN_DAY).timestamp())
    uri_pufeth = PUFETH_URI_TEMPLATE.format(start=d, end=d + 86400 // CHUNKS_IN_DAY - 1)
    uri_wsteth = WSTETH_URI_TEMPLATE.format(start=d, end=d + 86400 // CHUNKS_IN_DAY - 1)
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
