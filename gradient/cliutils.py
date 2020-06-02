import curses
import json
import shutil

import requests
import six

from gradient import exceptions


def get_terminal_lines(fallback=48):
    if six.PY3:
        return shutil.get_terminal_size().lines

    return fallback


def print_json_pretty(res):
    print(json.dumps(res, indent=2, sort_keys=True))


def response_error_check(res):
    if ('error' not in res
            and 'status' in res
            and (res['status'] < 200 or res['status'] > 299)):
        res['error'] = True
    return res


def requests_exception_to_error_obj(e):
    return {'error': True, 'message': str(e)}


def status_code_to_error_obj(status_code):
    message = 'unknown'
    if status_code in requests.status_codes._codes:
        message = requests.status_codes._codes[status_code][0]
    return {'error': True, 'message': message, 'status': status_code}


def validate_auth_options(kwargs):
    if kwargs["generate_auth"] and any((kwargs["auth_username"], kwargs["auth_password"])):
        raise exceptions.ApplicationError("Use either --authUsername and --authPassword options or --auth flag")

    # checking if both or none auth options were used
    if len([val for val in (kwargs["auth_username"], kwargs["auth_password"]) if val is not None]) == 1:
        raise exceptions.ApplicationError("--authUsername and --authPassword have to be used together")


def none_strings_to_none_objects(lst):
    return [elem if elem != "none" else None for elem in lst]


class TerminalPrinter(object):
    def __init__(self):
        self.screen_writer = None

    def init(self):
        self.screen_writer = curses.initscr()
        return self

    def cleanup(self):
        """Cleanup before program ends or terminal may stop working correlctly"""
        curses.nocbreak()
        self.screen_writer.keypad(False)
        curses.echo()
        curses.endwin()

    def rewrite_screen(self, s):
        self.clear()
        self.add_line(s)
        self.refresh()

    def add_line(self, s):
        self.add_str(s + "\n")

    def add_str(self, s):
        self.screen_writer.addstr(s)

    def refresh(self):
        self.screen_writer.refresh()

    def clear(self):
        self.screen_writer.clear()
