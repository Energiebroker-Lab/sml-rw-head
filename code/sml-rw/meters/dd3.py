import time
from meters.meter import Meter


class DD3(Meter):
    _pauseSeconds = 0.7
    _quickPauseSeconds = 0.5
    _transitionSeconds = 4
    _shortSeconds = 2
    _longSeconds = 6
    _lastCmdTime = time.time()
    _menuTimeoutSeconds = 120

    def _shortPulse(self, quick: bool = False):
        """ send short pulse """
        self._gpio.setGpio(1)
        if quick:
            time.sleep(self._quickPauseSeconds)
        else:
            time.sleep(self._shortSeconds)
        self._gpio.setGpio(0)
        self._lastCmdTime = time.time()

    def _longPulse(self):
        """ send long pulse """
        self._gpio.setGpio(1)
        time.sleep(self._longSeconds)
        self._gpio.setGpio(0)
        self._lastCmdTime = time.time()

    def _transition(self):
        """ wait for the meter to transition to the next input field """
        self._gpio.setGpio(0)
        time.sleep(self._transitionSeconds)

    def _pause(self):
        """ normal wait time between pulses """
        self._gpio.setGpio(0)
        time.sleep(self._pauseSeconds)

    def _initialWait(self):
        """ ensure consistent starting point
            - after correct pin input the menu is life
            - ~120 seconds after the last input the menu dies
        """
        if self._debug:
            return
        time.sleep(self._menuTimeoutSeconds + 10)  # 10 seconds safety margin

    def _enterPinMode(self):
        """ put meter in 'enter pin' mode """
        self._initialWait()
        self._shortPulse()
        self._transition()

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
        self.toggle("info")

    def toggle(self, menuItem: str):
        self.enterPin()
        self._pause()
        menuLocation = 0
        menuTotal = 11
        if menuItem == "info":
            menuLocation = 9
        elif menuItem == "p":
            menuLocation = 10
        elif menuItem == "pin":
            menuLocation = 11
        for i in range(2, menuTotal + 2):
            self._shortPulse(quick=True)
            self._pause()
            if i == menuLocation:
                self._longPulse()
                self._pause()

    def clear(self, menuItem: str):
        self.enterPin()
        self._pause()
        menuLocation = 0
        menuTotal = 11
        if menuItem == "e":
            menuLocation = 3
        elif menuItem == "his":
            menuLocation = 8
        for i in range(2, menuTotal + 2):
            self._shortPulse(quick=True)
            self._pause()
            if i == menuLocation:
                self._longPulse()
                self._pause()

    def show(self, menuItem: str):
        self.enterPin()
        self._pause()
        menuLocation = 0
        menuTotal = 11
        if menuItem == "e":
            menuLocation = 2
        elif menuItem == "1d":
            menuLocation = 4
        elif menuItem == "7d":
            menuLocation = 5
        elif menuItem == "30d":
            menuLocation = 6
        elif menuItem == "365d":
            menuLocation = 7
        elif menuItem == "info":
            menuLocation = 9
        elif menuItem == "p":
            menuLocation = 10
        elif menuItem == "pin":
            menuLocation = 11
        for i in range(2, menuTotal + 2):
            self._shortPulse(quick=True)
            self._pause()
            if i == menuLocation:
                input("press enter to continue")
                if (time.time() - self._lastCmdTime) > (self._menuTimeoutSeconds - 5):  # 5 seconds safety margin
                    return
