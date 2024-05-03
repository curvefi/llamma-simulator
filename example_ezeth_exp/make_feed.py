import gzip
import json
from math import exp, log

Teth = int(60 * 20 / log(2))  # 1/2 time is 20 min
filenames = ['ezetheth-1m.json.gz', 'ethcrvusd-1m.json.gz']

data = []
loaded_data = [json.load(gzip.open(f)) for f in filenames]

p0 = loaded_data[0][0][1]
for i in range(len(loaded_data[0])):
    p = loaded_data[0][i][1]
    mul = exp(-60 / Teth)
    p = p * (1 - mul) + p0 * mul
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

with open('ezethcrvusd-1m.json', 'w') as f:
    json.dump(data, f)
