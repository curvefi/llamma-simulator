#!/usr/bin/env python3

import datetime
import time
import cloudscraper
import json

pair = 'XETHUSD-1m'

URI_TEMPLATE = 'https://app.geckoterminal.com/api/p1/candlesticks/163016493/2127419?resolution=1&from_timestamp={start}&to_timestamp={end}&for_update=false&count_back=329&currency=usd&is_inverted=false'
data = []

scraper = cloudscraper.create_scraper()
begin = datetime.datetime(year=2023, month=9, day=28)
start = datetime.datetime.utcnow()
dt = (start - begin)
step = int(dt.total_seconds()) // 30
while True:
    start -= datetime.timedelta(seconds=step)
    uri = URI_TEMPLATE.format(start=int(start.timestamp()), end=int(start.timestamp())+step-1)
    resp = scraper.get(uri).json()['data']
    print(pair, start, len(resp))
    data += [[int(datetime.datetime.fromisoformat(x['dt'][:-1] + '+00:00').timestamp()), x['o'], x['h'], x['l'], x['c'], x['v']] for x in resp]
    time.sleep(1)
    if start < begin:
        break

data.sort(key=lambda x: x[0])
with open(pair.lower() + '.json', 'w') as f:
    json.dump(data, f)
