"""
easy meter logic
"""
import time
from typing import List, Annotated

from meters.meter import Meter


class Easy(Meter):
    """
    easy meter logic and config
    """
    _pause_seconds = 0.7
    _quick_pause_seconds = 0.5
    _transition_seconds = 4
    _short_seconds = 2
    _long_seconds = 6
    _last_cmd_time = time.time()
    _menu_timeout_seconds = 120

    def _short_pulse(self, quick: bool = False):
        """ send short pulse """
        self._gpio.set_gpio(1)
        if quick:
            time.sleep(self._quick_pause_seconds)
        else:
            time.sleep(self._short_seconds)
        self._gpio.set_gpio(0)
        self._last_cmd_time = time.time()

    def _long_pulse(self):
        """ send long pulse """
        self._gpio.set_gpio(1)
        time.sleep(self._long_seconds)
        self._gpio.set_gpio(0)
        self._last_cmd_time = time.time()

    def _transition(self):
        """ wait for the meter to transition to the next input field """
        self._gpio.set_gpio(0)
        time.sleep(self._transition_seconds)

    def _pause(self):
        """ normal wait time between pulses """
        self._gpio.set_gpio(0)
        time.sleep(self._pause_seconds)

    def _initial_wait(self):
        """ ensure consistent starting point
            - after correct pin input the menu is life
            - ~120 seconds after the last input the menu dies
        """
        if self._debug:
            return
        time.sleep(self._menu_timeout_seconds + 10)  # 10 seconds safety margin

    def _enter_pin_mode(self):
        """ put meter in 'enter pin' mode """
        self._initial_wait()
        self._short_pulse()
        self._pause()
        self._short_pulse()
        #self._transition()
        self._pause()

    def enter_pin(self, pin_array: Annotated[List[int], 4]):
        """ send pulse counts defined by the pin_array parameter """
        self._enter_pin_mode()
        for i in pin_array:
            if i == 0:
                i = 10
            while i > 0:
                i -= 1
                self._short_pulse(quick=True)
                if i > 0:
                    self._pause()
            self._transition()

    def toggle(self, pin_array: Annotated[List[int], 4], menu_item: str):
        """
        Traverses through the menu and toggles the menu_item
        :param pin_array: pin of the meter
        :param menu_item: The menu_item to toggle
        """
        self.enter_pin(pin_array)
        self._pause()
        menu_location = 0
        menu_total = 11
        if menu_item == "info":
            menu_location = 8
        elif menu_item == "pin":
            menu_location = 9
        for i in range(2, menu_total + 2):
            self._short_pulse(quick=True)
            self._pause()
            if i == menu_location:
                self._long_pulse()
                self._pause()

    def clear(self, pin_array: Annotated[List[int], 4], menu_item: str):
        """
        Traverses through the menu and clears the history of menu_item
        :param pin_array: pin of the meter
        :param menu_item: The menu_item to clear history of
        """
        self.enter_pin(pin_array)
        self._pause()
        menu_location = 0
        menu_total = 11
        if menu_item == "e":
            menu_location = 2
        elif menu_item == "his":
            menu_location = 7
        for i in range(2, menu_total + 2):
            self._short_pulse(quick=True)
            self._pause()
            if i == menu_location:
                self._long_pulse()
                self._pause()

    def show(self, pin_array: Annotated[List[int], 4], menu_item: str):
        """
        Traverses through the menu to the location of menu_item
        :param pin_array: pin of the meter
        :param menu_item: The menu_item to show
        """
        self.enter_pin(pin_array)
        self._pause()
        menu_location = 0
        menu_total = 11
        if menu_item == "e":
            menu_location = 1
        elif menu_item == "1d":
            menu_location = 3
        elif menu_item == "7d":
            menu_location = 4
        elif menu_item == "30d":
            menu_location = 5
        elif menu_item == "365d":
            menu_location = 6
        elif menu_item == "info":
            menu_location = 8
        elif menu_item == "pin":
            menu_location = 9
        for i in range(2, menu_total + 2):
            self._short_pulse(quick=True)
            self._pause()
            if i == menu_location:
                input("press enter to continue")
                if ((
                        time.time() - self._last_cmd_time)
                        > (self._menu_timeout_seconds - 5)
                ):  # 5 seconds safety margin
                    return
