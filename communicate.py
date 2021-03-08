#!/usr/bin/env python

# This file enables the extension to communicate with yin-yang.
import logging
import sys
import json
import struct
import time
from datetime import date
from pathlib import Path

from yin_yang.config import config, Modes

logging.basicConfig(filename=str(Path.home()) + '/.local/share/yin_yang.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s - %(name)s: %(message)s')
logger = logging.getLogger(__name__)


def parse_time(time_str: str) -> float:
    dt = date.fromisoformat(time_str)
    return time.mktime(dt.timetuple())


def create_message() -> dict:
    logger.debug('Building message')

    enabled = config.get('enabled', 'firefox')
    message = {'enabled': enabled}
    if enabled:
        scheduled = config.get("mode") != Modes.manual.value
        message['scheduled'] = scheduled
        message['themes'] = [
            config.get("light_theme", "firefox"),
            config.get("dark_theme", "firefox")
        ]
        if scheduled:
            times = [
                parse_time(config.get("switch_To_Light")),
                parse_time(config.get("switch_To_Dark"))
            ]
            message['times'] = times
        else:
            message['dark_mode'] = config.get('dark_mode')

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
def get_message():
    raw_length = sys.stdin.buffer.read(4)

    if not raw_length:
        sys.exit(0)
    message_length = struct.unpack('=I', raw_length)[0]
    message = sys.stdin.buffer.read(message_length).decode("utf-8")

    return json.loads(message)


while True:
    message_received = get_message()
    if message_received is not None:
        logger.debug('Message received: ' + message_received)

    if message_received == 'GetSettings':
        send_message(encode_message(create_message()))
