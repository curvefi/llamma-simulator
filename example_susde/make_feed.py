import gzip
import json
from math import exp, log

Thalf = int(60 * 30 / log(2))  # 1/2 time is 30 min
mul = exp(-60 / Thalf)
filenames = ['susdesdai.json.gz', 'sdaifrax.json.gz']

data = []
loaded_data = [json.load(gzip.open(f)) for f in filenames]

p0 = loaded_data[0][0][1]
for i in range(len(loaded_data[0])):
    p = loaded_data[0][i][1]
    p = p * (1 - mul) + p0 * mul
    p0 = p
    for j in range(1, len(loaded_data[0][i]) - 1):
        loaded_data[0][i][j] = p

loaded_data = zip(*loaded_data)
ctrs = [0] * len(filenames)

for line in loaded_data:
    for i in range(1, len(line)):
        assert line[i][0] == line[0][0]
        out_line = line[0][:]
        for j in range(1, len(line)):
            for k in range(1, len(line[0]) - 1):
                out_line[k] *= line[j][k]
        data.append(out_line)

with open('susdefrax-1m.json', 'w') as f:
    json.dump(data, f)
