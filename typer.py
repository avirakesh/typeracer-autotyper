from keyboard import Keyboard
from random import random
from time import sleep


class Typer:
    _SPEED_SCALE = 2.5

    _FINGER_SPEED_RAW = 1000/150  # units: ms/mm
    _FINGER_STATIC_DELAY_RAW = 110  # units: ms

    _FINGER_SPEED = _FINGER_SPEED_RAW / _SPEED_SCALE
    _FINGER_STATIC_DELAY = _FINGER_STATIC_DELAY_RAW / _SPEED_SCALE

    _JITTER_RANGE = 3  # units: ms

    FINGER_TO_KEY_MAP = {
        "LEFT_PINKY": ["1", "q", "a", "z", "left_shift"],
        "LEFT_RING": ["2", "w", "s", "x"],
        "LEFT_MIDDLE": ["3", "e", "d", "c"],
        "LEFT_INDEX": ["4", "5", "r", "t", "f", "g", "v", "b"],
        "RIGHT_INDEX": ["6", "7", "y", "u", "h", "j", "n", "m"],
        "RIGHT_MIDDLE": ["8", "i", "k", ","],
        "RIGHT_RING": ["9", "o", "l", "."],
        "RIGHT_PINKY": ["0", "-", "=", "p", "[", "]", "\\", ";", "'", "/", "backspace", "right_shift"],
        "THUMB": [" "],
    }

    KEY_TO_FINGER_MAP = {key: finger for (finger, keys) in FINGER_TO_KEY_MAP.items() for key in keys}

    def __init__(self, speed_mult = 1):
        self.keyboard = Keyboard()
        self.finger_positions = {
            "LEFT_PINKY": "a",
            "LEFT_RING": "s",
            "LEFT_MIDDLE": "d",
            "LEFT_INDEX": "f",
            "RIGHT_INDEX": "j",
            "RIGHT_MIDDLE": "k",
            "RIGHT_RING": "l",
            "RIGHT_PINKY": ";",
            "THUMB": " ",
        }

        self.speed_mult = speed_mult

    def _finger_for_key(self, key):
        return Typer.KEY_TO_FINGER_MAP[self.keyboard.get_keyboard_key(key)]

    def _current_finger_position(self, finger):
        return self.finger_positions[finger]

    def _get_new_finger_positions(self, new_key):
        should_press_shift = self.keyboard.should_press_shift(new_key)
        physical_keyboard_key = self.keyboard.get_keyboard_key(new_key)

        key_finger = self._finger_for_key(physical_keyboard_key)
        new_positions = {
            key_finger: physical_keyboard_key
        }

        if not should_press_shift:
            return new_positions

        (shift_finger, shift_key) = ("LEFT_PINKY", "left_shift") \
            if key_finger.startswith("RIGHT_") else ("RIGHT_PINKY", "right_shift")

        new_positions[shift_finger] = shift_key
        return new_positions

    def _move_fingers_to_positions(self, new_positions):
        for (finger, key) in new_positions.items():
            self.finger_positions[finger] = key

    @staticmethod
    def _typing_jitter():
        # returns a random floating point number in range [-_JITTER_RANGE / 2, _JITTER_RANGE / 2)
        return (random() * Typer._JITTER_RANGE) - (Typer._JITTER_RANGE / 2)

    def simulate_typing_key_with_delay(self, key):
        # returns after waiting for appropriate time to type key.
        # Does not do actual keyboard input

        new_positions = self._get_new_finger_positions(key)

        delay = 0  # unit: ms
        for (finger, new_key) in new_positions.items():
            current_key = self._current_finger_position(finger)
            delay_for_key = 0  # units: ms
            if current_key == new_key:
                delay_for_key = Typer._FINGER_STATIC_DELAY
            else:
                key_distance = self.keyboard.get_distance_between_keys(current_key, new_key)
                delay_for_key = key_distance * Typer._FINGER_SPEED
            delay = max(delay, delay_for_key)  # take the max delay of moving all fingers to their new positions

        jitter_time_ms = self._typing_jitter()

        time_to_wait_s = (delay + jitter_time_ms) / 1000
        sleep(time_to_wait_s / self.speed_mult)
        self._move_fingers_to_positions(new_positions)
