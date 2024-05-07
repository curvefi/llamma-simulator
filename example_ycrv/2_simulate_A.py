from numpy import logspace, log10
from libsimulate import scan_param, plot_losses


if __name__ == '__main__':
    results = scan_param(
        'example_ycrv/ycrvcrvusd-1m.json.gz',
        A=sorted(set(int(a) for a in logspace(log10(10), log10(300), 50))),
        range_size=4,
        fee=0.005,
        min_loan_duration=1/24, max_loan_duration=1/24,
        add_reverse=True,
        Texp=600,
        samples=2000000,
        n_top_samples=50
    )

    plot_losses('A', results)
