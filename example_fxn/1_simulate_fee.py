from numpy import logspace, log10
from libsimulate import scan_param, plot_losses


if __name__ == '__main__':
    results = scan_param(
        'data/fxnusd-1m.json.gz',
        A=50,
        range_size=4,
        fee=logspace(log10(0.0005), log10(0.05), 20),
        Texp=600
    )

    plot_losses('fee', results)
