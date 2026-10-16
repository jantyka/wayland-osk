"""Reads the configuration shared by wayland-osk and wayland-osk-listener.

The file is ~/.config/wayland-osk/config.ini (or $XDG_CONFIG_HOME/wayland-osk/config.ini).
Every setting has a default, so the file is optional. See config.example.ini.
"""
import configparser
import os
import re

DEFAULTS = {
    'keyboard': {
        'layout': 'de',
    },
    'trigger': {
        'button': 'BTN_MIDDLE',
        'device': '',
    },
    'style': {
        'font': '',
        'font_size': '13',
        'background': '#232629',
        'key': '#31363b',
        'text': '#eff0f1',
        'border': '#4d4d4d',
        'hover': '#3daee9',
        'hover_text': '#ffffff',
        'active': '#1d99f3',
        'active_text': '#ffffff',
    },
}

# A comment after a value. The marker needs whitespace after it, because '#' also starts
# a colour code.
INLINE_COMMENT = re.compile(r'(?:^|\s+)[#;](?:\s|$)')


def config_path():
    base = os.environ.get('XDG_CONFIG_HOME') or os.path.expanduser('~/.config')
    return os.path.join(base, 'wayland-osk', 'config.ini')


def load():
    """Returns the settings as a dict of sections, defaults filled in."""
    parser = configparser.ConfigParser()
    parser.read_dict(DEFAULTS)
    parser.read(config_path(), encoding='utf-8')
    return {section: {key: INLINE_COMMENT.split(value, maxsplit=1)[0].strip()
                      for key, value in parser[section].items()}
            for section in DEFAULTS}
