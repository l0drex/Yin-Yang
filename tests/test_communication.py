import json
import struct
import sys
import unittest
from datetime import datetime
from subprocess import Popen, PIPE

import communicate
from yin_yang.checker import Checker
from yin_yang.config import ConfigParser, Modes

config = ConfigParser(2.2)


class CommunicationTest(unittest.TestCase):
    def setUp(self):
        # reset all changes
        global config
        config = ConfigParser(2.2)

    def test_parse_time(self):
        response = communicate.parse_time('07:00')

        self.assertIsInstance(response, int)
        date = datetime.fromtimestamp(response)
        self.assertEqual(date.strftime('%H:%M'), '07:00')

        now: int = int(datetime.now().timestamp())
        one_hour_later = communicate.parse_time(datetime.fromtimestamp(now + 60*60).strftime('%H:%M'))
        one_hour_later_next_day = datetime.today().timestamp() + 60*60 + 60+60*24
        self.assertTrue(one_hour_later < one_hour_later_next_day,
                        'Time should not be increased by one day if it is already in the future')

    def test_message_build(self):
        message = communicate.send_config('firefox')
        self.assertNotEqual(message, None,
                            'Message should not be empty')
        self.assertNotEqual(message, {},
                            'Message should not be empty')
        self.assertIsInstance(message['enabled'], bool)
        self.assertIsInstance(message['dark_mode'], bool)
        if message['enabled']:
            self.assertIsInstance(message['scheduled'], bool)
            self.assertIsInstance(message['themes'][0], str)
            self.assertIsInstance(message['themes'][1], str)
            if message['scheduled']:
                time_dark, time_light = message['times']
                self.assertIsInstance(time_light, int)
                self.assertIsInstance(time_dark, int)
                time_now = datetime.today().timestamp()
                self.assertTrue(time_light <= time_now < time_dark or time_dark <= time_now < time_light,
                                'Current time should always be between light and dark times')

    def test_encode_decode(self):
        message = communicate.send_config('firefox')

        process = Popen([sys.executable, '../communicate.py'],
                        stdin=PIPE, stdout=PIPE)

        # build call
        call = {
            'name': 'Firefox',
            'themes': []
        }
        call_encoded = json.dumps(call).encode('utf-8')
        call_encoded = struct.pack(str(len(call_encoded)) + 's',
                                   call_encoded)
        msg_length = struct.pack('=I', len(call_encoded))

        # send call and get response
        process.stdin.write(msg_length)
        process.stdin.write(call_encoded)
        process.stdin.flush()
        process.stdin.close()
        response = process.stdout.readline()
        process.terminate()

        # decode response
        response_length = struct.unpack('=I', response[:4])[0]
        response = response[4:]
        response_decoded = response[:response_length].decode('utf-8')
        response_decoded = json.loads(response_decoded)

        # test if correct
        self.assertEqual(message, response_decoded,
                         'Returned message should be equal to the message')

    def test_dark_mode_detection_scheduled(self):
        config.update('mode', Modes.scheduled.value)
        time_current: int = int(datetime.today().timestamp())
        checker_scheduled = Checker(Modes.scheduled.value)
        msg = 'Dark mode should be decided correctly.'
        times = [
            # day
            [time_current - 60, time_current + 60],
            # night
            [time_current - 120, time_current - 60],
            # morning
            [time_current + 60, time_current + 120],
        ]

        for time_light, time_dark in times:
            with self.subTest(msg,
                              time_current=datetime.fromtimestamp(time_current).strftime('%H:%M'),
                              time_light_str=datetime.fromtimestamp(time_light).strftime('%H:%M'),
                              time_dark_str=datetime.fromtimestamp(time_dark).strftime('%H:%M')):
                # update config with those times
                config.update('switch_to_light', datetime.fromtimestamp(time_light).strftime('%H:%M'))
                config.update('switch_to_dark', datetime.fromtimestamp(time_dark).strftime('%H:%M'))
                # get unix times
                time_light_unix, time_dark_unix = communicate.send_config('firefox')['times']

                # NOTE: this should be equal to how the extension calculates the theme
                should_be_dark_extension = time_dark_unix <= time_current < time_light_unix
                self.assertEqual(checker_scheduled.should_be_dark(), should_be_dark_extension,
                                 'Dark mode should be ' + 'active' if checker_scheduled.should_be_dark() else 'inactive')

    def test_dark_mode_detection_follow_sun(self):
        config.update('mode', Modes.followSun.value)
        checker = Checker(Modes.followSun.value)
        time_current: int = int(datetime.today().timestamp())
        time_light_unix, time_dark_unix = communicate.send_config('firefox')['times']

        should_be_dark_extension = time_dark_unix <= time_current < time_light_unix
        self.assertEqual(checker.should_be_dark(), should_be_dark_extension,
                         'Dark mode detection should be correct')


if __name__ == '__main__':
    unittest.main()
