#!/usr/bin/env python

# This file enables the extension to communicate with yin-yang.
import logging
import sys
import json
import struct
from pathlib import Path

from yin_yang.config import config, Modes

logging.basicConfig(filename=str(Path.home()) + '/.local/share/yin_yang.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s - %(name)s: %(message)s')
logger = logging.getLogger(__name__)


def parse_time(time: str) -> tuple[int, int]:
    hour = int(time.split(":")[0])
    minute = int(time.split(":")[1])
    return hour, minute


def create_message() -> dict:
    logger.debug('Building message')
    theme_light = config.get("light_theme", "firefox")
    theme_dark = config.get("dark_theme", "firefox")
    theme_active: str = theme_dark if config.get('dark_mode') else theme_light
    message = {
        'schedule': config.get("mode") != Modes.manual.value,
        'theme_dark': theme_dark,
        'theme_light': theme_light,
        'theme_active': theme_active,
        'time_day': parse_time(config.get("switch_To_Light")),
        'time_night': parse_time(config.get("switch_To_Dark"))
    }

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
