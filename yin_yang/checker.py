import datetime
from abc import ABC, abstractmethod

from yin_yang.config import Modes, config


class Checker:
    """Checker with strategy design pattern"""

    def __init__(self, mode: Modes):
        # set the strategy
        if mode == Modes.manual.value:
            self._mode = Manual()
        elif mode == Modes.scheduled.value:
            self._mode = Time()
        elif mode == Modes.followSun.value:
            self._mode = Sun()
        else:
            raise ValueError('Unknown mode for determining theme.')

    def should_be_dark(self) -> bool:
        return self._mode.should_be_dark()


class Mode(ABC):
    @abstractmethod
    def should_be_dark(self) -> bool:
        raise NotImplementedError('Method should_be_dark() is not implemented')


class Manual(Mode):
    def should_be_dark(self) -> bool:
        return not config.get('dark_mode')


class Time(Mode):
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


class Sun(Time):
    def should_be_dark(self) -> bool:
        config.set_sun_time()

        return super().should_be_dark()
