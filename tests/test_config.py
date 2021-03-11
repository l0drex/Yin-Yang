import unittest

from yin_yang.config import ConfigParser, PLUGINS, Modes


class ConfigTest(unittest.TestCase):
    def setUp(self) -> None:
        self.config = ConfigParser()
        self.config.set_default()

    def test_get_value(self):
        message = 'All general config values must have the correct type.'

        self.assertIsInstance(self.config.version, float, message)
        self.assertIsInstance(self.config.running, bool, message)
        self.assertIsInstance(self.config.desktop, str, message)
        self.assertIsInstance(self.config.mode, Modes, message)
        self.assertIsInstance(self.config.location, tuple, message)

        message = 'Times for switching must be time objects.'
        self.assertIsInstance(self.config.times, tuple, message)

        message = 'All plugin config values must have the correct type.'
        for p in PLUGINS:
            with self.subTest(message, plugin=p.name):
                self.assertIsInstance(self.config.get(p.name, 'enabled'), bool)
                self.assertIsInstance(self.config.get(p.name, 'light_theme'), str)
                self.assertIsInstance(self.config.get(p.name, 'dark_theme'), str)

    def test_update_value(self):
        self.config.dark_mode = True
        self.assertTrue(self.config.dark_mode,
                        'Key should be updated.')
        self.assertTrue(self.config.update(PLUGINS[0].name, 'enabled', True),
                        'Updating settings for plugins should be possible.')
        self.assertTrue(self.config.update(PLUGINS[0].name.title(), 'enabled', True),
                        'Plugin names should not be case sensitive.')
        self.assertTrue(self.config.changed,
                        'Config should see itself as changed when it is.')

    @unittest.skip('Implementation needed')
    def test_updates_old_files(self):
        pass

    @unittest.skip('Implementation needed')
    def test_writes_file(self):
        pass


if __name__ == '__main__':
    unittest.main()
