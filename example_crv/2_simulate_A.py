from numpy import logspace, log10
from libsimulate import scan_param, plot_losses


if __name__ == '__main__':
    results = scan_param(
        'data/crvusdt-1m.json.gz',
        A=[int(a) for a in logspace(log10(10), log10(300), 50)],
        range_size=4,
        fee=0.002,
        min_loan_duration=1/24/2, max_loan_duration=1/24/2,
        add_reverse=True,
        Texp=600
    )

    plot_losses('A', results)
