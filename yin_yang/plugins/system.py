from yin_yang.plugins.plugin import Plugin, PluginDesktopDependent
import subprocess
import pwd
import os


class System(PluginDesktopDependent):
    name = 'System'

    def set_strategy(self, strategy):
        if strategy == 'kde':
            self.strategy = Kde()
        elif strategy == 'gtk':
            self.strategy = Gnome()

    @property
    def theme_dark(self):
        if hasattr(self, 'strategy'):
            # needed since the plugin class checks if the themes are set correctly
            # in it's init
            return self.strategy.theme_dark
        else:
            return ''

    @theme_dark.setter
    def theme_dark(self, theme: str):
        self.strategy.theme_dark = theme

    @property
    def theme_bright(self):
        if hasattr(self, 'strategy'):
            return self.strategy.theme_bright
        else:
            return ''

    @theme_bright.setter
    def theme_bright(self, theme: str):
        self.strategy.theme_bright = theme

    def get_themes_available(self) -> dict[str, str]:
        return self.strategy.get_themes_available()


# WIP: Potential Check for https://gist.github.com/atiensivu/fcc3183e9a6fd74ec1a283e3b9ad05f0
# to reduce common issues, or write it in the FAQ
class Gnome(Plugin):
    name = 'Gnome'
    # TODO set the default theme for gnome
    theme_dark = ''
    theme_bright = ''

    def set_theme(self, theme: str):
        # Shell theme
        # noinspection SpellCheckingInspection
        subprocess.run(["gsettings", "set", "org.gnome.shell.extensions.user-theme", "name",
                        '"{}"'.format(theme)])


translations = {}


class Kde(Plugin):
    name = 'KDE'
    # noinspection SpellCheckingInspection
    theme_bright = 'org.kde.breeze.desktop'
    # noinspection SpellCheckingInspection
    theme_dark = 'org.kde.breezedark.desktop'

    def get_themes_available(self) -> dict[str, str]:
        return get_kde_theme_names()

    def set_theme(self, theme: str):
        # uses a kde api to switch to a light theme
        # noinspection SpellCheckingInspection
        subprocess.run(["lookandfeeltool", "-a", theme])


def get_short_name(file) -> str:
    """Searches for the long_name in the file and maps it to the found short name"""

    for line in file:
        if 'Name=' in line:
            name: str = ''
            write: bool = False
            for letter in line:
                if letter == '\n':
                    write = False
                if write:
                    name += letter
                if letter == '=':
                    write = True
            return name


def get_kde_theme_names():
    """
    Returns a name_map with translations for kde theme names.
    """

    global translations

    if translations != {}:
        return translations

    # aliases for path to use later on
    user = pwd.getpwuid(os.getuid())[0]
    path = "/home/" + user + "/.local/share/plasma/look-and-feel/"

    # asks the system what themes are available
    # noinspection SpellCheckingInspection
    long_names = subprocess.check_output(["lookandfeeltool", "-l"], universal_newlines=True)
    long_names = long_names.splitlines()
    long_names.sort()

    # get the actual name
    for long_name in long_names:
        # trying to get the Desktop file
        try:
            # load the name from the metadata.desktop file
            with open('/usr/share/plasma/look-and-feel/{long_name}/metadata.desktop'.format(**locals()), 'r') as file:
                translations[long_name] = get_short_name(file)
        except OSError:
            # check the next path if the themes exist there
            try:
                # load the name from the metadata.desktop file
                with open('{path}{long_name}/metadata.desktop'.format(**locals()), 'r') as file:
                    # search for the name
                    translations[long_name] = get_short_name(file)
            except OSError:
                # if no file exist lets just use the long name
                translations[long_name] = long_name

    return translations
