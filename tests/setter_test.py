import unittest

from yin_yang.config import config, Modes
from yin_yang.yin_yang import Setter


class SetterTest(unittest.TestCase):
    def test_update_dark_value(self):
        setter = Setter()

        config.update('mode', Modes.manual.value)
        mode_currently_used = config.get('dark_mode')

        setter.set_mode(not mode_currently_used)
        self.assertEqual(not mode_currently_used, config.get('dark_mode'))

        setter.set_mode(mode_currently_used)
        self.assertEqual(mode_currently_used, config.get('dark_mode'))


if __name__ == '__main__':
    unittest.main()
