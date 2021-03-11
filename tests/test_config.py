import json
import os
import unittest
from pathlib import Path

from yin_yang.config import ConfigParser, PLUGINS, Modes, update_config

path = str(Path.home()) + '/.config/yin_yang/yin_yang.json'


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

    def test_updates_old_files(self):
        old_configs = [
            {
                "version": 2.1,
                "desktop": self.config.desktop,
                "followSun": False,
                "latitude": "",
                "longitude": "",
                "schedule": False,
                "switchToDark": "20:00",
                "switchToLight": "07:00",
                "running": False,
                "theme": "",
                "codeLightTheme": "Default Light+", "codeDarkTheme": "Default Dark+",
                "codeEnabled": False,
                "kdeLightTheme": "org.kde.breeze.desktop",
                "kdeDarkTheme": "org.kde.breezedark.desktop",
                "kdeEnabled": False, "gtkLightTheme": "",
                "gtkDarkTheme": "", "atomLightTheme": "",
                "atomDarkTheme": "", "atomEnabled": False,
                "gtkEnabled": False,
                "wallpaperLightTheme": "",
                "wallpaperDarkTheme": "",
                "wallpaperEnabled": False,
                "firefoxEnabled": False,
                "firefoxDarkTheme": "firefox-compact-dark@mozilla.org",
                "firefoxLightTheme": "firefox-compact-light@mozilla.org",
                "firefoxActiveTheme": "firefox-compact-light@mozilla.org",
                "gnomeEnabled": False,
                "gnomeLightTheme": "",
                "gnomeDarkTheme": "",
                "kvantumEnabled": False,
                "kvantumLightTheme": "",
                "kvantumDarkTheme": "",
                "soundEnabled": True
            }
        ]
        for old_config in old_configs:
            with self.subTest(version=old_config['version']):
                new_config = update_config(old_config, self.config.defaults)

                for key in self.config.defaults:
                    self.assertTrue(new_config.get(key) is not None,
                                    'All default keys should be contained in the new config')
                for key in new_config:
                    self.assertTrue(self.config.defaults.get(key) is not None,
                                    'No new keys should be added to the new config file')

    @unittest.skipUnless(os.path.isfile(path), 'No config file found')
    def test_loads_file(self):
        self.config.load()
        with open(path, 'r') as file:
            data: dict = json.load(file)
            self.assertDictEqual(data, self.config.data,
                                 'Loaded data should be correct')

    def test_writes_file(self):
        if os.path.isfile(path):
            self.config.load()
            old_data = self.config.data

        self.assertTrue(self.config.write(),
                        'Config could not be saved')
        self.test_loads_file()

        if os.path.isfile(path):
            with open(path, 'w') as file:
                json.dump(old_data, file, indent=4)


if __name__ == '__main__':
    unittest.main()
