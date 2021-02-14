from yin_yang.config import config
from yin_yang.toggle_checker.time import Time


class Sun(Time):
    def should_be_dark(self) -> bool:
        config.set_sun_time()

        return super().should_be_dark()
