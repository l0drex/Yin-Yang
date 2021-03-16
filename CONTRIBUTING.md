# Changing the theme in your application

If you want to write code that changes the theme of an application,
you have two possible ways to do so:

1. Develop a [plugin](#Plugins) for running commands or changing values in config files.
2. [Communicate](#Communication) from an external application.


## Plugins

Plugins provide a way to directly change the theme by running commands or
changing a value in a config file.

Each plugin is a class in `yin_yang/plugins` and extends `plugin.py`.
Write your code to set any theme by overwriting the `set_theme()` function.


### Default themes

If you want to provide default values for light and dark themes,
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

If you want to provide a combobox instead, you can simply implement the `get_available_themes()` function.


### Testing

Testing plugins currently only checks that none of the enabled plugins `set_theme` functions
result in an error.
To test your plugin you have to:
1. Enable it (via UI or the config file stored in `~/.config/yin-yang/yin-yang.json`).
2. Run `tests/test_plugins.py`.


## Communication

If you need to update the theme from an external application, you can do the following:

1. Write a plugin as described in _Plugins_ without implementing the `set_theme` function.
   This will create a section for your application in the config file.
1. Call `communicate.py` as a process from your application.
2. Write your application name into stdin of that process.
3. Read the response from stdout. It should be a json object with the following data:
```json
{
  "enabled": true,
  "dark_mode": true,
  "scheduled": true,
  "themes": ["light_theme", "dark_theme"],
  "times": [1615881600, 1615924800]
} 
```
- `enabled` is true if your plugin is enabled.
  If not, the response only contains `enabled` and `dark_mode`
- `dark_mode` is true if the system is currently using a dark theme
- `scheduled` is true if the theme changes automatically.
  If not, the response does not contain the times section.
- `themes` is a list of the preferred themes a strings.
- `times` is a list of the times when the theme changes.
  These are unix times in seconds since the epoch and always "surround" the current time.
  This enables your external application to calculate the preferred theme directly and
  compare it to `dark_mode` if you want.
  > For example, the times provided above would be the times when called on `2021-03-16 13:31:05`.