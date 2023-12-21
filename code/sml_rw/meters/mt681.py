"""
MT681 meter logic
"""
import time

from meters.meter import Meter


class MT681(Meter):
    """
    MT681 meter logic and config
    """
    _pause_seconds = 0.7
    _quick_pause_seconds = 0.6
    _transition_seconds = 4
    _short_seconds = 2
    _long_seconds = 6

    def _short_pulse(self, quick: bool = False):
        """ send short pulse """
        self._gpio.set_gpio(1)
        if quick:
            time.sleep(self._quick_pause_seconds)
        else:
            time.sleep(self._short_seconds)
        self._gpio.set_gpio(0)

    def _long_pulse(self):
        """ send long pulse """
        self._gpio.set_gpio(1)
        time.sleep(self._long_seconds)
        self._gpio.set_gpio(0)

    def _transition(self):
        """ wait for the meter to transition to the next input field """
        if self._debug:
            return
        self._gpio.set_gpio(0)
        time.sleep(self._transition_seconds)

    def _pause(self):
        """ normal wait time between pulses """
        self._gpio.set_gpio(0)
        time.sleep(self._pause_seconds)

    def _quick_pause(self):
        """ quick wait time between pulses """
        self._gpio.set_gpio(0)
        time.sleep(self._quick_pause_seconds)

    def _initial_wait(self):
        """ ensure consistent starting point """
        self._transition()
        self._transition()
        self._transition()
        self._transition()

    def _enter_pin_mode(self):
        """ put meter in 'enter pin' mode """
        self._initial_wait()
        self._short_pulse()
        self._pause()
        self._short_pulse()
        self._quick_pause()

    def enter_pin(self):
        """ send pulse counts defined by the pin_array parameter """
        self._enter_pin_mode()
        for i in self._pin:
            while i > 0:
                i -= 1
                self._short_pulse(quick=True)
                if i > 0:
                    self._pause()
            self._transition()

    def toggle_info_mode(self):
        """
        toggles the info mode by entering the pin
        """
        self.enter_pin()
