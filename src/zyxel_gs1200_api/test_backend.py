# SPDX-License-Identifier: BSD-3-Clause
# SPDX-FileCopyrightText: Czech Technical University in Prague

"""Test backend of the switch allowing to test the API without being actually connected to the switch."""

from .web_backend import WebBackend

__all__ = ['TestBackend']


class JsonWrapper:
    def __init__(self, obj):
        self.obj = obj

    def json(self):
        return {"data": self.obj}


class TestBackend(WebBackend):
    """Test backend of the switch allowing to test the API without being actually connected to the switch."""

    def __init__(self):
        super(TestBackend, self).__init__("", "")

    def get(self, cmd, *args, **kwargs):
        base_sys_data = {
            'Max_port': 12,
            'model_name': 'XGS1210-12',
            'sys_dev_name': 'marv-robot-sw',
            'sys_fmw_ver': 'V1.00(ABTY.6)C0',
            'sys_bld_date': 'Aug 19 2022 - 17:18:42',
            'sys_MAC': '00:E0:4C:00:00:01',
            'sys_IP': '192.168.1.3',
            'sys_sbnt_msk': '255.255.255.0',
            'sys_gateway': '0.0.0.0',
            'sys_dhcp_state': '0',
        }
        if cmd == "home_systemData":
            data = {
                'loop_status': ['Normal', 'Normal', 'Normal', 'Normal', 'Normal', 'Normal', 'Normal', 'Normal',
                                'Normal', 'Normal', 'Normal', 'Normal', 'Normal', 'Normal', 'Normal', 'Normal'],
                'loop': 'Normal',
                'isTrunk0': 0,
                'isTrunk1': 0,
                'isTrunk2': 0,
                'isTrunk3': 0
            }
            data.update(base_sys_data)
            return JsonWrapper(data)
        elif cmd == "home_linkData":
            return JsonWrapper({
                'portstatus': ['Down', 'Down', 'Down', 'Down', 'Up', 'Up', 'Up', 'Down', 'Up', 'Up', 'Up', 'Down',
                               'Down', 'Down', 'Down', 'Down'],
                'speed': ['auto', 'auto', 'auto', 'auto', '1 Gbps', '1 Gbps', '1 Gbps', 'auto', '1 Gbps', '1 Gbps',
                          '10 Gbps', '10 Gbps', 'auto', 'auto', 'auto', 'auto'],
                'Stats': [[0, 0], [0, 0], [0, 0], [0, 0], [989337, 1901160], [30439, 251116], [30441, 251118], [0, 0],
                          [94387325, 692480894], [1278514941, 446201368], [361071932, 594838996],
                          [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]})
        elif cmd == "port_portInfo":
            return JsonWrapper({
                'portType': [2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 6, 6],
                'isCopper': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
                'portSpeed': [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
                'portState': 4095, 'portFlctl': 0, 'storm_ctrl_en': 0, 'storm_ctrl_pps': 10000, 'loop_dp': 2})
        elif cmd == "home_main":
            data = {
                'sys_first_login': '0',
                'sys_lag_map': [[0, 1, 2, 3], [4, 5], [6, 7], [8, 9]],
                'capability': {'debug_img': 0, 'mgmt_vlan': 1, 'https': 1, 'websock': 1, 'overheat_protect': 0},
            }
            data.update(base_sys_data)
            return JsonWrapper(data)

    def set(self, cmd, *args, **kwargs):
        pass

    def login(self):
        pass

    def logout(self):
        pass
