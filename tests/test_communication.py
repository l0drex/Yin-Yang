import json
import struct
import sys
import unittest
from datetime import datetime, time
from subprocess import Popen, PIPE

import communicate
from yin_yang.config import config, Modes
from yin_yang.yin_yang import should_be_dark


class CommunicationTest(unittest.TestCase):
    def setUp(self):
        config.set_default()
        config.update('firefox', 'enabled', True)

    def test_move_time(self):
        time_light = time.fromisoformat('07:00')
        time_dark = time.fromisoformat('20:00')

        times = [
            # morning
            datetime.strptime('03:00', '%H:%M'),
            # day
            datetime.strptime('12:00', '%H:%M'),
            # night
            datetime.strptime('22:00', '%H:%M')
        ]

        for time_current in times:
            time_current_str = time_current.strftime('%H:%M')
            with self.subTest('Current time should always be between dark and light',
                              time_current=time_current_str):
                time_current_unix = time_current.timestamp()
                time_light_unix, time_dark_unix = communicate.move_times(time_current, time_light, time_dark)
                self.assertIsInstance(time_light_unix, int)
                self.assertIsInstance(time_dark_unix, int)
                self.assertTrue(time_light_unix <= time_current_unix <= time_dark_unix or
                                time_dark_unix <= time_current_unix <= time_light_unix)

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
        config.load()

        process = Popen([sys.executable, '../communicate.py'],
                        stdin=PIPE, stdout=PIPE)
        calls = ['firefox']

        for call in calls:
            # build call
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
            message_expected = communicate.send_config(call)
            self.assertEqual(message_expected, response_decoded,
                             'Returned message should be equal to the message')

    def test_dark_mode_detection_scheduled(self):
        time_light = time.fromisoformat('07:00')
        time_dark = time.fromisoformat('20:00')

        times = [
            # morning
            datetime.strptime('03:00', '%H:%M'),
            # day
            datetime.strptime('12:00', '%H:%M'),
            # night
            datetime.strptime('22:00', '%H:%M')
        ]

        for time_current in times:
            time_current_str = time_current.strftime('%H:%M')
            with self.subTest('Dark mode should be decided correctly.',
                              time_current=time_current_str):
                # get unix times
                time_light_unix, time_dark_unix = communicate.move_times(time_current, time_light, time_dark)

                is_dark = should_be_dark(time_current.time(), time_light, time_dark)
                # NOTE: this should be equal to how the extension calculates the theme
                detected_dark = time_dark_unix <= time_current.timestamp() < time_light_unix

                self.assertEqual(is_dark, detected_dark,
                                 f'Dark mode should be {"active" if is_dark else "inactive"} at {time_current_str}')

    def test_dark_mode_detection_follow_sun(self):
        config.mode = Modes.followSun
        time_current: datetime = datetime.today()
        time_light, time_dark = config.times
        time_light_unix, time_dark_unix = communicate.move_times(time_current, time_light, time_dark)
        time_current_unix: int = int(time_current.timestamp())

        is_dark = should_be_dark(time_current.time(), time_light, time_dark)
        # NOTE: this should be equal to how the extension calculates the theme
        detected_dark = time_dark_unix <= time_current_unix < time_light_unix
        self.assertEqual(is_dark, detected_dark,
                         'Dark mode detection should be correct')


if __name__ == '__main__':
    unittest.main()
