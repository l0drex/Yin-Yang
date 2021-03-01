import unittest

from yin_yang.config import config, Modes
from yin_yang.yin_yang import Setter


class SetterTest(unittest.TestCase):
    def test_update_dark_value(self):
        mode_used = config.get('mode')
        config.update('mode', Modes.manual.value)
        dark_mode_active = config.get('dark_mode')

        setter = Setter()

        setter.set_mode(not dark_mode_active)
        self.assertEqual(not dark_mode_active, config.get('dark_mode'))

        setter.set_mode(dark_mode_active)
        self.assertEqual(dark_mode_active, config.get('dark_mode'))

        config.update('mode', mode_used)


if __name__ == '__main__':
    unittest.main()
