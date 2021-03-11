import unittest

from yin_yang.config import ConfigParser, Modes
from yin_yang.yin_yang import set_mode

config = ConfigParser()
config.load()
# NOTE set this to true if you want to test your plugin
test_theme_changes = False


class SetterTest(unittest.TestCase):
    @unittest.skipUnless(test_theme_changes, 'test_theme_changes is disabled')
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
