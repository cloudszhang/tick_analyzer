#encoding=utf-8
import pandas as pd

from param import Param
from data_base import DataBase
import numpy as np
from feature_algorithm import FeatureAlgorithm

class FeatureLoader(object):
    def __init__(self):
        self.param = Param()
        self.db = DataBase(self.param)
        self.algorithm = FeatureAlgorithm()
        self.dump_cnt = 0
        return


    def run(self):
        signal_ins = self.db.signal_ins
        for one_ins in signal_ins:
            one_df = self.db.get_signal_df(one_ins).copy()
            for sn in range(len(one_df)):
                one_signal = one_df.iloc[sn, :]
                one_feature = self.load_one_feature(one_signal)
                self.dump_one_feature(one_feature)

        return

    def dump_one_feature(self, one_feature):
        df = pd.DataFrame([one_feature])
        if self.dump_cnt == 0:
            df.to_csv('feature.txt', sep = '\t', index = None, mode = 'w')
        else:
            df.to_csv('feature.txt', sep = '\t', index = None, header = None, mode = 'a+')
        self.dump_cnt += 1


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
        features['ins'] = one_signal.ins
        features['date'] = one_signal.date
        features['time'] = one_signal.time
        features['id'] = one_signal.id
        self.load_next_features(features, one_signal)
        self.load_curr_features(features, one_signal)
        self.load_prev_features(features, one_signal)

        return features

    def load_next_features(self, features, one_signal):
        curr_ins_next_data, all_ins_next_data = self.get_next_data(one_signal)
        features['next_10_mins_inc'] = self.algorithm.next_10_min_inc(curr_ins_next_data)
        features['first_raise_or_drop'] = self.algorithm.first_raise_or_drop(curr_ins_next_data, ths = 1.0)
        return

    def load_curr_features(self, features, one_signal):
        prev_high = one_signal.high
        prev_low = one_signal.low
        curr = one_signal.curr

        features['curr'] = curr
        features['curr_inc'] = (curr / prev_low - 1) * 100.0
        features['curr_dec'] = (curr / prev_high - 1) * 100.0
        return

    def load_prev_features(self, features, one_signal):
        return

if __name__ == '__main__':
    feature = FeatureLoader()
    feature.run()