# Contributing

If you want to write code that changes the theme of an application,
you have two possible ways to do so:

1. `plugin.py` for running commands or changing values in config files.
2. `communicate.py` for communication from another application.


## Plugins

Plugins provide a way to directly change the theme by running commands or
changing a value in a config file.

Each plugin is a class in `yin_yang/plugins` and extends `plugin.py`.
Write your code to set any theme by overwriting the `set_theme()` function.


### Default themes

If you want to provide default values for light and darkt themes,
you can set the class attributes `theme_light` and `theme_dark`.


### Configuration

Every plugin has its own section in the application's config file.
It consists of the following options:
- `enabled`: If the plugin is enabled or not
- `light_theme`: The theme that should be used in light mode
- `dark_theme`: The theme that should be used in dark mode

If you need to store more information, you should have a look at `yin_yang/config.py`.


### GUI

By default, each plugin has its own section in the tab plugins,
with one simple text input to set the desired theme.

If you want to provide a combobox instead, you can simply override the `get_available_themes()` function.


## Communication

If you need to update the theme with an extension of your program, you can call `communicate.py`.
Currently, it might be pretty outdated since the only plugin that needed this was removed.


# What needs to be done?

- [ ] Separate the gui for configuration from the daemon,
      so that the command line tool doesn't run endlessly in after exiting the gui
- [ ] Optimize the building process to include
  - creating `yin_yang/ui/mainwindow.py` from `design/mainwindow.ui`
  - creating `yin_yang/ui/resources_rc.py` from `resources.qrc`
- [ ] optimize `scripts/install.sh` and `uninstall.sh`
- [ ] optimize installation process
- [ ] add an option to only change the theme when pc is awakening from suspend
- [ ] add an option to automatically update the location
