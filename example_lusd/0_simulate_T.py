from numpy import logspace, log10
from libsimulate import scan_param, plot_losses


if __name__ == '__main__':
    results = scan_param(
        'data/lusdusdt-1m.json.gz',
        A=100,
        range_size=4,
        fee=0.002,
        min_loan_duration=10, max_loan_duration=10,
        samples=50000, n_top_samples=10,
        add_reverse=True,
        Texp=[int(a) for a in logspace(log10(500), log10(86400 * 2), 20)]
    )

    plot_losses('Texp', results)
