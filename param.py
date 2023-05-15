#encoding=utf-8


class Param(object):
    def __init__(self):
        self.data_path = r'../data'
        self.focus = 'm,i,j,RM,jm,TA,y,p,rb,hc'.split(',')
        self.next_tick_cnt = 60*2*60 #ticks of 60 minutes.
        self.prev_tick_cnt = 2*60*2*60 #ticks of 2 hours.
        return


