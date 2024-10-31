#!/usr/bin/env python3

import numpy as np
import gzip
import json
import pylab


with gzip.open('xauusd-1m.json.gz', 'r') as f:
    data = json.load(f)

t = np.array([x[0] for x in data])
p = np.array([x[1] for x in data])

pylab.plot(t[::1000], p[::1000])
pylab.show()
