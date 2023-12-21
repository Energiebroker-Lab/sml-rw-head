import time
from meters.meter import Meter


class EHZ(Meter):
    _pauseSeconds = 0.7
    _quickPauseSeconds = 0.4
    _transitionSeconds = 4
    _shortSeconds = 2
    _longSeconds = 6

    def _shortPulse(self, quick: bool = False):
        """ send short pulse """
        self._gpio.setGpio(1)
        if quick:
            time.sleep(self._quickPauseSeconds)
        else:
            time.sleep(self._shortSeconds)
        self._gpio.setGpio(0)

    def _longPulse(self):
        """ send long pulse """
        self._gpio.setGpio(1)
        time.sleep(self._longSeconds)
        self._gpio.setGpio(0)

    def _transition(self):
        """ wait for the meter to transition to the next input field """
        self._gpio.setGpio(0)
        time.sleep(self._transitionSeconds)

    def _pause(self):
        """ normal wait time between pulses """
        self._gpio.setGpio(0)
        time.sleep(self._pauseSeconds)

    def _initialWait(self):
        """ ensure consistent starting point """
        if self._debug:
            return
        self._transition()
        self._transition()
        self._transition()
        self._transition()

    def _enterPinMode(self):
        """ put meter in 'enter pin' mode """
        self._initialWait()
        self._shortPulse()
        self._pause()
        self._shortPulse()
        self._pause()

    def enterPin(self):
        """ send pulse counts defined by the pinArray parameter """
        self._enterPinMode()
        for i in self._pin:
            while i > 0:
                i -= 1
                self._shortPulse(quick=True)
                if i > 0:
                    self._pause()
            self._transition()

    def toggleInfoMode(self):
        self.enterPin()
