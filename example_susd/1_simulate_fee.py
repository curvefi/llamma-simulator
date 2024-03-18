from numpy import logspace, log10
from libsimulate import scan_param, plot_losses


if __name__ == '__main__':
    results = scan_param(
        'data/susdusdt-1m.json.gz',
        A=100,
        range_size=4,
        fee=logspace(log10(0.0001), log10(0.02), 20),
        min_loan_duration=2, max_loan_duration=2,
        add_reverse=True,
        samples=20000, n_top_samples=10,
        Texp=30000
    )

    plot_losses('fee', results)
