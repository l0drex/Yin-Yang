import datetime
from datetime import time
from abc import ABC, abstractmethod
from typing import Tuple

from suntime import Sun, SunTimeException

from yin_yang.config import Modes, config


class Checker:
    """Checker with strategy design pattern"""

    def __init__(self, mode: Modes):
        message = 'Dark mode will be activated '
        # set the strategy
        if mode == Modes.manual.value:
            self._mode = ManualMode()
            print(message + 'manually.')
        elif mode == Modes.scheduled.value:
            self._mode = TimeMode()
            print(message + 'at ' + config.get('switch_to_dark'))
        elif mode == Modes.followSun.value:
            self._mode = SunMode()
            print(message + 'at ' + config.get('switch_to_dark'))
        else:
            raise ValueError('Unknown mode for determining theme.')

    def should_be_dark(self) -> bool:
        return self._mode.should_be_dark()


class Mode(ABC):
    @abstractmethod
    def should_be_dark(self) -> bool:
        raise NotImplementedError('Method should_be_dark() is not implemented')


class ManualMode(Mode):
    def should_be_dark(self) -> bool:
        return not config.get('dark_mode')


class TimeMode(Mode):
    def should_be_dark(self) -> bool:
        time_current = datetime.datetime.now().time()
        time_light = time.fromisoformat(config.get('switch_to_light'))
        time_dark = time.fromisoformat(config.get('switch_to_dark'))

        return compare_time(time_current, time_light, time_dark)


class SunMode(Mode):
    def should_be_dark(self) -> bool:
        time_current = datetime.datetime.now().time()
        time_light, time_dark = get_sun_time()

        return compare_time(time_current, time_light, time_dark)


def get_sun_time() -> Tuple[time, time]:
    """Sets the sunrise and sunset to config based on location"""
    latitude, longitude = config.get('coordinates')
    sun = Sun(latitude, longitude)

    try:
        today_sr = sun.get_local_sunrise_time()
        today_ss = sun.get_local_sunset_time()

        return today_sr.time(), today_ss.time()

    except SunTimeException as e:
        print("Error: {0}.".format(e))


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
