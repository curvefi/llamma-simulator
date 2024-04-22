from numpy import logspace, log10
from libsimulate import scan_param, plot_losses


if __name__ == '__main__':
    results = scan_param(
        'data/fxsusdt-1m.json.gz',
        A=sorted(set(int(a) for a in logspace(log10(3), log10(200), 50))),
        range_size=4,
        fee=0.003,
        min_loan_duration=1/24/2, max_loan_duration=1/24/2,
        add_reverse=True,
        samples=2000000,
        Texp=600
    )

    plot_losses('A', results)
