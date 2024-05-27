#!/usr/bin/env python3

import datetime
import requests
import json
import time

pair1 = 'SUSDESDAI'
pair2 = 'SDAIFRAX'
pair = 'SUSDEFRAX'

SUSDE = "0x9D39A5DE30e57443BfF2A8307A4256c8797A3497"
SDAI = "0x83F20F44975D03b1b09e64809B757c47f942BEeA"
FRAX = "0x853d955aCEf822Db058eb8505911ED77F175b99e"

SUSDE_URI_TEMPLATE = 'https://prices.curve.fi/v1/ohlc/ethereum/0x167478921b907422F8E88B43C4Af2B8BEa278d3A?main_token=%s&reference_token=%s&agg_number=1&agg_units=minute&start={start}&end={end}' % (SDAI, SUSDE)
SDAI_URI_TEMPLATE = 'https://prices.curve.fi/v1/ohlc/ethereum/0xcE6431D21E3fb1036CE9973a3312368ED96F5CE7?main_token=%s&reference_token=%s&agg_number=1&agg_units=minute&start={start}&end={end}' % (FRAX, SDAI)
CHUNKS_IN_DAY = 5
data1 = []
data2 = []
data = []

s = requests.session()
begin = datetime.datetime(year=2024, month=2, day=20)
start = datetime.datetime.utcnow()
dt = (start - begin)
for i in range(-dt.days * CHUNKS_IN_DAY, 0):
    d = int((start + datetime.timedelta(days=1) * i / CHUNKS_IN_DAY).timestamp())
    uri_susde = SUSDE_URI_TEMPLATE.format(start=d, end=d + 86400 // CHUNKS_IN_DAY - 1)
    uri_sdai = SDAI_URI_TEMPLATE.format(start=d, end=d + 86400 // CHUNKS_IN_DAY - 1)
    while True:
        try:
            time.sleep(0.1)
            resp_susde = s.get(uri_susde, timeout=10).json()
            resp_sdai = s.get(uri_sdai, timeout=10).json()
            break
        except Exception as e:
            print(e)
            time.sleep(30)
    print(pair1, pair2, datetime.datetime.fromtimestamp(d), len(resp_susde['data']), len(resp_sdai['data']))
    if len(resp_susde['data']) == len(resp_sdai['data']):
        data1 += [[rp['time'] * 1000, rp['open'], rp['high'], rp['low'], rp['close'], 1000000]
                  for rp in resp_susde['data']]
        data2 += [[rs['time'] * 1000, rs['open'], rs['high'], rs['low'], rs['close'], 1000000]
                  for rs in resp_sdai['data']]
        data += [[rp['time'] * 1000, rp['open'] * rs['open'], rp['high'] * rs['high'], rp['low'] * rs['low'], rp['close'] * rs['close'], 1000000]
                 for rp, rs in zip(resp_susde['data'], resp_sdai['data'])]

with open(pair1.lower() + '.json', 'w') as f:
    json.dump(data1, f)
with open(pair2.lower() + '.json', 'w') as f:
    json.dump(data2, f)
with open(pair.lower() + '.json', 'w') as f:
    json.dump(data, f)
