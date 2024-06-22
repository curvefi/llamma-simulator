from numpy import logspace, log10
from libsimulate import scan_param, plot_losses


if __name__ == '__main__':
    results = scan_param(
        'example_usde/usdecrvusd-1m.json.gz',
        A=sorted(set(int(a) for a in logspace(log10(10), log10(2000), 50))),
        range_size=4,
        fee=0.002,
        Texp=600,
        add_reverse=True,
        min_loan_duration=0.5, max_loan_duration=0.5
    )

    plot_losses('A', results)
