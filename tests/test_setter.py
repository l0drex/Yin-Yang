import unittest

from yin_yang.config import config, Modes
from yin_yang.yin_yang import set_mode


class SetterTest(unittest.TestCase):
    def test_update_dark_value(self):
        mode_used = config.mode
        config.mode = Modes.manual
        dark_mode_active = config.dark_mode

        set_mode(not dark_mode_active)
        self.assertEqual(not dark_mode_active, config.dark_mode)

        set_mode(dark_mode_active)
        self.assertEqual(dark_mode_active, config.dark_mode)

        config.mode = mode_used


if __name__ == '__main__':
    unittest.main()
