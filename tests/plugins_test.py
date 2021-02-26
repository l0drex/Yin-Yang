import unittest

from yin_yang.config import PLUGINS
from yin_yang.plugins.plugin import Plugin


class PluginsTest(unittest.TestCase):
    def test_setup(self):
        for pl in PLUGINS:
            with self.subTest(plugin=pl.name):
                self.assertIsInstance(pl, Plugin, 'Every plugin should extend the Plugin class')
                self.assertTrue(pl.name != '')
                self.assertTrue(pl.theme_dark is not None and pl.theme_bright is not None)


if __name__ == '__main__':
    unittest.main()
