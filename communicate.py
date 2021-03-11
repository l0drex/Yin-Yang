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


def move_times(time_now: datetime, time_light: datetimetime, time_dark: datetimetime) -> list[int, int]:
    """
    Converts a time string to seconds since the epoch
    :param time_now: the current time
    :param time_light: the time when light mode starts
    :param time_dark: the time when dark mode starts
    """

    # convert all times to unix times
    time_now_unix: int = int(time_now.timestamp())
    time_light_unix: int = int(time.mktime(
        datetime.combine(time_now.date(), time_light).timetuple()))
    time_dark_unix: int = int(time.mktime(
        datetime.combine(time_now.date(), time_dark).timetuple()))

    # move times so that one of them is always in the future
    one_day = 60 * 60 * 24
    if time_now_unix < time_light_unix and time_now_unix < time_dark_unix:
        time_dark_unix -= one_day
    elif time_light_unix < time_now_unix and time_dark_unix < time_now_unix:
        time_light_unix += one_day

    return [time_light_unix, time_dark_unix]


def send_config(plugin: str) -> dict:
    """
    Returns the configuration for the plugin plus some general necessary stuff (scheduled, dark_mode, times)
    :param plugin: the plugin for which the configuration should be returned
    :return: a dictionary containing config information
    """
    logger.debug('Building message')

    enabled = config.get(plugin, 'enabled')
    message = {
        'enabled': enabled,
        'dark_mode': config.dark_mode
    }

    if enabled:
        mode = config.mode
        message['scheduled'] = mode != Modes.manual
        message['themes'] = [
            config.get(plugin, "light_theme"),
            config.get(plugin, "dark_theme")
        ]
        if mode != Modes.manual:
            time_light, time_dark = config.times
            time_now = datetime.now()

            message['times'] = move_times(time_now, time_light, time_dark)

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
