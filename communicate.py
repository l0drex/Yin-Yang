#!/usr/bin/env python

# This file enables the extension to communicate with yin-yang.
import logging
import sys
import json
import struct
import time
from datetime import date, datetime, time as datetimetime
from pathlib import Path

from yin_yang import checker
from yin_yang.config import config, Modes

logging.basicConfig(filename=str(Path.home()) + '/.local/share/yin_yang.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s - %(name)s: %(message)s')
logger = logging.getLogger(__name__)


def parse_time(time_str: str) -> int:
    today = date.today()
    tm = datetimetime.fromisoformat(time_str)
    unix_time: float = time.mktime(datetime.combine(today, tm).timetuple())

    if unix_time < time.time():
        unix_time += 60*60*24

    return int(unix_time)


def send_config(plugin: str) -> dict:
    logger.debug('Building message')

    enabled = config.get('enabled', plugin)
    message = {
        'enabled': enabled,
        'dark_mode': config.get('dark_mode')
    }

    if enabled:
        mode = config.get("mode")
        message['scheduled'] = mode != Modes.manual.value
        message['themes'] = [
            config.get("light_theme", "firefox"),
            config.get("dark_theme", "firefox")
        ]
        if mode != Modes.manual.value:
            if mode == Modes.scheduled.value:
                times = [
                    parse_time(config.get("switch_To_Light")),
                    parse_time(config.get("switch_To_Dark"))
                ]
            elif mode == Modes.followSun.value:
                time_light, time_dark = checker.get_sun_time()
                times = [
                    parse_time(time_light.strftime('%H:%M')),
                    parse_time(time_dark.strftime('%H:%M'))
                ]
            message['times'] = times

    return message


def encode_message(message_content: dict) -> dict[str, bytes]:
    """
    Encode a message for transmission, given its content.
    :param message_content: a message
    """
    encoded_content = json.dumps(message_content).encode("utf-8")
    encoded_length = struct.pack('=I', len(encoded_content))
    # use struct.pack("10s", bytes)
    # to pack a string of the length of 10 characters

    encoded_message = {
        'length': encoded_length,
        'content': struct.pack(str(len(encoded_content)) + "s",
                               encoded_content)}
    logger.debug('Encoded message with length ' + str(len(encoded_content)))
    return encoded_message


# Send an encoded message to stdout.
def send_message(encoded_message: dict[str, bytes]):
    """
    Send a message.
    :param encoded_message: message as json
    """
    logger.debug('Sending message')
    sys.stdout.buffer.write(encoded_message['length'])
    sys.stdout.buffer.write(encoded_message['content'])
    sys.stdout.buffer.flush()


# Read a message from stdin and decode it.
def decode_message():
    raw_length = sys.stdin.buffer.read(4)

    if not raw_length:
        sys.exit(0)
    message_length = struct.unpack('=I', raw_length)[0]
    message = sys.stdin.buffer.read(message_length).decode("utf-8")

    return json.loads(message)


if __name__ == '__main__':
    while True:
        try:
            message_received: dict = decode_message()
            if message_received is not None:
                logger.debug('Message received from ' + message_received['name'])

            if message_received['name'] == 'Firefox':
                send_message(encode_message(send_config('firefox')))
        except Exception as e:
            logger.error(e)
