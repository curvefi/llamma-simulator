from numpy import logspace, log10
from libsimulate import scan_param, plot_losses


if __name__ == '__main__':
    results = scan_param(
        'data/susdusdt-1m.json.gz',
        A=[int(a) for a in logspace(log10(50), log10(10000), 50)],
        range_size=4,
        fee=0.0003,
        min_loan_duration=4, max_loan_duration=4,
        samples=25000, n_top_samples=10,
        add_reverse=True,
        Texp=30000
    )

    plot_losses('A', results)
