def get_help_colors_dict(use_colors, help_headers_color, help_options_color):
    if not use_colors:
        return {}

    d = {
        "help_headers_color": help_headers_color,
        "help_options_color": help_options_color,
    }
    return d
