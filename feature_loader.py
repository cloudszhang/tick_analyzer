#encoding=utf-8
from param import Param
from data_base import DataBase

class FeatureLoader(object):
    def __init__(self):
        self.param = Param()
        self.db = DataBase(self.param)
        return


    def run(self):
        signal_ins = self.db.signal_ins
        for one_ins in signal_ins:
            one_df = self.db.get_signal_df(one_ins).copy()
            for sn in range(len(one_df)):
                one_signal = one_df.iloc[sn, :]
                self.load_one_feature(one_signal)

        return

    def load_one_feature(self, one_signal):
        next_data = self.db.load_next_data(one_signal.date, one_signal.time, one_signal.id)
        return


if __name__ == '__main__':
    feature = FeatureLoader()
    feature.run()