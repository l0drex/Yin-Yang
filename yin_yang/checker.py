import datetime
import logging
from datetime import time
from abc import ABC, abstractmethod

from yin_yang.config import Modes, config, get_sun_time

logger = logging.getLogger(__name__)


class Checker:
    """Checker with strategy design pattern"""

    def __init__(self, mode: Modes):
        message = 'Dark mode will be activated '
        # set the strategy
        if mode == Modes.manual.value:
            logger.info(message + 'manually.')
            self._mode = ManualMode()
        elif mode == Modes.scheduled.value:
            logger.info(message + f'between {config.get("switch_to_dark")} and {config.get("switch_to_light")}.')
            self._mode = TimeMode()
        elif mode == Modes.followSun.value:
            time_dark, time_light = get_sun_time()
            logger.info(message + f'between {time_dark.strftime("%H:%M")} and {time_light.strftime("%H:%M")}.')
            self._mode = SunMode()
        else:
            logger.error('Mode could not be specified.')
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
