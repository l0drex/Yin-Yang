import subprocess
from yin_yang.plugins.plugin import Plugin


class Notification(Plugin):
    name = 'Notification'
    theme_bright = 'Day'
    theme_dark = 'Night'

    def set_theme(self, theme: str):
        # TODO set an icon
        subprocess.run(['notify-send', f'Set the theme to {theme}', '-a', 'Yin & Yang', '-u', 'low'])

    @property
    def available(self) -> bool:
        try:
            return subprocess.run(['notify-send', '--help']).returncode == 0
        except FileNotFoundError:
            return False
