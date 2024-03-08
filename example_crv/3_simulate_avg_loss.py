from numpy import linspace
from libsimulate import scan_param, plot_losses


if __name__ == '__main__':
    results = scan_param(
        'data/crvusdt-1m.json.gz',
        A=30,
        range_size=[int(x) for x in linspace(4, 50, 10)],
        fee=0.002,
        Texp=600,
        samples=20000, n_top_samples=20000,
        add_reverse=True,
        min_loan_duration=1, max_loan_duration=1
    )

    plot_losses('N', [results[0]])
