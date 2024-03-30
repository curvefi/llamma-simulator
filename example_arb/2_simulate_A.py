from numpy import logspace, log10
from libsimulate import scan_param, plot_losses


if __name__ == '__main__':
    results = scan_param(
        'data/arbusdt-1m.json.gz',
        A=[int(a) for a in logspace(log10(10), log10(1000), 20)],
        range_size=4,
        fee=0.0045,
        Texp=600
    )

    plot_losses('A', results)
