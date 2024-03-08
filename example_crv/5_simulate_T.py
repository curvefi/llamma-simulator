from numpy import logspace, log10
from libsimulate import scan_param, plot_losses


if __name__ == '__main__':
    results = scan_param(
        'data/crvusdt-1m.json.gz',
        A=30,
        range_size=4,
        fee=0.002,
        min_loan_duration=1, max_loan_duration=1,
        samples=20000, n_top_samples=20000,
        add_reverse=True,
        Texp=[int(a) for a in logspace(log10(200), log10(40000), 20)]
    )

    plot_losses('Texp', results)
