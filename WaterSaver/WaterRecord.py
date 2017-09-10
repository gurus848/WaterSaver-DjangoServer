import time


class WaterRecord(object):
    def __init__(self, start_epoch, stop_epoch, average_water_rate):
        self.start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_epoch))
        self.stop_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stop_epoch))
        self.water_flowed = (stop_epoch - start_epoch) * average_water_rate
