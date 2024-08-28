from numpy import logspace, log10
from libsimulate import scan_param, plot_losses


if __name__ == '__main__':
    results = scan_param(
        'example_op_conservative/opusdt-1m.json.gz',
        A=sorted(set(int(a) for a in logspace(log10(10), log10(200), 40))),
        range_size=4,
        fee=0.006,  # 3 x feed fee
        Texp=600,
        add_reverse=True,
        min_loan_duration=1/24/2, max_loan_duration=1/24/2,
        n_top_samples=1,  # Uses the very top loss of all
        samples=5_000_000,
        other={'dynamic_fee_multiplier': 0.5, 'use_po_fee': 1, 'po_fee_delay': 2}
    )

    plot_losses('A', results)
