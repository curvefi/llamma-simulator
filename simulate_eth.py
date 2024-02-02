from numpy import logspace, log10
from libsimulate import scan_param, plot_losses


results = scan_param(
    'data/ethusdt-1m.json.gz',
    A=[int(a) for a in logspace(log10(30), log10(500), 20)],
    range_size=4,
    fee=0.006,
    Texp=600
)

plot_losses('A', results)
