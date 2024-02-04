from numpy import logspace, log10
from libsimulate import scan_param, plot_losses


if __name__ == '__main__':
    results = scan_param(
        'data/crvusdt-1m.json.gz',
        A=50,
        range_size=4,
        fee=0.006,
        Texp=[int(a) for a in logspace(log10(300), log10(40000), 20)]
    )

    plot_losses('Texp', results)
