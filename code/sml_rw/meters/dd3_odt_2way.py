"""
DD3-ODT two-way meter logic
"""
import time

from meters.dd3_odt import DD3ODT


class DD3ODT2Way(DD3ODT):
    """
    Class for the DD3-ODT two-way Meter
    """

    def toggle(self, menu_item: str):
        """
        Traverses through the menu and toggles the menu_item
        :param menu_item: The menu_item to toggle
        """
        self.enter_pin()
        self._pause()
        menu_location = 0
        menu_total = 16
        if menu_item == "info":
            menu_location = 14
        elif menu_item == "p":
            menu_location = 15
        elif menu_item == "pin":
            menu_location = 16
        for i in range(2, menu_total + 2):
            self._short_pulse(quick=True)
            self._pause()
            if i == menu_location:
                self._long_pulse()
                self._pause()

    def clear(self, menu_item: str):
        """
        Traverses through the menu and clears the history of menu_item
        :param menu_item: The menu_item to clear history of
        """
        raise NotImplementedError

    def show(self, menu_item: str):
        """
        Traverses through the menu to the location of menu_item
        :param menu_item: The menu_item to show
        """
        self.enter_pin()
        self._pause()
        menu_location = 0
        menu_total = 16
        # if menu_item == "e":
        #     menu_location = 2
        # elif menu_item == "1d":
        #     menu_location = 4
        # elif menu_item == "7d":
        #     menu_location = 5
        # elif menu_item == "30d":
        #     menu_location = 6
        # elif menu_item == "365d":
        #     menu_location = 7
        # elif menu_item == "info":
        if menu_item == "info":
            menu_location = 14
        elif menu_item == "p":
            menu_location = 15
        elif menu_item == "pin":
            menu_location = 16
        for i in range(2, menu_total + 2):
            self._short_pulse(quick=True)
            self._pause()
            if i == menu_location:
                input("press enter to continue")
                if (
                        (time.time() - self._last_cmd_time)
                        > (self._menu_timeout_seconds - 5)
                ):  # 5 seconds safety margin
                    return
