from yin_yang.config import config
from yin_yang.toggle_checker.checker import Checker


class Manual(Checker):
    def should_be_dark(self) -> bool:
        return not config.get('dark_mode')
