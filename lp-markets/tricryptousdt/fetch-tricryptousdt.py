#!/usr/bin/env python3

import datetime
import requests
import json
import time
import numpy as np

virtual_price = 'VP'
lp_usdt = 'LP-USDT'
wbtc_usdt = 'WBTC_USDT'
weth_usdt = 'WETH_USDT'
usdt_crvusd = 'USDT_CRVUSD'
lp_crvusd = 'LP_CRVUSD'
lp_crvusd_calc = 'LP_CRVUSD_CALC'
wbtc_crvusd = 'WBTC_CRVUSD'
weth_crvusd = 'WETH_CRVUSD'

TRICRYPTOUSDT = "0xf5f5B97624542D72A9E06f04804Bf81baA15e2B4"
USDTCRVUSD = "0x390f3595bCa2Df7d23783dFd126427CCeb997BF4"
USDT = "0xdAC17F958D2ee523a2206206994597C13D831ec7"
WBTC = "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599"
WETH = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
CRVUSD = "0xf939E0A03FB07F59A73314E73794Be0E57ac1b4E"

VP_URI_TEMPLATE = f'https://prices.curve.finance/v1/snapshots/ethereum/{TRICRYPTOUSDT}' + '?start={start}&end={end}'
LP_URI_TEMPLATE = f'https://prices.curve.finance/v1/lp_ohlc/ethereum/{TRICRYPTOUSDT}?&agg_number=1&agg_units=minute&price_units=token0' + '&start={start}&end={end}'
WBTC_URI_TEMPLATE = f'https://prices.curve.finance/v1/ohlc/ethereum/{TRICRYPTOUSDT}?main_token={USDT}&reference_token={WBTC}&agg_number=1&agg_units=minute' + '&start={start}&end={end}'
WETH_URI_TEMPLATE = f'https://prices.curve.finance/v1/ohlc/ethereum/{TRICRYPTOUSDT}?main_token={USDT}&reference_token={WETH}&agg_number=1&agg_units=minute' + '&start={start}&end={end}'
USDT_CRVUSD_URI_TEMPLATE = f'https://prices.curve.finance/v1/ohlc/ethereum/{USDTCRVUSD}?main_token={CRVUSD}&reference_token={USDT}&agg_number=1&agg_units=minute' + '&start={start}&end={end}'

CHUNKS_IN_DAY = 5

vp_data = []
lp_usdt_data = []
wbtc_usdt_data = []
weth_usdt_data = []

usdt_crvusd_data = []

lp_crvusd_data = []
lp_crvusd_calc_data = []
wbtc_crvusd_data = []
weth_crvusd_data = []

s = requests.session()
start = datetime.datetime(year=2023, month=6, day=15)
end = datetime.datetime.utcnow()
dt = (end - start)
prev_vp = 0
for i in range(0, dt.days * CHUNKS_IN_DAY):
    d = int((start + datetime.timedelta(days=1) * i / CHUNKS_IN_DAY).timestamp())
    uri_vp = VP_URI_TEMPLATE.format(start=d, end=d + 86400 // CHUNKS_IN_DAY - 1)
    uri_lp = LP_URI_TEMPLATE.format(start=d, end=d + 86400 // CHUNKS_IN_DAY - 1)
    uri_wbtc = WBTC_URI_TEMPLATE.format(start=d, end=d + 86400 // CHUNKS_IN_DAY - 1)
    uri_weth = WETH_URI_TEMPLATE.format(start=d, end=d + 86400 // CHUNKS_IN_DAY - 1)
    uri_usdt_crvusd = USDT_CRVUSD_URI_TEMPLATE.format(start=d, end=d + 86400 // CHUNKS_IN_DAY - 1)
    while True:
        try:
            time.sleep(0.1)
            resp_vp = requests.get(uri_vp, timeout=10).json()
            resp_lp = requests.get(uri_lp, timeout=10).json()
            resp_wbtc = requests.get(uri_wbtc, timeout=10).json()
            resp_weth = requests.get(uri_weth, timeout=10).json()
            resp_usdt_crvusd = requests.get(uri_usdt_crvusd, timeout=10).json()
            break
        except Exception as e:
            print(e)
            time.sleep(30)
    print(datetime.datetime.fromtimestamp(d))
    print(virtual_price, len(resp_vp['data']))
    print(lp_usdt, len(resp_lp['data']))
    print(wbtc_usdt, len(resp_wbtc['data']))
    print(weth_usdt, len(resp_weth['data']))
    print(usdt_crvusd, len(resp_usdt_crvusd['data']))
    if len(resp_lp['data']) == len(resp_wbtc['data']) == len(resp_weth['data']) == len(resp_usdt_crvusd['data']):
        _vp = prev_vp
        if len(resp_vp["data"]) > 0:
            _vp = resp_vp["data"][0]["virtual_price"]
            prev_vp = _vp
        vp_data += [[rp['time'] * 1000, _vp / 10**18] for rp in resp_lp['data']]
        lp_usdt_data += [[rp['time'] * 1000, rp['open'], rp['high'], rp['low'], rp['close'], 1000000] for rp in resp_lp['data']]
        wbtc_usdt_data += [[rp['time'] * 1000, rp['open'], rp['high'], rp['low'], rp['close'], 1000000] for rp in resp_wbtc['data']]
        weth_usdt_data += [[rp['time'] * 1000, rp['open'], rp['high'], rp['low'], rp['close'], 1000000] for rp in resp_weth['data']]

        usdt_crvusd_data += [[rp['time'] * 1000, rp['open'], rp['high'], rp['low'], rp['close'], 1000000] for rp in resp_usdt_crvusd['data']]

        lp_crvusd_data += [[rp['time'] * 1000, rp['open'] * rs['open'], rp['high'] * rs['high'], rp['low'] * rs['low'], rp['close'] * rs['close'], 1000000]
                 for rp, rs in zip(resp_lp['data'], resp_usdt_crvusd['data'])]
        lp_crvusd_calc_data += [[wbtc_usdt_data[-1][0]] + \
                                    [3 * vp_data[-1][1] * np.cbrt(_wbtc * _weth) * _usdt for _wbtc, _weth, _usdt in
                                     zip(wbtc_usdt_data[-1][1:-1], weth_usdt_data[-1][1:-1], usdt_crvusd_data[-1][1:-1])] +
                                [1000000]]
        wbtc_crvusd_data += [[rp['time'] * 1000, rp['open'] * rs['open'], rp['high'] * rs['high'], rp['low'] * rs['low'], rp['close'] * rs['close'], 1000000]
                 for rp, rs in zip(resp_wbtc['data'], resp_usdt_crvusd['data'])]
        weth_crvusd_data += [[rp['time'] * 1000, rp['open'] * rs['open'], rp['high'] * rs['high'], rp['low'] * rs['low'], rp['close'] * rs['close'], 1000000]
                 for rp, rs in zip(resp_weth['data'], resp_usdt_crvusd['data'])]


with open(virtual_price.lower() + '-1m.json', 'w') as f:
    json.dump(vp_data, f)
with open(lp_usdt.lower() + '-1m.json', 'w') as f:
    json.dump(lp_usdt_data, f)
with open(wbtc_usdt.lower() + '-1m.json', 'w') as f:
    json.dump(wbtc_usdt_data, f)
with open(weth_usdt.lower() + '-1m.json', 'w') as f:
    json.dump(weth_usdt_data, f)

with open(usdt_crvusd.lower() + '-1m.json', 'w') as f:
    json.dump(usdt_crvusd_data, f)

with open(lp_crvusd.lower() + '-1m.json', 'w') as f:
    json.dump(lp_crvusd_data, f)
with open(lp_crvusd_calc.lower() + '-1m.json', 'w') as f:
    json.dump(lp_crvusd_calc_data, f)
with open(wbtc_crvusd.lower() + '-1m.json', 'w') as f:
    json.dump(wbtc_crvusd_data, f)
with open(weth_crvusd.lower() + '-1m.json', 'w') as f:
    json.dump(weth_crvusd_data, f)
