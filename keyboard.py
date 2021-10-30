import math


class Keyboard:
    KEYS = [
        ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", "backspace"],
        ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "[", "]", "\\"],
        ["a", "s", "d", "f", "g", "h", "j", "k", "l", ";", "'"],
        ["z", "x", "c", "v", "b", "n", "m", ",", ".", "/"],
        [" "],
    ]

    SHIFT_KEYS = {
        "{": "[",
        "}": "]",
        ":": ";",
        "\"": "'",
        "<": ",",
        ">": ".",
        "?": "/",
        "!": "1",
        "@": "2",
        "#": "3",
        "$": "4",
        "%": "5",
        "^": "6",
        "&": "7",
        "*": "8",
        "(": "9",
        ")": "0",
        "_": "-",
        "+": "=",
    }

    KEYS_DIST = 18  # units: mm
    ROW_OFFSETS = [-10, 0, 5, 15, 69]  # units: mm

    @staticmethod
    def calc_key_coordinates():
        key_coordinates = {}
        for i in range(0, len(Keyboard.KEYS)):
            horizontal_offset = Keyboard.ROW_OFFSETS[i]
            vertical_offset = i * Keyboard.KEYS_DIST

            for key in Keyboard.KEYS[i]:
                key_coordinates[key] = (horizontal_offset, vertical_offset)
                horizontal_offset += Keyboard.KEYS_DIST

        z_coords = key_coordinates["z"]
        left_shift = (z_coords[0]  - Keyboard.KEYS_DIST, z_coords[1])
        key_coordinates["left_shift"] = left_shift

        slash_coords = key_coordinates["/"]
        right_shift = (slash_coords[0] + Keyboard.KEYS_DIST, slash_coords[1])
        key_coordinates["right_shift"] = right_shift

        backslash_coords = key_coordinates["\\"]
        backspace_coords = (backslash_coords[0], backslash_coords[1] - Keyboard.KEYS_DIST)
        key_coordinates["backspace"] = backspace_coords

        return key_coordinates

    @staticmethod
    def should_press_shift(key):
        return key in Keyboard.SHIFT_KEYS or key.isupper()

    def __init__(self):
        self.key_coords = Keyboard.calc_key_coordinates()

    def get_keyboard_key(self, key):
        # Maps special keys back to keys in self.key_coords and KEY_TO_FINGER_MAP
        if key in self.key_coords:
            return key

        if key in Keyboard.SHIFT_KEYS:
            return Keyboard.SHIFT_KEYS[key]

        return key.lower()

    def get_distance_between_keys(self, key1, key2):
        # k1 = self.get_keyboard_key(key1)
        # k2 = self.get_keyboard_key(key2)

        coords_1 = self.key_coords[key1]
        coords_2 = self.key_coords[key2]

        return math.sqrt(math.pow(coords_1[0] - coords_2[0], 2) + math.pow(coords_1[1] - coords_2[1], 2))
