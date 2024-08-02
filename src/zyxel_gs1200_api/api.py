# SPDX-License-Identifier: BSD-3-Clause
# SPDX-FileCopyrightText: Czech Technical University in Prague

"""High-level API for collecting information about the Zyxel switch using a low-level backend."""

from .backend import Backend
from .test_backend import TestBackend
from .web_backend import WebBackend

__all__ = ['ZyxelAPI']


class ZyxelAPI:
    """High-level API for collecting information about the Zyxel switch using a low-level backend."""

    def __init__(self, address_or_backend, password=""):
        """
        :param address_or_backend: Address of the web/serial interface of the switch, word "test", or a backend instance
        :type address_or_backend: str or Backend
        :param str password: Password or another parameter required by the autodetected backend.
        """
        if address_or_backend.startswith('http'):
            self._backend = WebBackend(address_or_backend, password)
        elif address_or_backend == "test":
            self._backend = TestBackend()
        elif address_or_backend.startswith("/dev/tty") or address_or_backend.startswith("file:///dev/tty"):
            raise NotImplementedError("Serial console backend is not yet implemented")
        elif isinstance(address_or_backend, Backend):
            self._backend = address_or_backend
        else:
            raise NotImplementedError("Unknown address. To type the Web GUI address, start with http://")

    def get_switch(self):
        """Connect to the switch and read its static or semi-static configuration. The status fields will not be filled.
        :return: The populated switch instance.
        :rtype: Switch
        :raises: RuntimeError
        """
        return self._backend.get_switch()

    def update_switch_config(self, switch):
        """Update semi-static configuration of the switch. Should be called from time to time to update things like
        port speeds or administrative status of individual ports.
        :param Switch switch: The switch instance prepopulated by a previous call to :meth:`~get_switch`. This instance
                              will be updated.
        :raises: RuntimeError
        """
        self._backend.update_switch_config(switch)

    def update_port_states(self, switch):
        """Update dynamic status of the switch. Should be called periodically.
        :param Switch switch: The switch instance prepopulated by a previous call to :meth:`~get_switch`. This instance
                              will be updated.
        :raises: RuntimeError
        """
        self._backend.update_port_states(switch)

    def __enter__(self):
        self._backend.login()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self._backend.logout()
        except:  # noqa: E722
            pass
