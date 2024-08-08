from numpy import logspace, log10
from libsimulate import scan_param, plot_losses


if __name__ == '__main__':
    results = scan_param(
        'data/ethusdt-1m.json.gz',
        A=[int(a) for a in logspace(log10(30), log10(500), 20)],
        range_size=4,
        fee=0.002,
        Texp=600,
        add_reverse=True,
        min_loan_duration=1/24/2, max_loan_duration=1/24/2,
        n_top_samples=1,
        other = {'dynamic_fee_multiplier': 0.5, 'use_po_fee': 1, 'po_fee_delay': 2}
    )

    plot_losses('A', results)
