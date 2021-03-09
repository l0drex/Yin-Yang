import json
import struct
import sys
import unittest
from datetime import datetime
from subprocess import Popen, PIPE

import communicate


class CommunicationTest(unittest.TestCase):
    def test_parse_time(self):
        response = communicate.parse_time('07:00')

        self.assertIsInstance(response, int)
        date = datetime.fromtimestamp(response)
        self.assertEqual(date.strftime('%H:%M'), '07:00')

        now: int = int(datetime.now().timestamp())
        self.assertTrue(response > now,
                        'Time should always be in the future')
        self.assertTrue(communicate.parse_time(datetime.today().strftime('%H:%M')) > now,
                        'Time should always be in the future')

    def test_message_build(self):
        message = communicate.create_message()
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
                self.assertTrue(time_light > datetime.now().timestamp())
                self.assertTrue(time_dark > datetime.now().timestamp())

    def test_encode_decode(self):
        message = communicate.create_message()

        process = Popen([sys.executable, '../communicate.py'],
                        stdin=PIPE, stdout=PIPE)

        # build call
        call = 'GetSettings'
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
        response_decoded = response[4 : (response_length + 4)].decode('utf-8')
        response_decoded = json.loads(response_decoded)

        # test if correct
        self.assertEqual(message, response_decoded,
                         'Returned message should be equal to the message')


if __name__ == '__main__':
    unittest.main()
