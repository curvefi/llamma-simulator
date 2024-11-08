from numpy import logspace, log10
from libsimulate import scan_param, plot_losses


if __name__ == '__main__':
    results = scan_param(
        'example_gold/xauusd-1m.json.gz',
        A=110,
        range_size=4,
        fee=logspace(log10(0.001), log10(0.05), 50),
        Texp=600,
        samples=50_000,
        n_top_samples=50_000,
        min_loan_duration=1/2, max_loan_duration=1/2
    )

    plot_losses('fee', results)
