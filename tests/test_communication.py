import unittest
from datetime import datetime

import communicate
from yin_yang.config import config


class MyTestCase(unittest.TestCase):
    def test_parse_time(self):
        self.assertIsInstance(communicate.parse_time('07:00'), float)
        response = communicate.parse_time('07:00')
        date = datetime.fromtimestamp(response)
        self.assertEqual(date.strftime('%H:%M'), '07:00')

    def test_message_build(self):
        message = communicate.create_message()
        self.assertNotEqual(message, None,
                            'Message should not be empty')
        self.assertNotEqual(message, {},
                            'Message should not be empty')


if __name__ == '__main__':
    unittest.main()
