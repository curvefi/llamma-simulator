from numpy import logspace, log10
from libsimulate import scan_param, plot_losses


if __name__ == '__main__':
    results = scan_param(
        'example-rch/rchusdt-1m.json.gz',
        A=sorted(set(int(a) for a in logspace(log10(3), log10(200), 50))),
        range_size=4,
        fee=0.001,
        min_loan_duration=1/24, max_loan_duration=1/24,
        add_reverse=True,
        samples=2000000,
        Texp=600
    )

    plot_losses('A', results)
