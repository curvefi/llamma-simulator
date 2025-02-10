from numpy import logspace, log10
from libsimulate import scan_param, plot_losses


if __name__ == '__main__':
    results = scan_param(
        'example_ftm/ftmusd-1m.json.gz',
        A=sorted(set([int(a) for a in logspace(log10(5), log10(50), 20)])),
        range_size=4,
        fee=0.005,
        min_loan_duration=1/24/2, max_loan_duration=1/24/2,
        add_reverse=True,
        Texp=600,
        samples=4_000_000,
        n_top_samples=10,
        other={'dynamic_fee_multiplier': 0.5, 'use_po_fee': 1, 'po_fee_delay': 2}
    )

    plot_losses('A', results)
