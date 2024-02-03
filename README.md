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

# Finding optimal A

Amplification (A) depends on asset volatility. Let's put the optimal fee we have found into the script
`2_simulate_A.py` and run it.

We obtain two graphs - losses and discount (sum of losses and the value of liquidity if price slowly goes down) for N = 4 bands:
![CRV/USD A optimization](/example_crv/2_A.png)

Value of A for the minimum of orange graph is the A we need to set for the market:
`A = 50`.

Let's take the value of the blue graph at `A = 50`: it is 0.11. It is the loss we MAY have in the worst case with N=4 which the position will lose if volatility is really bad.

This means, we set `liquidation_discount = 0.11`.

It's not great to be immediately liquidated once we get there, so let's add `3%` margin to it. This gives:
`loan_discount = 0.14`.

Minimum of the orange graph is 0.135..0.14. Let's add those 3% to it - this is 0.17. It means that:
`LTV_max = 1 - 0.17 = 0.83` - maximum achievable LTV for CRV.

Therefore, maximum possible leverage for CRV is `1 / (1 - 0.83) = 5.9`.

# Checking losses for different band numbers

User can adjust position losses by adjusting numbers of bands. Let's calculate losses in SL using recent prices for CRV depending on N using script `4_simulate_avg_loss_brief.py`:
![CRV/USD SL loss calculation](/example_crv/4_avg_loss.png)

Graph calculates loss user would experience when borrowing maximum possible amount and waiting for 1 day (on average). For example, on this graph, at N=50, loss is `0.07%` per day. However price could go up or down, so one could assume that when in actual soft liquidation, the loss could be `0.14%` per day on average.
