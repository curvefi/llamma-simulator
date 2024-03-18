#!/usr/bin/env python3

import datetime
import requests
import json
import time

pair = 'FXNCRVUSD'

FXN_URI_TEMPLATE = 'https://prices.curve.fi/v1/ohlc/ethereum/0xC15F285679a1Ef2d25F53D4CbD0265E1D02F2A92?main_token=0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2&reference_token=0x365AccFCa291e7D3914637ABf1F7635dB165Bb09&agg_number=1&agg_units=minute&start={start}&end={end}'
ETH_URI_TEMPLATE = 'https://prices.curve.fi/v1/ohlc/ethereum/0x4eBdF703948ddCEA3B11f675B4D1Fba9d2414A14?main_token=0xf939E0A03FB07F59A73314E73794Be0E57ac1b4E&reference_token=0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2&agg_number=1&agg_units=minute&start={start}&end={end}'
CHUNKS_IN_DAY = 5
data = []

s = requests.session()
begin = datetime.datetime(year=2023, month=10, day=1)
start = datetime.datetime.utcnow()
dt = (start - begin)
for i in range(-dt.days * CHUNKS_IN_DAY, 0):
    d = int((start + datetime.timedelta(days=1) * i / CHUNKS_IN_DAY).timestamp())
    uri_fxn = FXN_URI_TEMPLATE.format(start=d, end=d + 86400 // CHUNKS_IN_DAY - 1)
    uri_eth = ETH_URI_TEMPLATE.format(start=d, end=d + 86400 // CHUNKS_IN_DAY - 1)
    while True:
        try:
            time.sleep(0.1)
            resp_fxn = s.get(uri_fxn).json()
            resp_eth = s.get(uri_eth).json()
            break
        except Exception as e:
            print(e)
            time.sleep(30)
    print(pair, datetime.datetime.fromtimestamp(d), len(resp_fxn['data']), len(resp_eth['data']))
    if len(resp_fxn['data']) == len(resp_eth['data']):
        data += [[rf['time'] * 1000, rf['open'] * re['open'], rf['high'] * re['high'], rf['low'] * re['low'], rf['close'] * re['close'], 1000000]
                 for rf, re in zip(resp_fxn['data'], resp_eth['data'])]

with open(pair.lower() + '.json', 'w') as f:
    json.dump(data, f)
