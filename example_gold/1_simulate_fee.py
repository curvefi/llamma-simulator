from numpy import logspace, log10
from libsimulate import scan_param, plot_losses


if __name__ == '__main__':
    results = scan_param(
        'example_gold/xauusd-1m.json.gz',
        A=100,
        range_size=4,
        fee=logspace(log10(0.0002), log10(0.01), 20),
        Texp=600,
        n_top_samples=150
    )

    plot_losses('fee', results)
