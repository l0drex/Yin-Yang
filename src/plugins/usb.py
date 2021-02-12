from src.plugins.plugin import Plugin


class Usb(Plugin):
    name = 'USB'
    theme_dark = ''
    theme_bright = ''

    def set_theme(self, theme: str):
        # TODO
        pass

    def get_input(self, widget):
        # TODO implement check boxes

        return super(Usb, self).get_input(widget)
