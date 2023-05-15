#encoding=utf-8
import numpy as np

class FeatureAlgorithm(object):
    def __init__(self):
        return

    def valid_tick(self, tick):
        tick = tick.copy()
        if tick.bid1 < 0.1:
            tick.bid1 = tick.ask1
        if tick.ask1 < 0.1:
            tick.ask1 = tick.bid1
        return tick

    #using 10*60*2 ticks, not using minutes, because it is difficult to calc time
    def next_10_min_inc(self, df):
        tick_curr = df.iloc[0]
        tick_curr = self.valid_tick(tick_curr)

        tick_per_10_min = 10 * 60 * 2
        tick_10min = df.iloc[tick_per_10_min] if len(df) > tick_per_10_min else df.iloc[-1]
        tick_10min = self.valid_tick(tick_10min)
        inc = (tick_10min.bid1 /tick_curr.bid1 - 1) * 100
        return inc

    #后续走势先上张到1%,还是先下跌到1%
    def first_raise_or_drop(self,df, ths = 1.0):
        tick_curr = df.iloc[0]

        price_curr = tick_curr.bid1
        if price_curr < 0.1:
            return np.nan

        df = df.copy()
        df = df[df.bid1 > 0]
        df.index = np.arange(len(df))
        df['inc'] = df.bid1 - price_curr
        inc_ths = price_curr * ths / 100.0

        inc_df = df[df.inc > inc_ths]
        dec_df = df[df.inc < -inc_ths]

        if len(inc_df) == 0 and len(dec_df) == 0:
            return np.nan
            return
        if len(inc_df) > 0 and len(dec_df) == 0:
            return 1.0

        if len(inc_df) == 0 and len(dec_df) > 0:
            return -1.0
        else:
            inc_sn = inc_df.index[0]
            dec_sn = dec_df.index[0]
            if inc_sn < dec_sn:
                return 1.0
            else:
                return -1.0


        return 0

    def prev_inc_ratio(self, prev_df):
        df = prev_df.copy()
        curr_tick = df.iloc[-1]
        curr_tick = self.valid_tick(curr_tick)
        curr = curr_tick.bid1
        df['ratio'] = (df.bid1 / curr -1) * 100
        df['inc'] = df.ratio - df.ratio.iloc[-1]

        return 0