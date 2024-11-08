from numpy import logspace, log10
from libsimulate import scan_param, plot_losses


if __name__ == '__main__':
    results = scan_param(
        'example_gold/xauusd-1m.json.gz',
        A=sorted(set([int(a) for a in logspace(log10(10), log10(500), 30)])),
        range_size=4,
        fee=0.007,
        Texp=600,
        samples=200_000,
        n_top_samples=3,
        min_loan_duration=1/2, max_loan_duration=1/2
    )

    plot_losses('A', results)
