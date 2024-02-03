# Example of using the simulator to find optimal parameters

## Installation

To make simulator work, one needs just Python, NumPy and Matplotlib installed

## Downloading data

Use scripts located in `data/fetch-*.py` to download price data from Binance. For example, to download
CRV/USDT price data:

```
cd data
python3 fetch-crvusd.py
mv crvusdt.json crvusdt-1m.json  # Format we used in scripts, change to any naming you wish
gzip crvusdt-1m.json
```

All price data files are assumed to be stored gzipped.

## Finding optimal fee

Algorithm is pretty insensitive to AMM fees, however optimal value for almost all coins seems to be within 0.6%-0.9% with the exception of EUR (in examples).

Let's look at fee calculation in `example_crv`.

```
python3 1_simulate_fee.py
```
This script calculates losses depending on the AMM fee for a 4-band position with A=50 (you can change that).

This gives this graph:
![CRV/USD fee optimization](/example_crv/1_fee.png)

The graph suggests that optimal fee is at the minimum of the graph and is equal to 0.9%.
