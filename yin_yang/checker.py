import datetime
from datetime import time
from abc import ABC, abstractmethod

from yin_yang.config import Modes, config


class Checker:
    """Checker with strategy design pattern"""

    def __init__(self, mode: Modes):
        message = 'Dark mode will be activated '
        # set the strategy
        if mode == Modes.manual.value:
            self._mode = Manual()
            print(message + 'manually.')
        elif mode == Modes.scheduled.value:
            self._mode = Time()
            print(message + 'at ' + config.get('switch_to_dark'))
        elif mode == Modes.followSun.value:
            self._mode = Sun()
            print(message + 'at ' + config.get('switch_to_dark'))
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
        time_current = datetime.datetime.now().time()
        time_light = time.fromisoformat(config.get('switch_to_light'))
        time_dark = time.fromisoformat(config.get('switch_to_dark'))

        return compare_time(time_current, time_light, time_dark)


class Sun(Mode):
    def should_be_dark(self) -> bool:
        time_current = datetime.datetime.now().time()
        time_light, time_dark = config.get_sun_time()

        return compare_time(time_current, time_light, time_dark)


def compare_time(time_current: time, time_light: time, time_dark: time) -> bool:
    """Compares two times with current time.
    :param time_current: time to check
    :param time_dark: time dark
    :param time_light: time light
    :return: False if current time between time light and time dark, otherwise true"""

    if time_light.hour <= time_current.hour < time_dark.hour:
        return time_current.hour == time_light.hour and time_current.minute <= time_light.minute
    else:
        return not (time_current.hour == time_dark.hour and time_current.minute <= time_dark.minute)
