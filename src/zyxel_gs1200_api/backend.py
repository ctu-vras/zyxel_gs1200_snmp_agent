# SPDX-License-Identifier: BSD-3-Clause
# SPDX-FileCopyrightText: Czech Technical University in Prague

"""Common interface for all Zyxel (X)GS-1200 series low-level backends."""

from .types import Switch

__all__ = ['Backend']


class Backend(object):
    """Common interface for all Zyxel (X)GS-1200 series low-level backends."""

    def login(self):
        """Perform login to the switch."""
        raise NotImplementedError()

    def logout(self):
        """Perform logout from the switch."""
        raise NotImplementedError()

    def get_switch(self):
        """Connect to the switch and read its static or semi-static configuration. The status fields will not be filled.
        :return: The populated switch instance.
        :rtype: Switch
        :raises: RuntimeError
        """
        raise NotImplementedError()

    def update_switch_config(self, switch):
        """Update semi-static configuration of the switch. Should be called from time to time to update things like
        port speeds or administrative status of individual ports.
        :param Switch switch: The switch instance prepopulated by a previous call to :meth:`~get_switch`. This instance
                              will be updated.
        :raises: RuntimeError
        """
        raise NotImplementedError()

    def update_port_states(self, switch):
        """Update dynamic status of the switch. Should be called periodically.
        :param Switch switch: The switch instance prepopulated by a previous call to :meth:`~get_switch`. This instance
                              will be updated.
        :raises: RuntimeError
        """
        raise NotImplementedError()
