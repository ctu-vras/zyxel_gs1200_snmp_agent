# SPDX-License-Identifier: BSD-3-Clause
# SPDX-FileCopyrightText: Czech Technical University in Prague

"""Data types provided by the high-level API."""

try:
    from dataclasses import dataclass
except ImportError:
    def dataclass(f):
        return f

__all__ = ['Capabilities', 'PacketCounter', 'Port', 'PortStatus', 'Switch']


@dataclass
class Capabilities(object):
    """Capabilities of the switch and its firmware."""
    debug_img = False
    """Whether a debug image is loaded."""
    mgmt_vlan = False
    """Whether management VLAN is supported."""
    https = False
    """Whether HTTPS API is supported."""
    websock = False
    """Whether WebSocket API is supported."""
    overheat_protect = False
    """Whether overheat protection is supported."""
    ssh = False
    """Whether SSH is supported."""


@dataclass
class PacketCounter(object):
    """Counter of packets flowing through a switch port in one direction."""
    num_bytes = 0
    """Total number of bytes."""
    num_unicast_packets = 0
    """Total number of unicast packets."""
    num_multicast_packets = 0
    """Total number of multicast packets."""
    num_broadcast_packets = 0
    """Total number of broadcast packets."""
    num_discards = 0
    """Total number of discarded packets."""
    num_errors = 0
    """Total number of errors."""


@dataclass
class PortStatus(object):
    """Dynamic status of a switch port."""
    enabled = False
    """Whether the port is administratively enabled."""
    connected = None
    """Whether the port is connected."""
    speed = 0
    """Speed of the port in bps."""
    last_change_time = 0
    """Last time a change to the connected state was detected."""
    loop_detected = False
    """Whether is loop is currently detected between this port and another one."""
    overheat_detected = False
    """Whether this port is overheating."""
    rx_packets = PacketCounter()
    """Counter of received packets."""
    tx_packets = PacketCounter()
    """Counter of transmitted packets."""
    last_packet_jump_back_time = 0
    """Last time when `rx_packets` or `tx_packets` counters jumped back."""


@dataclass
class Port(object):
    """Information about a switch port."""
    index = 0
    """Index of the port in the switch API."""
    name = ''
    """Long name of the port (e.g. GigabitEthernet1)."""
    short_name = ''
    """Short name of the port (e.g. ge1)."""
    alias = ''
    """Alias of the port (configurable by user, falls back to `name`)."""
    max_speed = 0
    """Maximum speed of the port in bps."""
    mtu = 1500
    """MTU of the port in bytes."""
    is_copper = False
    """Whether the port is copper or optical."""
    mac_bin = b''
    """Binary representation of the port's MAC address."""
    mac_str = ''
    """String representation of the port's MAC address."""
    status = PortStatus()
    """Dynamic status of the port."""


@dataclass
class Switch(object):
    """Representation of the switch."""
    num_ports = 0
    """Number of switch ports."""
    model_name = ''
    """Name of the switch model."""
    device_name = ''
    """Name of the device (configurable in web GUI)."""
    firmware_version = ''
    """Firmware version of the switch."""
    firmware_build_date = ''
    """Firmware build date."""
    description = ''
    """A human-readable description of the switch."""
    mac_bin = b''
    """Binary representation of the switch MAC address."""
    mac_str = ''
    """String representation of the switch MAC address."""
    ip_addr = ''
    """IP address of the switch."""
    ip_subnet = ''
    """IP subnet of the switch."""
    ip_gateway = ''
    """IP gateway of the switch."""
    dhcp_enabled = False
    """Whether DHCP client is enabled for the switch API."""
    first_login = True
    """Whether this is the very first login after factory reset and the switch needs to be configured."""
    max_mtu = 1500
    """Maximum MTU in bytes."""
    capabilities = Capabilities()
    """Capabilities of the switch."""
    ports = []  # List[Port]
    """List of switch ports (ordered by port index)."""
