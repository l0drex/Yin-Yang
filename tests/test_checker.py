import unittest
from datetime import time

from yin_yang.checker import ManualMode, compare_time
from yin_yang.config import config


class TestChecker(unittest.TestCase):
    def test_mode_manual(self):
        checker = ManualMode()

        for dark in [False, True]:
            with self.subTest('Changing theme manually should always be possible!', dark=dark):
                config.update('dark_mode', dark)
                self.assertEqual(not dark, checker.should_be_dark())

    def test_compare_time(self):
        time_light = time.fromisoformat('08:00')
        time_dark = time.fromisoformat('20:00')

        for time_current in [time.fromisoformat('05:00'),
                             time_dark,
                             time.fromisoformat('22:00'),
                             time.fromisoformat('00:00')]:
            with self.subTest('Dark mode should be activated!', time_current=time_current, light_before_dark=True):
                self.assertTrue(compare_time(time_current, time_light, time_dark))
            with self.subTest('Light mode should be activated', time_current=time_current, light_before_dark=False):
                self.assertFalse(compare_time(time_current, time_dark, time_light))

        for time_current in [time_light,
                             time.fromisoformat('12:00')]:
            with self.subTest('Light mode should be activated!', time_current=time_current, light_before_dark=True):
                self.assertFalse(compare_time(time_current, time_light, time_dark))
            with self.subTest('Dark mode should be activated!', time_current=time_current, light_before_dark=False):
                self.assertTrue(compare_time(time_current, time_dark, time_light))

        message = 'Light mode should always be enabled if times are equal'
        self.assertFalse(compare_time(time.fromisoformat('05:00'), time_dark, time_dark), message)
        self.assertFalse(compare_time(time_dark, time_dark, time_dark), message)
        self.assertFalse(compare_time(time.fromisoformat('22:00'), time_dark, time_dark), message)


if __name__ == '__main__':
    unittest.main()
