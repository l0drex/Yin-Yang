import json
import os
import unittest
from pathlib import Path

from yin_yang.config import ConfigManager, PLUGINS, Modes, update_config
from psutil import process_iter
import time
from datetime import datetime
from yin_yang import yin_yang
from multiprocessing import Process
import subprocess

path = str(Path.home()) + '/.config/yin_yang/yin_yang.json'
config = ConfigManager()


class ConfigTest(unittest.TestCase):
    def setUp(self) -> None:
        config.set_default()

    def test_get_value(self):
        message = 'All general config values must have the correct type.'

        self.assertIsInstance(config.version, float, message)
        self.assertIsInstance(config.running, bool, message)
        self.assertIsInstance(config.desktop, str, message)
        self.assertIsInstance(config.mode, Modes, message)
        self.assertIsInstance(config.location, tuple, message)

        message = 'Times for switching must be time objects.'
        self.assertIsInstance(config.times, tuple, message)

        message = 'All plugin config values must have the correct type.'
        for p in PLUGINS:
            with self.subTest(message, plugin=p.name):
                self.assertIsInstance(config.get(p.name, 'light_theme'), str)
                self.assertIsInstance(config.get(p.name, 'dark_theme'), str)
                self.assertIsInstance(config.get(p.name, 'enabled'), bool)

    def test_running(self):
        # save some config values
        was_running = config.running
        previous_mode = config.mode
        if was_running:
            # stop running processes
            # save is done automatically
            config.mode = Modes.manual

            # wait until next check and give one extra second for computing
            print('Waiting until next check...')
            time.sleep(config.update_interval - datetime.now().second + 1)
            config.mode = previous_mode

        self.assertFalse(config.running, 'Yin Yang is not running')

        # start yin yang in the background and check if config.running is true
        p_main = Process(target=yin_yang.run)
        p_check = Process(target=self.check)
        p_main.start()
        p_check.start()
        p_main.join(10)
        p_check.join()
        p_main.terminate()

        # this is not a test but rather a check for debugging,
        # it should always be true
        config.load()
        assert not config.running, 'Yin Yang should not run anymore'

        if was_running:
            print('Yin Yang was stopped for this test. \
                  Please restart the background process.')

    def test_update_value(self):
        old_value = config.update_location
        config.update_location = not old_value
        self.assertEqual(config.update_location, not old_value,
                         'Key should be updated.')
        self.assertTrue(config.update(PLUGINS[0].name, 'enabled', True),
                        'Updating settings for plugins should be possible.')
        self.assertTrue(config.update(PLUGINS[0].name.title(), 'enabled', True),
                        'Plugin names should not be case sensitive.')
        self.assertTrue(config.changed,
                        'Config should see itself as changed when it is.')

    def test_updates_old_files(self):
        old_configs = [
            {
                "version": 2.1,
                "desktop": config.desktop,
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
                new_config = update_config(old_config, config.defaults)

                for key in config.defaults:
                    self.assertTrue(new_config.get(key) is not None,
                                    'All default keys should be contained in the new config')
                for key in new_config:
                    self.assertTrue(config.defaults.get(key) is not None,
                                    'No new keys should be added to the new config file')

    @unittest.skipUnless(os.path.isfile(path), 'No config file found')
    def test_loads_file(self):
        config.load()
        with open(path, 'r') as file:
            data: dict = json.load(file)
            self.assertDictEqual(data, config.data,
                                 'Loaded data should be correct')

    def test_writes_file(self):
        if os.path.isfile(path):
            config.load()
            old_data = config.data

        self.assertTrue(config.write(),
                        'Config could not be saved')
        self.test_loads_file()

        if os.path.isfile(path):
            with open(path, 'w') as file:
                json.dump(old_data, file, indent=4)

    def check(self):
        self.assertTrue(config.running, 'Yin Yang is running')
        config.running = False


if __name__ == '__main__':
    unittest.main()
