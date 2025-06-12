#!/usr/bin/env python3

import datetime
import requests
import json
import time

virtual_price = 'VP'
lp_crv = 'LP-CRV'
cvxcrv_crv = 'CVXCRV-CRV'
crv_crvusd = 'CRV-CRVUSD'
lp_crvusd = 'LP-CRVUSD'
lp_crvusd_calc = 'LP-CRVUSD-CALC'
cvxcrv_crvusd = 'CVXCRV-CRVUSD'

CVXCRVPOOL = "0x971add32Ea87f10bD192671630be3BE8A11b8623"
TRICRV = "0x4eBdF703948ddCEA3B11f675B4D1Fba9d2414A14"
CRV = "0xD533a949740bb3306d119CC777fa900bA034cd52"
CVXCRV = "0x62B9c7356A2Dc64a1969e19C23e4f579F9810Aa7"
CRVUSD = "0xf939E0A03FB07F59A73314E73794Be0E57ac1b4E"

VP_URI_TEMPLATE = f'https://prices.curve.finance/v1/snapshots/ethereum/{CVXCRVPOOL}' + '?start={start}&end={end}'
LP_URI_TEMPLATE = f'https://prices.curve.finance/v1/lp_ohlc/ethereum/{CVXCRVPOOL}?&agg_number=1&agg_units=minute&price_units=token0' + '&start={start}&end={end}'
CVXCRV_URI_TEMPLATE = f'https://prices.curve.finance/v1/ohlc/ethereum/{CVXCRVPOOL}?main_token={CRV}&reference_token={CVXCRV}&agg_number=1&agg_units=minute' + '&start={start}&end={end}'
CRV_CRVUSD_URI_TEMPLATE = f'https://prices.curve.finance/v1/ohlc/ethereum/{TRICRV}?main_token={CRVUSD}&reference_token={CRV}&agg_number=1&agg_units=minute' + '&start={start}&end={end}'

CHUNKS_IN_DAY = 5

vp_data = []
lp_crv_data = []
cvxcrv_crv_data = []
crv_crvusd_data = []
lp_crvusd_data = []
lp_crvusd_calc_data = []
cvxcrv_crvusd_data = []

s = requests.session()
start = datetime.datetime(year=2023, month=8, day=1)
end = datetime.datetime.utcnow()
dt = (end - start)
prev_vp = 0
for i in range(0, dt.days * CHUNKS_IN_DAY):
    d = int((start + datetime.timedelta(days=1) * i / CHUNKS_IN_DAY).timestamp())
    uri_vp = VP_URI_TEMPLATE.format(start=d, end=d + 86400 // CHUNKS_IN_DAY - 1)
    uri_lp = LP_URI_TEMPLATE.format(start=d, end=d + 86400 // CHUNKS_IN_DAY - 1)
    uri_cvxcrv = CVXCRV_URI_TEMPLATE.format(start=d, end=d + 86400 // CHUNKS_IN_DAY - 1)
    uri_crv_crvusd = CRV_CRVUSD_URI_TEMPLATE.format(start=d, end=d + 86400 // CHUNKS_IN_DAY - 1)
    while True:
        try:
            time.sleep(0.1)
            resp_vp = requests.get(uri_vp, timeout=10).json()
            resp_lp = requests.get(uri_lp, timeout=10).json()
            resp_cvxcrv = requests.get(uri_cvxcrv, timeout=10).json()
            resp_crv_crvusd = requests.get(uri_crv_crvusd, timeout=10).json()
            break
        except Exception as e:
            print(e)
            time.sleep(30)
    print(datetime.datetime.fromtimestamp(d))
    print(virtual_price, len(resp_vp['data']))
    print(lp_crv, len(resp_lp['data']))
    print(cvxcrv_crv, len(resp_cvxcrv['data']))
    print(crv_crvusd, len(resp_crv_crvusd['data']))
    if len(resp_lp['data']) == len(resp_cvxcrv['data']) == len(resp_crv_crvusd['data']):
        _vp = prev_vp
        if len(resp_vp["data"]) > 0:
            _vp = resp_vp["data"][0]["virtual_price"]
            prev_vp = _vp
        vp_data += [[rp['time'] * 1000, _vp / 10**18] for rp in resp_lp['data']]
        lp_crv_data += [[rp['time'] * 1000, rp['open'], rp['high'], rp['low'], rp['close'], 1000000] for rp in resp_lp['data']]
        cvxcrv_crv_data += [[rp['time'] * 1000, rp['open'], rp['high'], rp['low'], rp['close'], 1000000] for rp in resp_cvxcrv['data']]

        crv_crvusd_data += [[rp['time'] * 1000, rp['open'], rp['high'], rp['low'], rp['close'], 1000000] for rp in resp_crv_crvusd['data']]

        lp_crvusd_data += [[rp['time'] * 1000, rp['open'] * rs['open'], rp['high'] * rs['high'], rp['low'] * rs['low'], rp['close'] * rs['close'], 1000000]
                 for rp, rs in zip(resp_lp['data'], resp_crv_crvusd['data'])]
        lp_crvusd_calc_data += [[cvxcrv_crv_data[-1][0]] + \
                                    [(_cvxcrv if _cvxcrv < 1 else 1 / _cvxcrv) * _crv * vp_data[-1][1] for _cvxcrv, _crv in
                                     zip(cvxcrv_crv_data[-1][1:-1], crv_crvusd_data[-1][1:-1])] +
                                [1000000]]
        cvxcrv_crvusd_data += [[rp['time'] * 1000, rp['open'] * rs['open'], rp['high'] * rs['high'], rp['low'] * rs['low'], rp['close'] * rs['close'], 1000000]
                 for rp, rs in zip(resp_cvxcrv['data'], resp_crv_crvusd['data'])]


with open(virtual_price.lower() + '.json', 'w') as f:
    json.dump(vp_data, f)
with open(lp_crv.lower() + '.json', 'w') as f:
    json.dump(lp_crv_data, f)
with open(cvxcrv_crv.lower() + '.json', 'w') as f:
    json.dump(cvxcrv_crv_data, f)

with open(crv_crvusd.lower() + '.json', 'w') as f:
    json.dump(crv_crvusd_data, f)

with open(lp_crvusd.lower() + '.json', 'w') as f:
    json.dump(lp_crvusd_data, f)
with open(lp_crvusd_calc.lower() + '.json', 'w') as f:
    json.dump(lp_crvusd_calc_data, f)
with open(cvxcrv_crvusd.lower() + '.json', 'w') as f:
    json.dump(cvxcrv_crvusd_data, f)
