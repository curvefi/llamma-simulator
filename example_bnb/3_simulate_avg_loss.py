from numpy import linspace
from libsimulate import scan_param, plot_losses


if __name__ == '__main__':
    results = scan_param(
        'data/bnbusdt-1m.json.gz',
        A=100,
        range_size=[int(x) for x in linspace(4, 50, 10)],
        fee=0.006,
        Texp=600,
        samples=20000, n_top_samples=20000,
        min_loan_duration=1, max_loan_duration=1
    )

    plot_losses('N', [results[0]])
