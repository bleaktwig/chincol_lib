# No preamble _on purpose_. This should be ran with the python version in your
#     virtual environment!

# Colors in the F2 palette.
COLORS = [
#     name          #     strong     weak.
    (("scarlet",     0), ("#CD2E26", "#E9635C")),
    (("magenta",     1), ("#B5293D", "#D95C6D")),
    (("lilac",       2), ("#A22969", "#C45D94")),
    (("purple",      3), ("#942B7B", "#AE5F9B")),
    (("lavender",    4), ("#8E3388", "#A86BA4")),
    (("violet",      5), ("#623B86", "#927DA5")),
    (("indigo",      6), ("#364A8B", "#7783AA")),
    (("blue",        7), ("#315E90", "#7893B3")),
    (("teal",        8), ("#2B6581", "#5E8599")),
    (("cyan",        9), ("#257263", "#529285")),
    (("mint",       10), ("#257C55", "#55997A")),
    (("green",      11), ("#258147", "#559E6F")),
    (("fern",       12), ("#429346", "#74B277")),
    (("chartreuse", 13), ("#6FB43F", "#9AD272")),
    (("lemon",      14), ("#98C02E", "#C1E560")),
    (("yellow",     15), ("#E0CA28", "#F9E866")),
    (("gold",       16), ("#EDBE25", "#FBD869")),
    (("amber",      17), ("#F0AE28", "#FCCD6D")),
    (("saffron",    18), ("#F39730", "#FDBB71")),
    (("orange",     19), ("#F68A32", "#FFB374")),
    (("tangerine",  20), ("#F07D2C", "#FDAB71")),
    (("vermilion",  21), ("#EB6127", "#FB976E")),
    (("crimson",    22), ("#E44A25", "#F98266")),
    (("red",        23), ("#DC4022", "#F77B65"))
]

class f2_palette:
    """
    Class for the feshtone2 palette. This simply is a dictionary where the items
    can be accessed with two keys, a string with the color name or an integer.
    """
    def __init__(self):
        """Setup the palette from COLORS."""
        self.dict_str: dict[str, tuple[str]] = {}
        self.dict_int: dict[int, tuple[str]] = {}

        for color in COLORS:
            self.dict_str[color[0][0]] = color[1]
            self.dict_int[color[0][1]] = color[1]

    def __getitem__(self, key: str | int) -> tuple[str]:
        """Get an item either with an integer or a string."""
        try:
            if isinstance(key, str): return self.dict_str[key]
            if isinstance(key, int): return self.dict_int[key]
        except ValueError:
            raise ValueError("Key " + key + " not found.")
        raise ValueError("Key should be either a string or an integer.")

    def keys(self) -> list[int]:
        """Get a list of keys in integer form."""
        return self.dict_int.keys()

    def values(self) -> list[tuple[str]]:
        """Get a list of values."""
        return self.dict_int.values()
