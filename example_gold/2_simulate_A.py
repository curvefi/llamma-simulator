from numpy import logspace, log10
from libsimulate import scan_param, plot_losses


if __name__ == '__main__':
    results = scan_param(
        'example_gold/xauusd-1m.json.gz',
        A=sorted(set([int(a) for a in logspace(log10(3), log10(3000), 50)])),
        range_size=4,
        fee=0.004,
        Texp=600,
        samples=300_000,
        n_top_samples=3
    )

    plot_losses('A', results)
