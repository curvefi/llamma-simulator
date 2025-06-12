from numpy import logspace, log10
from libsimulate import scan_param, plot_losses


if __name__ == '__main__':
    results = scan_param(
        'data/lp-markets/cvxcrv/lp-crvusd-1m.json',
        'data/lp-markets/cvxcrv/lp-crvusd-calc-1m.json',
        A=50,
        range_size=4,
        fee=logspace(log10(0.0005), log10(0.05), 20),
        Texp=600,
        add_reverse=True,
        min_loan_duration=1/24,
        max_loan_duration=1/24
    )

    plot_losses('fee', results)
