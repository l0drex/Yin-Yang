import os
import unittest
from datetime import time
from pathlib import Path

from yin_yang.config import ConfigParser, PLUGINS


class ConfigTest(unittest.TestCase):
    def setUp(self) -> None:
        self.config = ConfigParser(2.2)
        self.config.set_default()

    def test_get_value(self):
        message = 'All general config values must have the correct type.'

        self.assertIsInstance(self.config.get('version'), float, message)
        self.assertIsInstance(self.config.get('running'), bool, message)
        self.assertIsInstance(self.config.get('desktop'), str, message)
        self.assertIsInstance(self.config.get('mode'), str, message)
        self.assertIsInstance(self.config.get('coordinates'), tuple, message)

        message = 'Times for switching must be strings in iso format.'
        time_light = self.config.get('switch_to_light')
        time_dark = self.config.get('switch_to_dark')
        self.assertIsInstance(time_light, str, message)
        self.assertIsInstance(time_dark, str, message)

        self.assertIsInstance(time.fromisoformat(time_light), time, message)
        self.assertIsInstance(time.fromisoformat(time_dark), time, message)

        message = 'All plugin config values must have the correct type.'
        for p in PLUGINS:
            with self.subTest(message, plugin=p.name):
                self.assertIsInstance(self.config.get('enabled', p.name), bool)
                self.assertIsInstance(self.config.get('light_theme', p.name), str)
                self.assertIsInstance(self.config.get('dark_theme', p.name), str)

    def test_update_value(self):
        self.assertTrue(self.config.update('dark_mode', True),
                        'Method should update the key and return the new value.')
        self.assertTrue(self.config.get('dark_mode'),
                        'Key should be updated.')
        self.assertTrue(self.config.update('DARK_Mode', True),
                        'Specified key should be case insensitive.')
        self.assertTrue(self.config.update('enabled', True, PLUGINS[0].name),
                        'Updating settings for plugins should be possible.')
        self.assertTrue(self.config.update('enabled', True, PLUGINS[0].name.title()),
                        'Plugin names should not be case sensitive.')
        self.assertTrue(self.config.changed,
                        'Config should see itself as changed when it is.')

    @unittest.skipUnless(os.path.isfile(str(Path.home()) + '/.config/yin_yang/yin_yang.json'),
                         'No config file found.')
    def test_loads_file(self):
        self.config.load()
        self.assertIsInstance(self.config.get_config(), dict,
                              'The inner config should be a dict.')
        self.assertFalse(self.config.get_config() == {},
                         'The loaded config should not be empty.')
        self.assertFalse(self.config.changed,
                         'Config should not be marked as changed when it has just been loaded.')

    @unittest.skip('Implementation needed')
    def test_updates_old_files(self):
        pass

    @unittest.skip('Implementation needed')
    def test_writes_file(self):
        pass


if __name__ == '__main__':
    unittest.main()
