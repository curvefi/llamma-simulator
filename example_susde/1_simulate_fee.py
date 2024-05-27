from numpy import logspace, log10
from libsimulate import scan_param, plot_losses


if __name__ == '__main__':
    results = scan_param(
        'example_susde/susdefrax.json.gz',
        A=250,
        range_size=4,
        fee=logspace(log10(0.0001), log10(0.05), 20),
        min_loan_duration=0.1, max_loan_duration=0.1,
        add_reverse=True,
        Texp=600
    )

    plot_losses('fee', results)
