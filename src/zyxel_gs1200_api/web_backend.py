# SPDX-License-Identifier: BSD-3-Clause
# SPDX-FileCopyrightText: Czech Technical University in Prague

"""Low-level backend of Zyxel (X)GS-1200 series switches utilizing the web browser API."""

import base64
import hashlib
import requests
import rsa
import time
from urllib3.util import parse_url

from .backend import Backend
from .types import PacketCounter, Port, PortStatus, Switch

__all__ = ['WebBackend']


def formalize_request(r):
    r.params.update({"dummy": int(time.time())})
    _, _, _, _, _, query, _ = parse_url(r.prepare().url)
    digest = hashlib.md5(query.encode("utf8")).digest()
    try:
        digest = digest.hex()
    except AttributeError:  # Python 2
        digest = digest.encode('hex')
    r.params.update({"bj4": digest})
    return r


def get_one_of(data, keys):
    for key in keys:
        if key in data:
            return data[key]
    raise KeyError("None of the keys %r found in %s" % (keys, data.keys()))


# These are the strings coming from Zyxel API
if_speeds = {
    "10 Mbps": 10000000,
    "100 Mbps": 100000000,
    "1 Gbps": 1000000000,
    "2.5 Gbps": 2500000000,
    "5 Gbps": 5000000000,
    "10 Gbps": 10000000000,
}


port_type_speeds = {
    0: 10000000,
    1: 100000000,
    2: 1000000000,
    3: 2500000000,
    4: 5000000000,
    6: 10000000000,
}


port_type_device_names = {
    0: "Ethernet",
    1: "FastEthernet",
    2: "GigabitEthernet",
    3: "TwoPointFiveGigabitEthernet",
    4: "FiveGigabitEthernet",
    6: "TenGigabitEthernet",
}


port_type_device_short_names = {
    0: "et",
    1: "fe",
    2: "ge",
    3: "tw",
    4: "fe",
    6: "tg",
}


def get_port_name(port_types, num, short=False):
    port_type = port_types[num]
    port_num = 0
    for i in range(num):
        if port_types[i] == port_type:
            port_num += 1
    device_names = port_type_device_short_names if short else port_type_device_names
    return device_names[port_type] + str(port_num + 1)


class WebBackend(Backend):
    """Low-level backend of Zyxel (X)GS-1200 series switches utilizing the web browser API."""
    def __init__(self, address, password, max_login_attempts=3):
        """
        :param str address: The HTTP(S) address of the switch API.
        :param str password: Password for the switch administration.
        :param int max_login_attempts: Maximum number of login retries before an exception is raised.
        """
        super(WebBackend, self).__init__()

        self.address = address
        self.password = password

        self.max_login_attempts = max_login_attempts
        self.failed_login_attempts = 0

        self.session = requests.Session()
        self.logged_in = False

    def send_request(self, method, url, *args, **kwargs):
        """Send a HTTP request to the switch API.
        :param str method: GET or POST
        :param url: The URL part after address.
        :param args: Passed to :meth:`requests.Request`.
        :param kwargs: Passed to :meth:`requests.Request`.
        :return: The HTTP response.
        :rtype: requests.Response
        :raises requests.exceptions.RequestException:
        :raises RuntimeError:
        """
        auto_login = kwargs.get("auto_login", True)
        if "auto_login" in kwargs:
            del kwargs["auto_login"]
        if auto_login and not self.logged_in:
            self.auto_login()

        url = self.address + "/" + url
        req = requests.Request(method=method, url=url, *args, **kwargs)
        req = formalize_request(req)
        req = self.session.prepare_request(req)
        resp = self.session.send(req)
        resp.raise_for_status()

        # Some non-existent pages return empty page
        if resp.content == b"\n":
            resp.status_code = 400
            resp.reason = "Not found"
            resp.raise_for_status()

        try:
            if "logout" in resp.json():
                self.logged_in = False
                if auto_login:
                    self.auto_login()
                    return self.send_request(method, url, auto_login=False, *args, **kwargs)
                else:
                    raise RuntimeError("Authentication session has expired")
        except requests.exceptions.JSONDecodeError:
            pass  # The response is not a JSON
        return resp

    def get(self, cmd, *args, **kwargs):
        """Perform a get action on the API.
        :param cmd: The command to execute (`cmd` argument of the URL).
        :param args: Passed to :meth:`requests.Request`.
        :param kwargs: Passed to :meth:`requests.Request`.
        :return: The HTTP response.
        :rtype: requests.Response
        :raises requests.exceptions.RequestException:
        :raises RuntimeError:
        """
        return self.send_request("GET", "cgi/get.cgi?cmd=" + cmd, *args, **kwargs)

    def set(self, cmd, *args, **kwargs):
        """Perform a set action on the API.
        :param cmd: The command to execute (`cmd` argument of the URL).
        :param args: Passed to :meth:`requests.Request`.
        :param kwargs: Passed to :meth:`requests.Request`.
        :return: The HTTP response.
        :rtype: requests.Response
        :raises requests.exceptions.RequestException:
        :raises RuntimeError:
        """
        return self.send_request("POST", "cgi/set.cgi?cmd=" + cmd, *args, **kwargs)

    def auto_login(self):
        """Automatically log in the web API if it is needed.
        :raises requests.exceptions.RequestException:
        :raises RuntimeError:
        """
        self.failed_login_attempts = 0
        while self.failed_login_attempts < self.max_login_attempts:
            try:
                self.login()
                return
            except Exception as e:
                if "errLoginPwdInvalid" in str(e):
                    self.failed_login_attempts = self.max_login_attempts
                    raise RuntimeError("Login failed: Invalid password")
                self.failed_login_attempts += 1
                print(e)
                time.sleep(1)
        raise RuntimeError("Login failed too many times, exiting")

    def login(self):
        print("Authenticating {}/{}".format(self.failed_login_attempts + 1, self.max_login_attempts))
        modulus = self.get("home_loginInfo", auto_login=False).json()["data"]["modulus"]

        key = rsa.PublicKey(n=int(modulus, 16), e=0x10001)
        encrypted = rsa.encrypt(self.password.encode("ascii"), key)
        try:
            enc_pass = base64.encodebytes(encrypted)
        except AttributeError:
            enc_pass = base64.encodestring(encrypted)
        enc_pass = enc_pass.replace(b"\n", b"").replace(b"+", b"%2B").replace(b"=", b"%3D")
        enc_pass = enc_pass.decode("ascii")

        auth_id = self.set('home_loginAuth',
                           json={"_ds=1&password=" + enc_pass + "&xsrfToken=fa9358fbd291c3bd&_de=1": {}},
                           auto_login=False).json()["authId"]
        resp = self.set("home_loginStatus",
                        json={"_ds=1&authId=" + auth_id + "&xsrfToken=fa9358fbd291c3bd&_de=1": {}},
                        auto_login=False).json()

        if resp["data"]["status"] != "ok":
            raise RuntimeError("Login failed: {}".format(resp["data"]))
        print("Successfully authenticated with session ID " + self.session.cookies["HTTP_SESSID"])

        self.logged_in = True
        self.failed_login_attempts = 0

    def logout(self):
        self.set("home_logout", data={})
        self.logged_in = False
        self.failed_login_attempts = 0
        print("Logged out")

    def get_switch(self):
        switch = Switch()

        main_data = self.get("home_main").json()["data"]
        switch.first_login = main_data["sys_first_login"] != '0'

        if switch.first_login:
            raise RuntimeError("Complete the first-time setup before accessing the switch API.")

        capabilities = main_data["capability"]
        switch.capabilities.ssh = bool(capabilities.get("ssh", False))
        switch.capabilities.https = bool(capabilities.get("https", False))
        switch.capabilities.websock = bool(capabilities.get("websock", False))
        switch.capabilities.debug_img = bool(capabilities.get("debug_img", False))
        switch.capabilities.mgmt_vlan = bool(capabilities.get("mgmt_vlan", False))
        switch.capabilities.overheat_protect = bool(capabilities.get("overheat_protect", False))

        switch.model_name = main_data["model_name"]
        switch.device_name = main_data["sys_dev_name"]
        switch.firmware_version = main_data["sys_fmw_ver"]
        switch.firmware_build_date = main_data["sys_bld_date"]
        switch.max_mtu = 12288 if switch.model_name.startswith("XGS") else 9000

        switch.mac_str = main_data["sys_MAC"].lower()
        try:
            switch.mac_bin = bytes.fromhex(switch.mac_str.replace(":", ""))
        except AttributeError:  # Python 2
            switch.mac_bin = switch.mac_str.replace(":", "").decode('hex')

        switch.ip_addr = main_data["sys_IP"]
        switch.ip_subnet = main_data["sys_sbnt_msk"]
        switch.ip_gateway = main_data["sys_gateway"]
        switch.dhcp_enabled = main_data["sys_dhcp_state"] != '0'

        switch.description = "Zyxel %s (FW %s) at %s/%s%s" % (
            switch.model_name, switch.firmware_version, switch.ip_addr, switch.ip_subnet,
            " (DHCP client)" if switch.dhcp_enabled else "")

        # ABTY.6 firmware renamed Max_port to max_port
        switch.num_ports = int(get_one_of(main_data, ("Max_port", "max_port")))

        port_data = self.get("port_portInfo").json()["data"]

        for i in range(switch.num_ports):
            port = Port()
            port.index = i
            port.max_speed = port_type_speeds[port_data["portType"][i]]
            port.name = get_port_name(port_data["portType"], i, short=False)
            port.short_name = get_port_name(port_data["portType"], i, short=True)
            port.alias = port.name
            port.mtu = switch.max_mtu
            port.is_copper = bool(port_data["isCopper"])
            port.mac_bin = switch.mac_bin
            port.mac_str = switch.mac_str
            port.status = PortStatus()
            port.status.rx_packets = PacketCounter()
            port.status.tx_packets = PacketCounter()
            port.status.enabled = bool((port_data["portState"] >> i) & 1)
            switch.ports.append(port)

        return switch

    def update_switch_config(self, switch):
        main_data = self.get("home_main").json()["data"]

        switch.first_login = main_data["sys_first_login"] != '0'
        switch.device_name = main_data["sys_dev_name"]
        switch.firmware_version = main_data["sys_fmw_ver"]
        switch.firmware_build_date = main_data["sys_bld_date"]

        switch.mac_str = main_data["sys_MAC"].lower()
        switch.mac_bin = bytes.fromhex(switch.mac_str.replace(":", ""))

        switch.ip_addr = main_data["sys_IP"]
        switch.ip_subnet = main_data["sys_sbnt_msk"]
        switch.ip_gateway = main_data["sys_gateway"]
        switch.dhcp_enabled = main_data["sys_dhcp_state"] != '0'

        port_data = self.get("port_portInfo").json()["data"]

        for i in range(switch.num_ports):
            port = switch.ports[i]
            port.max_speed = port_type_speeds[port_data["portType"][i]]
            port.mtu = switch.max_mtu
            port.mac_bin = switch.mac_bin
            port.mac_str = switch.mac_str
            port.status.enabled = bool((port_data["portState"] >> i) & 1)

    def update_port_states(self, switch):
        sys_data = self.get("home_systemData").json()["data"]
        link_data = self.get("home_linkData").json()["data"]

        switch.device_name = sys_data["sys_dev_name"]
        switch.mac_str = sys_data["sys_MAC"].lower()
        try:
            switch.mac_bin = bytes.fromhex(switch.mac_str.replace(":", ""))
        except AttributeError:  # Python2
            switch.mac_bin = switch.mac_str.replace(":", "").decode('hex')
            
        switch.ip_addr = sys_data["sys_IP"]
        switch.ip_subnet = sys_data["sys_sbnt_msk"]
        switch.ip_gateway = sys_data["sys_gateway"]
        switch.dhcp_enabled = sys_data["sys_dhcp_state"] != '0'

        for i in range(switch.num_ports):
            port = switch.ports[i]
            status = port.status
            assert isinstance(status, PortStatus)

            connected = link_data["portstatus"][i] == "Up"

            if status.connected is None:
                status.connected = connected
            elif status.connected != connected:
                status.last_change_time = time.time()
            status.connected = connected

            status.speed = if_speeds[link_data["speed"][i]] if status.connected else 0
            status.loop_detected = sys_data["loop_status"][i] != "Normal"

            if switch.capabilities.overheat_protect:
                status.overheat_detected = bool(link_data["overheat"][i])

            rx_packets = link_data["Stats"][i][0]
            tx_packets = link_data["Stats"][i][1]
            if rx_packets < status.rx_packets.num_unicast_packets or tx_packets < status.tx_packets.num_unicast_packets:
                status.last_packet_jump_back_time = time.time()

            status.rx_packets.num_unicast_packets = rx_packets
            status.tx_packets.num_unicast_packets = tx_packets
