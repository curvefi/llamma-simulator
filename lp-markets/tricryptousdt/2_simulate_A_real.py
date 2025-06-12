from numpy import logspace, log10
from libsimulate import scan_param, plot_losses


if __name__ == '__main__':
    results = scan_param(
        'data/lp-markets/tricryptousdt/lp-crvusd-1m.json',
        'data/lp-markets/tricryptousdt/lp-crvusd-calc-1m.json',
        A=[int(a) for a in logspace(log10(30), log10(200), 30)],
        range_size=4,
        fee=0.007,
        Texp=600,
        add_reverse=True,
        min_loan_duration=1/24,
        max_loan_duration=1/24
    )

    plot_losses('A', results)
