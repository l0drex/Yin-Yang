#!/usr/bin/env python

# This file allows external extensions to communicate with yin-yang.
# It's based on https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/Native_messaging,
# as it was originally used for the firefox plugin only

import logging
import sys
import json
import struct
import time
from datetime import date, datetime, time as datetimetime
from pathlib import Path

from yin_yang.config import config, Modes

logging.basicConfig(filename=str(Path.home()) + '/.local/share/yin_yang.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s - %(name)s: %(message)s')
logger = logging.getLogger(__name__)


def parse_time(time_str: str) -> int:
    """
    Converts a time string to seconds since the epoch
    :param time_str: a time string formatted as %H:%M
    """
    today = date.today()
    tm = datetimetime.fromisoformat(time_str)
    unix_time: float = time.mktime(datetime.combine(today, tm).timetuple())

    return int(unix_time)


def send_config(plugin: str) -> dict:
    """
    Returns the configuration for the plugin plus some general necessary stuff (scheduled, dark_mode, times)
    :param plugin: the plugin for which the configuration should be returned
    :return: a dictionary containing config information
    """
    logger.debug('Building message')

    enabled = config.get('enabled', plugin)
    message = {
        'enabled': enabled,
        'dark_mode': config.dark_mode
    }

    if enabled:
        mode = config.mode
        message['scheduled'] = mode != Modes.manual.value
        message['themes'] = [
            config.get("light_theme", plugin),
            config.get("dark_theme", plugin)
        ]
        if mode != Modes.manual.value:
            times = [parse_time(tm.strftime('%H:%M')) for tm in config.times]

            # move times so that one of them is always in the future
            time_now = datetime.today().timestamp()
            one_day = 60 * 60 * 24
            if time_now < times[0] and time_now < times[1]:
                times[1] -= one_day
            elif times[0] < time_now and times[1] < time_now:
                times[0] += one_day

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
    """
    Decodes a message in stdout and returns it.
    """
    raw_length = sys.stdin.buffer.read(4)

    if not raw_length:
        sys.exit(0)
    message_length = struct.unpack('=I', raw_length)[0]
    message = sys.stdin.buffer.read(message_length).decode("utf-8")

    return json.loads(message)


if __name__ == '__main__':
    while True:
        try:
            message_received: str = decode_message()
            if message_received is not None:
                logger.debug('Message received from ' + message_received)

            if message_received == 'firefox':
                send_message(encode_message(send_config('firefox')))
        except Exception as e:
            logger.error(e)
