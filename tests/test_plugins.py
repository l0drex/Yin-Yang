import unittest

from PyQt5.QtWidgets import QGroupBox

from yin_yang.config import PLUGINS, config
from yin_yang.plugins.plugin import Plugin


class PluginsTest(unittest.TestCase):
    def test_setup(self):
        for pl in PLUGINS:
            with self.subTest(plugin=pl.name):
                self.assertIsInstance(pl, Plugin, 'Every plugin should extend the Plugin class')
                self.assertTrue(pl.name != '', 'Every plugin needs a name for the config and the gui.')
                self.assertTrue(pl.theme_dark is not None and pl.theme_bright is not None,
                                'No default theme is specified. ' +
                                'If your plugin does not support any default themes, use empty strings.')
                self.assertIsInstance(pl.get_themes_available(), dict,
                                      'Available themes always should be a dict.')

    def test_set_theme_works(self):
        for pl in PLUGINS:
            with self.subTest(plugin=pl.name):
                if config.get('enabled', pl.name):
                    pl.set_mode(config.get('dark_mode'))


if __name__ == '__main__':
    unittest.main()
