from numpy import logspace, log10
from libsimulate import scan_param, plot_losses


if __name__ == '__main__':
    results = scan_param(
        'data/uwuusdt-1m.json.gz',
        A=30,
        range_size=4,
        fee=logspace(log10(0.0005), log10(0.05), 20),
        min_loan_duration=0.5, max_loan_duration=0.5,
        add_reverse=True,
        samples=8000,
        n_top_samples=8000,
        Texp=600
    )

    plot_losses('fee', results)
