"""Reads the configuration shared by wayland-osk and wayland-osk-listener.

The file is ~/.config/wayland-osk/config.ini (or $XDG_CONFIG_HOME/wayland-osk/config.ini).
Every setting has a default, so the file is optional. See config.example.ini.
"""
import configparser
import os

DEFAULTS = {
    'keyboard': {
        'layout': 'de',
    },
    'trigger': {
        'button': 'BTN_MIDDLE',
        'device': '',
    },
}


def config_path():
    base = os.environ.get('XDG_CONFIG_HOME') or os.path.expanduser('~/.config')
    return os.path.join(base, 'wayland-osk', 'config.ini')


def load():
    """Returns the settings as a dict of sections, defaults filled in."""
    parser = configparser.ConfigParser(inline_comment_prefixes=('#', ';'))
    parser.read_dict(DEFAULTS)
    parser.read(config_path(), encoding='utf-8')
    return {section: dict(parser[section]) for section in DEFAULTS}
