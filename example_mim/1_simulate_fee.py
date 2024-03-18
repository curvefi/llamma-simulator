from numpy import logspace, log10
from libsimulate import scan_param, plot_losses


if __name__ == '__main__':
    results = scan_param(
        'data/mimusdt-1m.json.gz',
        A=100,
        range_size=4,
        fee=logspace(log10(0.0001), log10(0.02), 20),
        min_loan_duration=10, max_loan_duration=10,
        add_reverse=True,
        samples=20000, n_top_samples=3,
        Texp=2 * 86400
    )

    plot_losses('fee', results)
