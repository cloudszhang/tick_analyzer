#encoding=utf-8
from param import Param
from data_base import DataBase
import numpy as np
from feature_algorithm import FeatureAlgorithm

class FeatureLoader(object):
    def __init__(self):
        self.param = Param()
        self.db = DataBase(self.param)
        self.algorithm = FeatureAlgorithm()
        return


    def run(self):
        signal_ins = self.db.signal_ins
        for one_ins in signal_ins:
            one_df = self.db.get_signal_df(one_ins).copy()
            for sn in range(len(one_df)):
                one_signal = one_df.iloc[sn, :]
                self.load_one_feature(one_signal)

        return

    def get_next_data(self, one_signal):
        next_data = self.db.load_next_data(one_signal.date, one_signal.time, one_signal.id).copy()
        next_data.index = np.arange(len(next_data))
        curr_ins_data = next_data[next_data.id == one_signal.id]
        if len(curr_ins_data) > self.param.next_tick_cnt:
            stop_pos = curr_ins_data.iloc[self.param.next_tick_cnt].name
            all_ins_data = next_data.loc[:stop_pos]
        else:
            all_ins_data = next_data

        curr_ins_data = curr_ins_data.iloc[:self.param.next_tick_cnt].copy()
        return curr_ins_data, all_ins_data
    def load_one_feature(self, one_signal):
        features = dict()
        curr_ins_next_data, all_ins_next_data = self.get_next_data(one_signal)
        features['next_10_mins_inc'] = self.algorithm.next_10_min_inc(curr_ins_next_data)
        return


if __name__ == '__main__':
    feature = FeatureLoader()
    feature.run()