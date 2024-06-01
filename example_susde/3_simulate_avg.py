from numpy import linspace
from libsimulate import scan_param, plot_losses


if __name__ == '__main__':
    results = scan_param(
        'example_susde/susdefrax.json.gz',
        A=200,
        range_size=[int(x) for x in linspace(4, 50, 20)],
        fee=0.002,
        Texp=600,
        add_reverse=True,
        samples=20000, n_top_samples=20000,
        min_loan_duration=1, max_loan_duration=1
    )

    plot_losses('A', results)
