from typing import Optional


class Plugin:
    name = ''
    # default themes
    theme_dark = None
    theme_bright = None
    enabled: bool = False

    def __init__(self, enabled: bool, theme_dark: Optional[str], theme_bright: Optional[str]):
        # check default values
        if self.theme_dark is None or self.theme_bright is None:
            raise ValueError('Default value for theme is not set!')

        # set the themes
        if theme_dark is not None and theme_dark != self.theme_dark:
            self.theme_dark = theme_dark
        if theme_bright is not None and theme_bright != self.theme_bright:
            self.theme_bright = theme_bright

        self.enabled = enabled

    def set_mode(self, dark: bool):
        """Set the theme"""
        if dark:
            self.set_theme(self.theme_dark)
        else:
            self.set_theme(self.theme_bright)

    def set_theme(self, theme: str):
        """Set a specific theme"""
        raise NotImplementedError('Function set_theme has not been implemented!')
