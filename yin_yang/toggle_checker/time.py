import datetime

from yin_yang.config import config
from yin_yang.toggle_checker.checker import Checker


class Time(Checker):
    def should_be_dark(self) -> bool:
        d_hour = int(config.get("switch_To_Dark").split(":")[0])
        d_minute = int(config.get("switch_To_Dark").split(":")[1])
        l_hour = int(config.get("switch_To_Light").split(":")[0])
        l_minute = int(config.get("switch_To_Light").split(":")[1])
        hour = datetime.datetime.now().time().hour
        minute = datetime.datetime.now().time().minute

        if l_hour <= hour < d_hour:
            return hour == l_hour and minute <= l_minute
        else:
            return not (hour == d_hour and minute <= d_minute)
