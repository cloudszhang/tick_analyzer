#encoding=utf-8
import os
import re
import pandas as pd
import numpy as np

class DataBase(object):
    def __init__(self, param):
        self.param = param
        self.path = self.param.data_path
        self.files = self.init_files_db()
        self.signal_ins = list()

        df = self.load_all_signals()
        self.signal_df = self.pick_signals(df)
        self.date_vec = self.files.date
        self.date_vec = self.date_vec.sort_values().to_list()

        self.cache_size = 10
        self.cache_tag = list()
        self.data_cache = dict()

        return


    def run(self):

        return

    def get_signal_df(self, one_ins):
        df = self.signal_df[self.signal_df.ins == one_ins]
        df = df.copy()
        df.index = np.arange(len(df))

        return df

    def get_next_date(self, curr_date):
        sn = self.date_vec.index(curr_date)
        if (sn + 1)>= len(self.date_vec):
            return None
        else:
            return self.date_vec[sn + 1]

    def get_prev_date(self, curr_date):
        sn = self.date_vec.index(curr_date)
        if (sn - 1) < 0:
            return None
        else:
            return self.date_vec[sn - 1]

    def load_next_data(self, curr_day, time, id):
        next_day = self.get_next_date(curr_day)
        self.fill_data_cache([curr_day, next_day])
        curr_tick_df = self.data_cache[curr_day]
        line_sn = curr_tick_df[(curr_tick_df.date == curr_day) & (curr_tick_df.time == time) & (curr_tick_df.id == id)].index.tolist()[-1]
        next_data = curr_tick_df[curr_tick_df.index >= line_sn]
        ticks_cnt = len(next_data[next_data.id == id])
        if ticks_cnt < self.param.next_tick_cnt:
            next_data = next_data.copy()
            if next_day in self.data_cache.keys():
                next_day_data = self.data_cache[next_day]
                next_data = next_data.append(next_day_data)
        return next_data

    def load_prev_data(self, curr_day, time, id):
        prev_day = self.get_prev_date(curr_day)
        self.fill_data_cache([curr_day, prev_day])
        curr_tick_df = self.data_cache[curr_day]
        line_sn = curr_tick_df[(curr_tick_df.date == curr_day) & (curr_tick_df.time == time) & (curr_tick_df.id == id)].index.tolist()[-1]
        curr_data = curr_tick_df[curr_tick_df.index <= line_sn]
        ticks_cnt = len(curr_data[curr_data.id == id])
        if ticks_cnt < self.param.next_tick_cnt:
            curr_data = curr_data.copy()
            if prev_day in self.data_cache.keys():
                prev_day_data = self.data_cache[prev_day]
                curr_data = prev_day_data.append(curr_data)
        return curr_data

    def trim_cache_size(self):
        if len(self.data_cache) > self.cache_size:
            del_item = self.cache_tag[0]
            self.data_cache.pop(del_item)
            del self.cache_tag[0]
        return

    def fill_data_cache(self, date_list):
        for one_item in date_list:
            if one_item is None:
                continue
            if one_item in self.data_cache.keys():
                continue
            self.trim_cache_size()
            self.fill_one_cache(one_item)
        return

    def fill_one_cache(self, one_date):
        sub_df = self.files[self.files.date == one_date]
        tick_file_name = sub_df.ticks.iloc[0]
        tick_df = pd.read_csv(tick_file_name, sep = '\t')

        tick_df = tick_df.dropna(axis = 1, how = 'all')
        tick_df.columns = 'index,id,date,time,curr,vol,vol_acc,oi,ask1,ask_vol,bid1,bid_vol,turnover'.split(',')
        tick_df = tick_df['id,date,time,curr,vol,vol_acc,oi,ask1,ask_vol,bid1,bid_vol,turnover'.split(',')]
        tick_df['ins'] = tick_df.id.str.extract('([a-zA-Z]+)')
        tick_df.index = np.arange(len(tick_df))
        self.cache_tag.append(one_date)
        self.data_cache[one_date] = tick_df.copy()

    def init_files_db(self):
        files = os.listdir(self.path)
        tick_files = list()
        signal_files = list()
        for one_file in files:
            items = re.split('\(|\)|,|_', one_file)
            one_dict = dict()
            if items[4].lower() == 'signal':
                one_dict['date'] = int(items[0])
                one_dict['signal'] = os.path.join(self.path, one_file)
                signal_files.append(one_dict)
            elif items[4].lower() == 'ticks':
                one_dict['date'] = int(items[0])
                one_dict['ticks'] = os.path.join(self.path, one_file)
                tick_files.append(one_dict)
        df_tick = pd.DataFrame(tick_files)
        df_signal = pd.DataFrame(signal_files)
        df = pd.merge(df_tick, df_signal, left_on='date', right_on='date', how= 'outer')
        df = df.sort_values('date')
        return df

    def load_all_signals(self):
        signal_files = self.files['signal'].copy()
        signal_files = signal_files.dropna()
        file_list = signal_files.to_list()

        df = None
        for one_file in file_list:
            one_df = pd.read_csv(one_file, sep = '\t')
            if df is None:
                df = one_df
            else:
                df = df.append(one_df)

        return df

    def pick_signals(self, df):
        df = df.dropna(axis = 1, how = 'all')
        columns = list()
        for one_item in df.columns:
            columns.append(one_item.lower())
        df.columns = columns

        df = df['stockid,tickdate,ticktime,signaltimes,highprice,lowpeice,currprice'.split(',')]
        df.columns = 'id,date,time,range,high,low,curr'.split(',')
        df = df.copy()
        df['ins'] = df.id.str.extract('([a-zA-Z]+)')
        df = df[df.ins.isin(self.param.focus)]

        self.signal_ins = df.ins.unique().tolist()
        df.index = np.arange(len(df))

        return df







if __name__ == '__main__':
    db = DataBase()
    db.run()