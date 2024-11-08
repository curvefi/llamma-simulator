#!/usr/bin/env python3

import json
import random
from multiprocessing import Pool, cpu_count
from collections.abc import Iterable
from datetime import datetime
from libmodel import LendingAMM


pool = None
price_data = None
EXT_FEE = 2.5e-3  # Need to be set to the actual redemption fee for arb traders
ORACLE_THRESHOLD = 3e-3  # 0.3% on Ethereum/Chainlink
ORACLE_EMA = False  # Using raw Chainlink with no EMA! Saves gas but losses are higher


class Simulator:
    min_loan_duration = 1  # day
    max_loan_duration = 1  # days
    SAMPLES = 400
    other = {'dynamic_fee_multiplier': 0, 'use_po_fee': 1, 'po_fee_delay': 2}

    def __init__(self, filename, ext_fee, add_reverse=False,
                 log=False, verbose=False):
        """
        filename - OHLC data in the same format as Binance returns
        ext_fee - Fee which arb trader pays to external platforms
        add_reverse - Attach the same data with the time reversed
        """
        self.filename = filename
        self.ext_fee = ext_fee
        self.add_reverse = add_reverse
        self.load_prices()
        self.log = log
        self.verbose = verbose
        self.ema_time = 0
        self.emas = []

    def load_prices(self):
        global price_data

        if self.filename.endswith('.gz'):
            import gzip
            with gzip.open(self.filename, "r") as f:
                data = json.load(f)
        else:
            with open(self.filename, "r") as f:
                data = json.load(f)
        # timestamp, OHLC, vol
        unfiltered_data = [[int(d[0]) * 1000] + [float(x) for x in d[1:6]] for d in data]
        data = []
        prev_time = 0
        for d in unfiltered_data:
            if d[0] >= prev_time:
                data.append(d)
                prev_time = d[0]
        if self.add_reverse:
            t0 = data[-1][0]
            data += [[t0 + (t0 - d[0])] + d[1:] for d in data[::-1]]
        price_data = data

    def update_emas(self, Texp):
        if self.ema_time != Texp:
            self.ema_time = Texp
            self.emas = []
            ema = price_data[0][1]
            ema_t = price_data[0][0]
            oracle = ema
            for t, _, high, low, _, _ in price_data:
                if ORACLE_EMA:
                    ema_mul = 2 ** (- (t - ema_t) / (1000 * Texp))
                new_oracle = (low + high) / 2
                if abs(oracle - new_oracle) / new_oracle >= ORACLE_THRESHOLD:
                    oracle = new_oracle
                if ORACLE_EMA:
                    ema = ema * ema_mul + oracle * (1 - ema_mul)
                else:
                    ema = oracle
                ema_t = t
                self.emas.append(ema)

    def single_run(self, A, range_size, fee, Texp, position, size, p_shift=None, **kw):
        """
        position: 0..1
        size: fraction of all price data length for size
        """
        self.update_emas(Texp)

        # Data for prices
        pos = (int(position * len(price_data)), int((position + size) * len(price_data)))
        data = price_data[pos[0]: pos[1]]
        emas = self.emas[pos[0]: pos[1]]
        if p_shift is None:
            p0 = data[0][1]
        else:
            p0 = data[0][1] * (1 - p_shift)
        initial_y0 = 1.0
        p_base = p0 * (A / (A - 1) + 1e-4)
        initial_x_value = initial_y0 * p_base
        amm = LendingAMM(p_base, A, fee, **kw)

        # Fill ticks with liquidity
        amm.deposit_nrange(initial_y0, p0, range_size)  # 1 ETH
        initial_all_x = amm.get_all_x()

        losses = []
        fees = []

        def find_target_price(p, is_up=True, new=False):
            if is_up:
                for n in range(amm.max_band, amm.min_band - 1, -1):
                    p_down = amm.p_down(n)
                    dfee = amm.dynamic_fee(n, new=new)
                    p_down_ = p_down * (1 + dfee)
                    # XXX print(n, amm.min_band, amm.max_band, p_down, p, amm.get_p())
                    if p > p_down_:
                        p_up = amm.p_up(n)
                        p_up_ = p_up * (1 + dfee)
                        # if p >= p_up_:
                        #     return p_up
                        # else:
                        return (p - p_down_) / (p_up_ - p_down_) * (p_up - p_down) + p_down
            else:
                for n in range(amm.min_band, amm.max_band + 1):
                    p_up = amm.p_up(n)
                    dfee = amm.dynamic_fee(n, new=new)
                    p_up_ = p_up * (1 - dfee)
                    if p < p_up_:
                        p_down = amm.p_down(n)
                        p_down_ = p_down * (1 - dfee)
                        # if p <= p_down_:
                        #     return p_down
                        # else:
                        return p_up - (p_up_ - p) / (p_up_ - p_down_) * (p_up - p_down)

            if is_up:
                return p * (1 - amm.dynamic_fee(amm.min_band, new=False))
            else:
                return p * (1 + amm.dynamic_fee(amm.max_band, new=False))

        for (t, o, high, low, c, vol), ema in zip(data, emas):
            amm.set_p_oracle(ema)
            # max_price = amm.p_up(amm.max_band)
            # min_price = amm.p_down(amm.min_band)
            high = find_target_price(high * (1 - self.ext_fee), is_up=True, new=True)
            low = find_target_price(low * (1 + self.ext_fee), is_up=False, new=False)
            # high = high * (1 - EXT_FEE - fee)
            # low = low * (1 + EXT_FEE + fee)
            # if high > amm.get_p():
            #     print(high, '/', high_, '/', max_price, '; ', low, '/', low_, '/', min_price)
            if high > amm.get_p():
                try:
                    amm.trade_to_price(high)
                except Exception:
                    print(high, low, amm.get_p())
                    raise

            # Not correct for dynamic fees which are too high
            # if high > max_price:
            #     # Check that AMM has only stablecoins
            #     for n in range(amm.min_band, amm.max_band + 1):
            #         assert amm.bands_y[n] == 0
            #         assert amm.bands_x[n] > 0

            if low < amm.get_p():
                amm.trade_to_price(low)

            # Not correct for dynamic fees which are too high
            # if low < min_price:
            #     # Check that AMM has only collateral
            #     for n in range(amm.min_band, amm.max_band + 1):
            #         assert amm.bands_x[n] == 0
            #         assert amm.bands_y[n] > 0

            d = datetime.fromtimestamp(t//1000).strftime("%Y/%m/%d %H:%M")
            fees.append(amm.dynamic_fee(amm.active_band, new=False))
            if self.log or self.verbose:
                loss = amm.get_all_x() / initial_x_value * 100
                if self.log:
                    print(f'{d}\t{o:.2f}\t{ema:.2f}\t{amm.get_p():.2f}\t\t{loss:.2f}%')
                if self.verbose:
                    losses.append([t//1000, loss / 100])

        if losses:
            self.losses = losses

        loss = 1 - amm.get_all_x() / initial_all_x
        return loss

    def f(self, x):
        A, range_size, fee, Texp, pos, size, p_shift, other = x
        try:
            return self.single_run(A, range_size, fee, Texp, pos, size, p_shift=p_shift, **other)
        except Exception as e:
            print(e)
            return 0

    def get_loss_rate(self, A, range_size, fee, Texp, samples=None,
                      max_loan_duration=None, min_loan_duration=None,
                      n_top_samples=None, other={}):
        _other = {k: v for k, v in self.other.items()}
        _other.update(other)
        other = _other
        if not samples:
            samples = self.SAMPLES
        if not max_loan_duration:
            max_loan_duration = self.max_loan_duration
        if not min_loan_duration:
            min_loan_duration = self.min_loan_duration
        dt = 86400 * 1000 / (price_data[-1][0] - price_data[0][0])  # Which fraction of all data is 1 day
        inputs = [(A, range_size, fee, Texp, random.random(), (max_loan_duration-min_loan_duration) * dt * random.random() +
                   min_loan_duration*dt, 0, other) for _ in range(samples)]
        result = pool.map(self.f, inputs, 1000)
        if not n_top_samples:
            n_top_samples = samples // 20
        return sum(sorted(result)[::-1][:n_top_samples]) / n_top_samples


def init_multicore():
    global pool
    pool = Pool(cpu_count())


def scan_param(filename, **kw):
    simulator = Simulator(filename, EXT_FEE, add_reverse=kw.pop('add_reverse', True))
    init_multicore()
    args = {'samples': 500000, 'n_top_samples': 50, 'min_loan_duration': 0.15, 'max_loan_duration': 0.15}
    args.update(kw)
    iterable_args = [k for k in kw if isinstance(kw[k], Iterable) and not isinstance(kw[k], dict)]
    assert len(iterable_args) == 1, "Not one iterable item"
    scanned_name = iterable_args[0]
    scanned_args = kw[scanned_name]
    del args[scanned_name]

    losses = []
    discounts = []

    for v in scanned_args:
        args[scanned_name] = v
        loss = simulator.get_loss_rate(**args)
        A = args['A']
        range_size = args['range_size']

        # Simplified formula
        # bands_coefficient = (((A - 1) / A) ** range_size) ** 0.5
        # More precise
        bands_coefficient = sum(((A - 1) / A) ** (k + 0.5) for k in range(range_size)) / range_size
        cl = 1 - (1 - loss) * bands_coefficient

        print(f'{scanned_name}={v}\t->\tLoss={loss},\tLiq_discount={cl}')

        losses.append(loss)
        discounts.append(cl)

    return [(scanned_args, losses), (scanned_args, discounts)]


def plot_losses(param_name, losses):
    try:
        import pylab
        import matplotlib
        try:
            matplotlib.use('Qt5Agg')
        except Exception:
            matplotlib.use('TkAgg')

    except ImportError:
        raise

    for (x, y) in losses:
        pylab.plot(x, y)

    pylab.grid()
    pylab.ylabel('Loss')
    pylab.xlabel(param_name)
    pylab.show()


if __name__ == '__main__':
    simulator = Simulator('example_gold/xauusd-1m.json.gz', 5e-4, add_reverse=False)
    init_multicore()
    print(simulator.get_loss_rate(
        100, 4, 0.005, min_loan_duration=0.05, max_loan_duration=0.05, Texp=600,
        samples=300000, n_top_samples=3))
