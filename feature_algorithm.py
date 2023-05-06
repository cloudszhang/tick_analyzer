#encoding=utf-8

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

