<!-- SPDX-License-Identifier: BSD-3-Clause -->
<!-- SPDX-FileCopyrightText: Czech Technical University in Prague -->

# External SNMP Agent for Zyxel (X)GS-1200 Series Switches and a Python API to communicate with the switch

Supported models:

- Zyxel GS1200-5 (not tested)
- Zyxel GS1200-8 (not tested)
- Zyxel GS1200-5HP v2 (not tested)
- Zyxel GS1200-8HP v2 (not tested)
- Zyxel XGS1210-12
- Zyxel XGS1250-12 (not tested)
- Zyxel XGS1010-12 (after [uploading firmware](https://www.reddit.com/r/homelab/comments/16q095r/making_managed_switch_out_of_unmanaged_zyxel/))

Tested firmwares:

- XGS1210_V1.00(ABTY.4)C0.bix
- XGS1210-12_V1.00(ABTY.5)C0.bix
- XGS1210-12_V1.00(ABTY.6)C0.bix

Not tested on 2.0 firmwares.

## Nodes

### snmp_agent

ROS node that uses `ZyxelAPI` to provide an external SNMP agent for the switch.

#### Parameters
- `~address` (str): Address of the HTTP API (including 'http://').
- `~password` (str): Password for the HTTP API.
- `~update_rate` (float): Polling frequency.
- `~snmp_port` (int, default 1161): Port at which the SNMP agent will be available. Note that ROS is not compatible with
                                    running as root, so ports under 1024 are not available.
- `~snmp_listen_ipv4` (str, default '0.0.0.0'): Listening IPv4 address of the SNMP server. If empty, IPv4 is disabled.
- `~snmp_listen_ipv6` (str, default '::'): Listening IPv6 address of the SNMP server. If empty, IPv6 is disabled.
- `~snmpv1` (bool, default True): Whether to provide SNMPv1.
- `~snmpv2c` (bool, default True): Whether to provide SNMPv2c.
- `~snmpv3` (bool, default True): Whether to provide SNMPv3.
- `~snmp_community` (str, default 'public'): The SNMP community name.
- `~snmpv3_user` (str, default 'public'): The SNMPv3 user name.
- `~snmpv3_auth` (str, default 'usmNoAuthProtocol'): The SNMPv3 authentication protocol. One of `pysnmp.entity.config`.
- `~snmpv3_priv` (str, default 'usmNoPrivProtocol'): The SNMPv3 privacy protocol. One of `pysnmp.entity.config`.
- `~snmpv3_auth_key` (str, optional): If set, this is the SNMPv3 auth key.
- `~snmpv3_priv_key` (str, optional): If set, this is the SNMPv3 priv key.
- `~demo_port_info` (bool, default False): If true, `~port_info` will be populated with a demonstration content.
- `~port_info` (dict): Extra configuration of switch ports. Keys are port names (e.g. `GigabitEthernet1`) and values
                       are dicts. These dicts can contain the following keys:
                       `name`: This is an alias of the port reported as `ifAlias` IF-MIB value.


#### Example snmpwalk

<details>

<summary>`snmpwalk localhost:1161 -v3 -u public -c public`</summary>

```
SNMPv2-MIB::sysDescr.0 = STRING: Zyxel XGS1210-12 (FW V1.00(ABTY.6)C0) at 192.168.1.3/255.255.255.0
SNMPv2-MIB::sysObjectID.0 = OID: SNMPv2-SMI::enterprises.20408
DISMAN-EVENT-MIB::sysUpTimeInstance = Timeticks: (375) 0:00:03.75
SNMPv2-MIB::sysContact.0 = STRING: 
SNMPv2-MIB::sysName.0 = STRING: marv-robot-sw
SNMPv2-MIB::sysLocation.0 = STRING: cras-17
SNMPv2-MIB::sysServices.0 = INTEGER: 4
SNMPv2-MIB::sysORLastChange.0 = Timeticks: (0) 0:00:00.00
IF-MIB::ifNumber.0 = INTEGER: 12
IF-MIB::ifIndex.1 = INTEGER: 1
IF-MIB::ifIndex.2 = INTEGER: 2
IF-MIB::ifIndex.3 = INTEGER: 3
IF-MIB::ifIndex.4 = INTEGER: 4
IF-MIB::ifIndex.5 = INTEGER: 5
IF-MIB::ifIndex.6 = INTEGER: 6
IF-MIB::ifIndex.7 = INTEGER: 7
IF-MIB::ifIndex.8 = INTEGER: 8
IF-MIB::ifIndex.9 = INTEGER: 9
IF-MIB::ifIndex.10 = INTEGER: 10
IF-MIB::ifIndex.11 = INTEGER: 11
IF-MIB::ifIndex.12 = INTEGER: 12
IF-MIB::ifDescr.1 = STRING: GigabitEthernet1
IF-MIB::ifDescr.2 = STRING: GigabitEthernet2
IF-MIB::ifDescr.3 = STRING: GigabitEthernet3
IF-MIB::ifDescr.4 = STRING: GigabitEthernet4
IF-MIB::ifDescr.5 = STRING: GigabitEthernet5
IF-MIB::ifDescr.6 = STRING: GigabitEthernet6
IF-MIB::ifDescr.7 = STRING: GigabitEthernet7
IF-MIB::ifDescr.8 = STRING: GigabitEthernet8
IF-MIB::ifDescr.9 = STRING: TwoPointFiveGigabitEthernet1
IF-MIB::ifDescr.10 = STRING: TwoPointFiveGigabitEthernet2
IF-MIB::ifDescr.11 = STRING: TenGigabitEthernet1
IF-MIB::ifDescr.12 = STRING: TenGigabitEthernet2
IF-MIB::ifType.1 = INTEGER: ethernetCsmacd(6)
IF-MIB::ifType.2 = INTEGER: ethernetCsmacd(6)
IF-MIB::ifType.3 = INTEGER: ethernetCsmacd(6)
IF-MIB::ifType.4 = INTEGER: ethernetCsmacd(6)
IF-MIB::ifType.5 = INTEGER: ethernetCsmacd(6)
IF-MIB::ifType.6 = INTEGER: ethernetCsmacd(6)
IF-MIB::ifType.7 = INTEGER: ethernetCsmacd(6)
IF-MIB::ifType.8 = INTEGER: ethernetCsmacd(6)
IF-MIB::ifType.9 = INTEGER: ethernetCsmacd(6)
IF-MIB::ifType.10 = INTEGER: ethernetCsmacd(6)
IF-MIB::ifType.11 = INTEGER: ethernetCsmacd(6)
IF-MIB::ifType.12 = INTEGER: ethernetCsmacd(6)
IF-MIB::ifMtu.1 = INTEGER: 12288
IF-MIB::ifMtu.2 = INTEGER: 12288
IF-MIB::ifMtu.3 = INTEGER: 12288
IF-MIB::ifMtu.4 = INTEGER: 12288
IF-MIB::ifMtu.5 = INTEGER: 12288
IF-MIB::ifMtu.6 = INTEGER: 12288
IF-MIB::ifMtu.7 = INTEGER: 12288
IF-MIB::ifMtu.8 = INTEGER: 12288
IF-MIB::ifMtu.9 = INTEGER: 12288
IF-MIB::ifMtu.10 = INTEGER: 12288
IF-MIB::ifMtu.11 = INTEGER: 12288
IF-MIB::ifMtu.12 = INTEGER: 12288
IF-MIB::ifSpeed.1 = Gauge32: 0
IF-MIB::ifSpeed.2 = Gauge32: 0
IF-MIB::ifSpeed.3 = Gauge32: 0
IF-MIB::ifSpeed.4 = Gauge32: 0
IF-MIB::ifSpeed.5 = Gauge32: 1000000000
IF-MIB::ifSpeed.6 = Gauge32: 1000000000
IF-MIB::ifSpeed.7 = Gauge32: 1000000000
IF-MIB::ifSpeed.8 = Gauge32: 0
IF-MIB::ifSpeed.9 = Gauge32: 1000000000
IF-MIB::ifSpeed.10 = Gauge32: 1000000000
IF-MIB::ifSpeed.11 = Gauge32: 4294967295
IF-MIB::ifSpeed.12 = Gauge32: 0
IF-MIB::ifPhysAddress.1 = STRING: 0:e0:4c:0:0:1
IF-MIB::ifPhysAddress.2 = STRING: 0:e0:4c:0:0:1
IF-MIB::ifPhysAddress.3 = STRING: 0:e0:4c:0:0:1
IF-MIB::ifPhysAddress.4 = STRING: 0:e0:4c:0:0:1
IF-MIB::ifPhysAddress.5 = STRING: 0:e0:4c:0:0:1
IF-MIB::ifPhysAddress.6 = STRING: 0:e0:4c:0:0:1
IF-MIB::ifPhysAddress.7 = STRING: 0:e0:4c:0:0:1
IF-MIB::ifPhysAddress.8 = STRING: 0:e0:4c:0:0:1
IF-MIB::ifPhysAddress.9 = STRING: 0:e0:4c:0:0:1
IF-MIB::ifPhysAddress.10 = STRING: 0:e0:4c:0:0:1
IF-MIB::ifPhysAddress.11 = STRING: 0:e0:4c:0:0:1
IF-MIB::ifPhysAddress.12 = STRING: 0:e0:4c:0:0:1
IF-MIB::ifAdminStatus.1 = INTEGER: up(1)
IF-MIB::ifAdminStatus.2 = INTEGER: up(1)
IF-MIB::ifAdminStatus.3 = INTEGER: up(1)
IF-MIB::ifAdminStatus.4 = INTEGER: up(1)
IF-MIB::ifAdminStatus.5 = INTEGER: up(1)
IF-MIB::ifAdminStatus.6 = INTEGER: up(1)
IF-MIB::ifAdminStatus.7 = INTEGER: up(1)
IF-MIB::ifAdminStatus.8 = INTEGER: up(1)
IF-MIB::ifAdminStatus.9 = INTEGER: up(1)
IF-MIB::ifAdminStatus.10 = INTEGER: up(1)
IF-MIB::ifAdminStatus.11 = INTEGER: up(1)
IF-MIB::ifAdminStatus.12 = INTEGER: up(1)
IF-MIB::ifOperStatus.1 = INTEGER: dormant(5)
IF-MIB::ifOperStatus.2 = INTEGER: dormant(5)
IF-MIB::ifOperStatus.3 = INTEGER: dormant(5)
IF-MIB::ifOperStatus.4 = INTEGER: dormant(5)
IF-MIB::ifOperStatus.5 = INTEGER: up(1)
IF-MIB::ifOperStatus.6 = INTEGER: up(1)
IF-MIB::ifOperStatus.7 = INTEGER: up(1)
IF-MIB::ifOperStatus.8 = INTEGER: dormant(5)
IF-MIB::ifOperStatus.9 = INTEGER: up(1)
IF-MIB::ifOperStatus.10 = INTEGER: up(1)
IF-MIB::ifOperStatus.11 = INTEGER: up(1)
IF-MIB::ifOperStatus.12 = INTEGER: dormant(5)
IF-MIB::ifLastChange.1 = Timeticks: (0) 0:00:00.00
IF-MIB::ifLastChange.2 = Timeticks: (0) 0:00:00.00
IF-MIB::ifLastChange.3 = Timeticks: (0) 0:00:00.00
IF-MIB::ifLastChange.4 = Timeticks: (0) 0:00:00.00
IF-MIB::ifLastChange.5 = Timeticks: (0) 0:00:00.00
IF-MIB::ifLastChange.6 = Timeticks: (0) 0:00:00.00
IF-MIB::ifLastChange.7 = Timeticks: (0) 0:00:00.00
IF-MIB::ifLastChange.8 = Timeticks: (0) 0:00:00.00
IF-MIB::ifLastChange.9 = Timeticks: (0) 0:00:00.00
IF-MIB::ifLastChange.10 = Timeticks: (0) 0:00:00.00
IF-MIB::ifLastChange.11 = Timeticks: (0) 0:00:00.00
IF-MIB::ifLastChange.12 = Timeticks: (0) 0:00:00.00
IF-MIB::ifInOctets.1 = Counter32: 0
IF-MIB::ifInOctets.2 = Counter32: 0
IF-MIB::ifInOctets.3 = Counter32: 0
IF-MIB::ifInOctets.4 = Counter32: 0
IF-MIB::ifInOctets.5 = Counter32: 0
IF-MIB::ifInOctets.6 = Counter32: 0
IF-MIB::ifInOctets.7 = Counter32: 0
IF-MIB::ifInOctets.8 = Counter32: 0
IF-MIB::ifInOctets.9 = Counter32: 0
IF-MIB::ifInOctets.10 = Counter32: 0
IF-MIB::ifInOctets.11 = Counter32: 0
IF-MIB::ifInOctets.12 = Counter32: 0
IF-MIB::ifInUcastPkts.1 = Counter32: 0
IF-MIB::ifInUcastPkts.2 = Counter32: 0
IF-MIB::ifInUcastPkts.3 = Counter32: 0
IF-MIB::ifInUcastPkts.4 = Counter32: 0
IF-MIB::ifInUcastPkts.5 = Counter32: 989337
IF-MIB::ifInUcastPkts.6 = Counter32: 30439
IF-MIB::ifInUcastPkts.7 = Counter32: 30441
IF-MIB::ifInUcastPkts.8 = Counter32: 0
IF-MIB::ifInUcastPkts.9 = Counter32: 94387325
IF-MIB::ifInUcastPkts.10 = Counter32: 1278514941
IF-MIB::ifInUcastPkts.11 = Counter32: 361071932
IF-MIB::ifInUcastPkts.12 = Counter32: 0
IF-MIB::ifInNUcastPkts.1 = Counter32: 0
IF-MIB::ifInNUcastPkts.2 = Counter32: 0
IF-MIB::ifInNUcastPkts.3 = Counter32: 0
IF-MIB::ifInNUcastPkts.4 = Counter32: 0
IF-MIB::ifInNUcastPkts.5 = Counter32: 0
IF-MIB::ifInNUcastPkts.6 = Counter32: 0
IF-MIB::ifInNUcastPkts.7 = Counter32: 0
IF-MIB::ifInNUcastPkts.8 = Counter32: 0
IF-MIB::ifInNUcastPkts.9 = Counter32: 0
IF-MIB::ifInNUcastPkts.10 = Counter32: 0
IF-MIB::ifInNUcastPkts.11 = Counter32: 0
IF-MIB::ifInNUcastPkts.12 = Counter32: 0
IF-MIB::ifInDiscards.1 = Counter32: 0
IF-MIB::ifInDiscards.2 = Counter32: 0
IF-MIB::ifInDiscards.3 = Counter32: 0
IF-MIB::ifInDiscards.4 = Counter32: 0
IF-MIB::ifInDiscards.5 = Counter32: 0
IF-MIB::ifInDiscards.6 = Counter32: 0
IF-MIB::ifInDiscards.7 = Counter32: 0
IF-MIB::ifInDiscards.8 = Counter32: 0
IF-MIB::ifInDiscards.9 = Counter32: 0
IF-MIB::ifInDiscards.10 = Counter32: 0
IF-MIB::ifInDiscards.11 = Counter32: 0
IF-MIB::ifInDiscards.12 = Counter32: 0
IF-MIB::ifInErrors.1 = Counter32: 0
IF-MIB::ifInErrors.2 = Counter32: 0
IF-MIB::ifInErrors.3 = Counter32: 0
IF-MIB::ifInErrors.4 = Counter32: 0
IF-MIB::ifInErrors.5 = Counter32: 0
IF-MIB::ifInErrors.6 = Counter32: 0
IF-MIB::ifInErrors.7 = Counter32: 0
IF-MIB::ifInErrors.8 = Counter32: 0
IF-MIB::ifInErrors.9 = Counter32: 0
IF-MIB::ifInErrors.10 = Counter32: 0
IF-MIB::ifInErrors.11 = Counter32: 0
IF-MIB::ifInErrors.12 = Counter32: 0
IF-MIB::ifInUnknownProtos.1 = Counter32: 0
IF-MIB::ifInUnknownProtos.2 = Counter32: 0
IF-MIB::ifInUnknownProtos.3 = Counter32: 0
IF-MIB::ifInUnknownProtos.4 = Counter32: 0
IF-MIB::ifInUnknownProtos.5 = Counter32: 0
IF-MIB::ifInUnknownProtos.6 = Counter32: 0
IF-MIB::ifInUnknownProtos.7 = Counter32: 0
IF-MIB::ifInUnknownProtos.8 = Counter32: 0
IF-MIB::ifInUnknownProtos.9 = Counter32: 0
IF-MIB::ifInUnknownProtos.10 = Counter32: 0
IF-MIB::ifInUnknownProtos.11 = Counter32: 0
IF-MIB::ifInUnknownProtos.12 = Counter32: 0
IF-MIB::ifOutOctets.1 = Counter32: 0
IF-MIB::ifOutOctets.2 = Counter32: 0
IF-MIB::ifOutOctets.3 = Counter32: 0
IF-MIB::ifOutOctets.4 = Counter32: 0
IF-MIB::ifOutOctets.5 = Counter32: 0
IF-MIB::ifOutOctets.6 = Counter32: 0
IF-MIB::ifOutOctets.7 = Counter32: 0
IF-MIB::ifOutOctets.8 = Counter32: 0
IF-MIB::ifOutOctets.9 = Counter32: 0
IF-MIB::ifOutOctets.10 = Counter32: 0
IF-MIB::ifOutOctets.11 = Counter32: 0
IF-MIB::ifOutOctets.12 = Counter32: 0
IF-MIB::ifOutUcastPkts.1 = Counter32: 0
IF-MIB::ifOutUcastPkts.2 = Counter32: 0
IF-MIB::ifOutUcastPkts.3 = Counter32: 0
IF-MIB::ifOutUcastPkts.4 = Counter32: 0
IF-MIB::ifOutUcastPkts.5 = Counter32: 1901160
IF-MIB::ifOutUcastPkts.6 = Counter32: 251116
IF-MIB::ifOutUcastPkts.7 = Counter32: 251118
IF-MIB::ifOutUcastPkts.8 = Counter32: 0
IF-MIB::ifOutUcastPkts.9 = Counter32: 692480894
IF-MIB::ifOutUcastPkts.10 = Counter32: 446201368
IF-MIB::ifOutUcastPkts.11 = Counter32: 594838996
IF-MIB::ifOutUcastPkts.12 = Counter32: 0
IF-MIB::ifOutNUcastPkts.1 = Counter32: 0
IF-MIB::ifOutNUcastPkts.2 = Counter32: 0
IF-MIB::ifOutNUcastPkts.3 = Counter32: 0
IF-MIB::ifOutNUcastPkts.4 = Counter32: 0
IF-MIB::ifOutNUcastPkts.5 = Counter32: 0
IF-MIB::ifOutNUcastPkts.6 = Counter32: 0
IF-MIB::ifOutNUcastPkts.7 = Counter32: 0
IF-MIB::ifOutNUcastPkts.8 = Counter32: 0
IF-MIB::ifOutNUcastPkts.9 = Counter32: 0
IF-MIB::ifOutNUcastPkts.10 = Counter32: 0
IF-MIB::ifOutNUcastPkts.11 = Counter32: 0
IF-MIB::ifOutNUcastPkts.12 = Counter32: 0
IF-MIB::ifOutDiscards.1 = Counter32: 0
IF-MIB::ifOutDiscards.2 = Counter32: 0
IF-MIB::ifOutDiscards.3 = Counter32: 0
IF-MIB::ifOutDiscards.4 = Counter32: 0
IF-MIB::ifOutDiscards.5 = Counter32: 0
IF-MIB::ifOutDiscards.6 = Counter32: 0
IF-MIB::ifOutDiscards.7 = Counter32: 0
IF-MIB::ifOutDiscards.8 = Counter32: 0
IF-MIB::ifOutDiscards.9 = Counter32: 0
IF-MIB::ifOutDiscards.10 = Counter32: 0
IF-MIB::ifOutDiscards.11 = Counter32: 0
IF-MIB::ifOutDiscards.12 = Counter32: 0
IF-MIB::ifOutErrors.1 = Counter32: 0
IF-MIB::ifOutErrors.2 = Counter32: 0
IF-MIB::ifOutErrors.3 = Counter32: 0
IF-MIB::ifOutErrors.4 = Counter32: 0
IF-MIB::ifOutErrors.5 = Counter32: 0
IF-MIB::ifOutErrors.6 = Counter32: 0
IF-MIB::ifOutErrors.7 = Counter32: 0
IF-MIB::ifOutErrors.8 = Counter32: 0
IF-MIB::ifOutErrors.9 = Counter32: 0
IF-MIB::ifOutErrors.10 = Counter32: 0
IF-MIB::ifOutErrors.11 = Counter32: 0
IF-MIB::ifOutErrors.12 = Counter32: 0
IF-MIB::ifOutQLen.1 = Gauge32: 0
IF-MIB::ifOutQLen.2 = Gauge32: 0
IF-MIB::ifOutQLen.3 = Gauge32: 0
IF-MIB::ifOutQLen.4 = Gauge32: 0
IF-MIB::ifOutQLen.5 = Gauge32: 0
IF-MIB::ifOutQLen.6 = Gauge32: 0
IF-MIB::ifOutQLen.7 = Gauge32: 0
IF-MIB::ifOutQLen.8 = Gauge32: 0
IF-MIB::ifOutQLen.9 = Gauge32: 0
IF-MIB::ifOutQLen.10 = Gauge32: 0
IF-MIB::ifOutQLen.11 = Gauge32: 0
IF-MIB::ifOutQLen.12 = Gauge32: 0
IF-MIB::ifSpecific.1 = OID: SNMPv2-SMI::zeroDotZero
IF-MIB::ifSpecific.2 = OID: SNMPv2-SMI::zeroDotZero
IF-MIB::ifSpecific.3 = OID: SNMPv2-SMI::zeroDotZero
IF-MIB::ifSpecific.4 = OID: SNMPv2-SMI::zeroDotZero
IF-MIB::ifSpecific.5 = OID: SNMPv2-SMI::zeroDotZero
IF-MIB::ifSpecific.6 = OID: SNMPv2-SMI::zeroDotZero
IF-MIB::ifSpecific.7 = OID: SNMPv2-SMI::zeroDotZero
IF-MIB::ifSpecific.8 = OID: SNMPv2-SMI::zeroDotZero
IF-MIB::ifSpecific.9 = OID: SNMPv2-SMI::zeroDotZero
IF-MIB::ifSpecific.10 = OID: SNMPv2-SMI::zeroDotZero
IF-MIB::ifSpecific.11 = OID: SNMPv2-SMI::zeroDotZero
IF-MIB::ifSpecific.12 = OID: SNMPv2-SMI::zeroDotZero
SNMPv2-MIB::snmpInPkts.0 = Counter32: 709
SNMPv2-MIB::snmpOutPkts.0 = Counter32: 0
SNMPv2-MIB::snmpInBadVersions.0 = Counter32: 0
SNMPv2-MIB::snmpInBadCommunityNames.0 = Counter32: 0
SNMPv2-MIB::snmpInBadCommunityUses.0 = Counter32: 0
SNMPv2-MIB::snmpInASNParseErrs.0 = Counter32: 0
SNMPv2-MIB::snmpInTooBigs.0 = Counter32: 0
SNMPv2-MIB::snmpInNoSuchNames.0 = Counter32: 0
SNMPv2-MIB::snmpInBadValues.0 = Counter32: 0
SNMPv2-MIB::snmpInReadOnlys.0 = Counter32: 0
SNMPv2-MIB::snmpInGenErrs.0 = Counter32: 0
SNMPv2-MIB::snmpInTotalReqVars.0 = Counter32: 0
SNMPv2-MIB::snmpInTotalSetVars.0 = Counter32: 0
SNMPv2-MIB::snmpInGetRequests.0 = Counter32: 0
SNMPv2-MIB::snmpInGetNexts.0 = Counter32: 0
SNMPv2-MIB::snmpInSetRequests.0 = Counter32: 0
SNMPv2-MIB::snmpInGetResponses.0 = Counter32: 0
SNMPv2-MIB::snmpInTraps.0 = Counter32: 0
SNMPv2-MIB::snmpOutTooBigs.0 = Counter32: 0
SNMPv2-MIB::snmpOutNoSuchNames.0 = Counter32: 0
SNMPv2-MIB::snmpOutBadValues.0 = Counter32: 0
SNMPv2-MIB::snmpOutGenErrs.0 = Counter32: 0
SNMPv2-MIB::snmpOutSetRequests.0 = Counter32: 0
SNMPv2-MIB::snmpOutGetResponses.0 = Counter32: 0
SNMPv2-MIB::snmpOutTraps.0 = Counter32: 0
SNMPv2-MIB::snmpEnableAuthenTraps.0 = INTEGER: enabled(1)
SNMPv2-MIB::snmpSilentDrops.0 = Counter32: 0
SNMPv2-MIB::snmpProxyDrops.0 = Counter32: 0
IF-MIB::ifName.1 = STRING: ge1
IF-MIB::ifName.2 = STRING: ge2
IF-MIB::ifName.3 = STRING: ge3
IF-MIB::ifName.4 = STRING: ge4
IF-MIB::ifName.5 = STRING: ge5
IF-MIB::ifName.6 = STRING: ge6
IF-MIB::ifName.7 = STRING: ge7
IF-MIB::ifName.8 = STRING: ge8
IF-MIB::ifName.9 = STRING: tw1
IF-MIB::ifName.10 = STRING: tw2
IF-MIB::ifName.11 = STRING: tg1
IF-MIB::ifName.12 = STRING: tg2
IF-MIB::ifInMulticastPkts.1 = Counter32: 0
IF-MIB::ifInMulticastPkts.2 = Counter32: 0
IF-MIB::ifInMulticastPkts.3 = Counter32: 0
IF-MIB::ifInMulticastPkts.4 = Counter32: 0
IF-MIB::ifInMulticastPkts.5 = Counter32: 0
IF-MIB::ifInMulticastPkts.6 = Counter32: 0
IF-MIB::ifInMulticastPkts.7 = Counter32: 0
IF-MIB::ifInMulticastPkts.8 = Counter32: 0
IF-MIB::ifInMulticastPkts.9 = Counter32: 0
IF-MIB::ifInMulticastPkts.10 = Counter32: 0
IF-MIB::ifInMulticastPkts.11 = Counter32: 0
IF-MIB::ifInMulticastPkts.12 = Counter32: 0
IF-MIB::ifInBroadcastPkts.1 = Counter32: 0
IF-MIB::ifInBroadcastPkts.2 = Counter32: 0
IF-MIB::ifInBroadcastPkts.3 = Counter32: 0
IF-MIB::ifInBroadcastPkts.4 = Counter32: 0
IF-MIB::ifInBroadcastPkts.5 = Counter32: 0
IF-MIB::ifInBroadcastPkts.6 = Counter32: 0
IF-MIB::ifInBroadcastPkts.7 = Counter32: 0
IF-MIB::ifInBroadcastPkts.8 = Counter32: 0
IF-MIB::ifInBroadcastPkts.9 = Counter32: 0
IF-MIB::ifInBroadcastPkts.10 = Counter32: 0
IF-MIB::ifInBroadcastPkts.11 = Counter32: 0
IF-MIB::ifInBroadcastPkts.12 = Counter32: 0
IF-MIB::ifOutMulticastPkts.1 = Counter32: 0
IF-MIB::ifOutMulticastPkts.2 = Counter32: 0
IF-MIB::ifOutMulticastPkts.3 = Counter32: 0
IF-MIB::ifOutMulticastPkts.4 = Counter32: 0
IF-MIB::ifOutMulticastPkts.5 = Counter32: 0
IF-MIB::ifOutMulticastPkts.6 = Counter32: 0
IF-MIB::ifOutMulticastPkts.7 = Counter32: 0
IF-MIB::ifOutMulticastPkts.8 = Counter32: 0
IF-MIB::ifOutMulticastPkts.9 = Counter32: 0
IF-MIB::ifOutMulticastPkts.10 = Counter32: 0
IF-MIB::ifOutMulticastPkts.11 = Counter32: 0
IF-MIB::ifOutMulticastPkts.12 = Counter32: 0
IF-MIB::ifOutBroadcastPkts.1 = Counter32: 0
IF-MIB::ifOutBroadcastPkts.2 = Counter32: 0
IF-MIB::ifOutBroadcastPkts.3 = Counter32: 0
IF-MIB::ifOutBroadcastPkts.4 = Counter32: 0
IF-MIB::ifOutBroadcastPkts.5 = Counter32: 0
IF-MIB::ifOutBroadcastPkts.6 = Counter32: 0
IF-MIB::ifOutBroadcastPkts.7 = Counter32: 0
IF-MIB::ifOutBroadcastPkts.8 = Counter32: 0
IF-MIB::ifOutBroadcastPkts.9 = Counter32: 0
IF-MIB::ifOutBroadcastPkts.10 = Counter32: 0
IF-MIB::ifOutBroadcastPkts.11 = Counter32: 0
IF-MIB::ifOutBroadcastPkts.12 = Counter32: 0
IF-MIB::ifHCInOctets.1 = Counter64: 0
IF-MIB::ifHCInOctets.2 = Counter64: 0
IF-MIB::ifHCInOctets.3 = Counter64: 0
IF-MIB::ifHCInOctets.4 = Counter64: 0
IF-MIB::ifHCInOctets.5 = Counter64: 0
IF-MIB::ifHCInOctets.6 = Counter64: 0
IF-MIB::ifHCInOctets.7 = Counter64: 0
IF-MIB::ifHCInOctets.8 = Counter64: 0
IF-MIB::ifHCInOctets.9 = Counter64: 0
IF-MIB::ifHCInOctets.10 = Counter64: 0
IF-MIB::ifHCInOctets.11 = Counter64: 0
IF-MIB::ifHCInOctets.12 = Counter64: 0
IF-MIB::ifHCInUcastPkts.1 = Counter64: 0
IF-MIB::ifHCInUcastPkts.2 = Counter64: 0
IF-MIB::ifHCInUcastPkts.3 = Counter64: 0
IF-MIB::ifHCInUcastPkts.4 = Counter64: 0
IF-MIB::ifHCInUcastPkts.5 = Counter64: 989337
IF-MIB::ifHCInUcastPkts.6 = Counter64: 30439
IF-MIB::ifHCInUcastPkts.7 = Counter64: 30441
IF-MIB::ifHCInUcastPkts.8 = Counter64: 0
IF-MIB::ifHCInUcastPkts.9 = Counter64: 94387325
IF-MIB::ifHCInUcastPkts.10 = Counter64: 1278514941
IF-MIB::ifHCInUcastPkts.11 = Counter64: 361071932
IF-MIB::ifHCInUcastPkts.12 = Counter64: 0
IF-MIB::ifHCInMulticastPkts.1 = Counter64: 0
IF-MIB::ifHCInMulticastPkts.2 = Counter64: 0
IF-MIB::ifHCInMulticastPkts.3 = Counter64: 0
IF-MIB::ifHCInMulticastPkts.4 = Counter64: 0
IF-MIB::ifHCInMulticastPkts.5 = Counter64: 0
IF-MIB::ifHCInMulticastPkts.6 = Counter64: 0
IF-MIB::ifHCInMulticastPkts.7 = Counter64: 0
IF-MIB::ifHCInMulticastPkts.8 = Counter64: 0
IF-MIB::ifHCInMulticastPkts.9 = Counter64: 0
IF-MIB::ifHCInMulticastPkts.10 = Counter64: 0
IF-MIB::ifHCInMulticastPkts.11 = Counter64: 0
IF-MIB::ifHCInMulticastPkts.12 = Counter64: 0
IF-MIB::ifHCInBroadcastPkts.1 = Counter64: 0
IF-MIB::ifHCInBroadcastPkts.2 = Counter64: 0
IF-MIB::ifHCInBroadcastPkts.3 = Counter64: 0
IF-MIB::ifHCInBroadcastPkts.4 = Counter64: 0
IF-MIB::ifHCInBroadcastPkts.5 = Counter64: 0
IF-MIB::ifHCInBroadcastPkts.6 = Counter64: 0
IF-MIB::ifHCInBroadcastPkts.7 = Counter64: 0
IF-MIB::ifHCInBroadcastPkts.8 = Counter64: 0
IF-MIB::ifHCInBroadcastPkts.9 = Counter64: 0
IF-MIB::ifHCInBroadcastPkts.10 = Counter64: 0
IF-MIB::ifHCInBroadcastPkts.11 = Counter64: 0
IF-MIB::ifHCInBroadcastPkts.12 = Counter64: 0
IF-MIB::ifHCOutOctets.1 = Counter64: 0
IF-MIB::ifHCOutOctets.2 = Counter64: 0
IF-MIB::ifHCOutOctets.3 = Counter64: 0
IF-MIB::ifHCOutOctets.4 = Counter64: 0
IF-MIB::ifHCOutOctets.5 = Counter64: 0
IF-MIB::ifHCOutOctets.6 = Counter64: 0
IF-MIB::ifHCOutOctets.7 = Counter64: 0
IF-MIB::ifHCOutOctets.8 = Counter64: 0
IF-MIB::ifHCOutOctets.9 = Counter64: 0
IF-MIB::ifHCOutOctets.10 = Counter64: 0
IF-MIB::ifHCOutOctets.11 = Counter64: 0
IF-MIB::ifHCOutOctets.12 = Counter64: 0
IF-MIB::ifHCOutUcastPkts.1 = Counter64: 0
IF-MIB::ifHCOutUcastPkts.2 = Counter64: 0
IF-MIB::ifHCOutUcastPkts.3 = Counter64: 0
IF-MIB::ifHCOutUcastPkts.4 = Counter64: 0
IF-MIB::ifHCOutUcastPkts.5 = Counter64: 1901160
IF-MIB::ifHCOutUcastPkts.6 = Counter64: 251116
IF-MIB::ifHCOutUcastPkts.7 = Counter64: 251118
IF-MIB::ifHCOutUcastPkts.8 = Counter64: 0
IF-MIB::ifHCOutUcastPkts.9 = Counter64: 692480894
IF-MIB::ifHCOutUcastPkts.10 = Counter64: 446201368
IF-MIB::ifHCOutUcastPkts.11 = Counter64: 594838996
IF-MIB::ifHCOutUcastPkts.12 = Counter64: 0
IF-MIB::ifHCOutMulticastPkts.1 = Counter64: 0
IF-MIB::ifHCOutMulticastPkts.2 = Counter64: 0
IF-MIB::ifHCOutMulticastPkts.3 = Counter64: 0
IF-MIB::ifHCOutMulticastPkts.4 = Counter64: 0
IF-MIB::ifHCOutMulticastPkts.5 = Counter64: 0
IF-MIB::ifHCOutMulticastPkts.6 = Counter64: 0
IF-MIB::ifHCOutMulticastPkts.7 = Counter64: 0
IF-MIB::ifHCOutMulticastPkts.8 = Counter64: 0
IF-MIB::ifHCOutMulticastPkts.9 = Counter64: 0
IF-MIB::ifHCOutMulticastPkts.10 = Counter64: 0
IF-MIB::ifHCOutMulticastPkts.11 = Counter64: 0
IF-MIB::ifHCOutMulticastPkts.12 = Counter64: 0
IF-MIB::ifHCOutBroadcastPkts.1 = Counter64: 0
IF-MIB::ifHCOutBroadcastPkts.2 = Counter64: 0
IF-MIB::ifHCOutBroadcastPkts.3 = Counter64: 0
IF-MIB::ifHCOutBroadcastPkts.4 = Counter64: 0
IF-MIB::ifHCOutBroadcastPkts.5 = Counter64: 0
IF-MIB::ifHCOutBroadcastPkts.6 = Counter64: 0
IF-MIB::ifHCOutBroadcastPkts.7 = Counter64: 0
IF-MIB::ifHCOutBroadcastPkts.8 = Counter64: 0
IF-MIB::ifHCOutBroadcastPkts.9 = Counter64: 0
IF-MIB::ifHCOutBroadcastPkts.10 = Counter64: 0
IF-MIB::ifHCOutBroadcastPkts.11 = Counter64: 0
IF-MIB::ifHCOutBroadcastPkts.12 = Counter64: 0
IF-MIB::ifLinkUpDownTrapEnable.1 = INTEGER: enabled(1)
IF-MIB::ifLinkUpDownTrapEnable.2 = INTEGER: enabled(1)
IF-MIB::ifLinkUpDownTrapEnable.3 = INTEGER: enabled(1)
IF-MIB::ifLinkUpDownTrapEnable.4 = INTEGER: enabled(1)
IF-MIB::ifLinkUpDownTrapEnable.5 = INTEGER: enabled(1)
IF-MIB::ifLinkUpDownTrapEnable.6 = INTEGER: enabled(1)
IF-MIB::ifLinkUpDownTrapEnable.7 = INTEGER: enabled(1)
IF-MIB::ifLinkUpDownTrapEnable.8 = INTEGER: enabled(1)
IF-MIB::ifLinkUpDownTrapEnable.9 = INTEGER: enabled(1)
IF-MIB::ifLinkUpDownTrapEnable.10 = INTEGER: enabled(1)
IF-MIB::ifLinkUpDownTrapEnable.11 = INTEGER: enabled(1)
IF-MIB::ifLinkUpDownTrapEnable.12 = INTEGER: enabled(1)
IF-MIB::ifHighSpeed.1 = Gauge32: 0
IF-MIB::ifHighSpeed.2 = Gauge32: 0
IF-MIB::ifHighSpeed.3 = Gauge32: 0
IF-MIB::ifHighSpeed.4 = Gauge32: 0
IF-MIB::ifHighSpeed.5 = Gauge32: 1000
IF-MIB::ifHighSpeed.6 = Gauge32: 1000
IF-MIB::ifHighSpeed.7 = Gauge32: 1000
IF-MIB::ifHighSpeed.8 = Gauge32: 0
IF-MIB::ifHighSpeed.9 = Gauge32: 1000
IF-MIB::ifHighSpeed.10 = Gauge32: 1000
IF-MIB::ifHighSpeed.11 = Gauge32: 10000
IF-MIB::ifHighSpeed.12 = Gauge32: 0
IF-MIB::ifPromiscuousMode.1 = INTEGER: false(2)
IF-MIB::ifPromiscuousMode.2 = INTEGER: false(2)
IF-MIB::ifPromiscuousMode.3 = INTEGER: false(2)
IF-MIB::ifPromiscuousMode.4 = INTEGER: false(2)
IF-MIB::ifPromiscuousMode.5 = INTEGER: false(2)
IF-MIB::ifPromiscuousMode.6 = INTEGER: false(2)
IF-MIB::ifPromiscuousMode.7 = INTEGER: false(2)
IF-MIB::ifPromiscuousMode.8 = INTEGER: false(2)
IF-MIB::ifPromiscuousMode.9 = INTEGER: false(2)
IF-MIB::ifPromiscuousMode.10 = INTEGER: false(2)
IF-MIB::ifPromiscuousMode.11 = INTEGER: false(2)
IF-MIB::ifPromiscuousMode.12 = INTEGER: false(2)
IF-MIB::ifConnectorPresent.1 = INTEGER: false(2)
IF-MIB::ifConnectorPresent.2 = INTEGER: false(2)
IF-MIB::ifConnectorPresent.3 = INTEGER: false(2)
IF-MIB::ifConnectorPresent.4 = INTEGER: false(2)
IF-MIB::ifConnectorPresent.5 = INTEGER: true(1)
IF-MIB::ifConnectorPresent.6 = INTEGER: true(1)
IF-MIB::ifConnectorPresent.7 = INTEGER: true(1)
IF-MIB::ifConnectorPresent.8 = INTEGER: false(2)
IF-MIB::ifConnectorPresent.9 = INTEGER: true(1)
IF-MIB::ifConnectorPresent.10 = INTEGER: true(1)
IF-MIB::ifConnectorPresent.11 = INTEGER: true(1)
IF-MIB::ifConnectorPresent.12 = INTEGER: false(2)
IF-MIB::ifAlias.1 = STRING: GigabitEthernet1
IF-MIB::ifAlias.2 = STRING: GigabitEthernet2
IF-MIB::ifAlias.3 = STRING: GigabitEthernet3
IF-MIB::ifAlias.4 = STRING: GigabitEthernet4
IF-MIB::ifAlias.5 = STRING: GigabitEthernet5
IF-MIB::ifAlias.6 = STRING: GigabitEthernet6
IF-MIB::ifAlias.7 = STRING: GigabitEthernet7
IF-MIB::ifAlias.8 = STRING: GigabitEthernet8
IF-MIB::ifAlias.9 = STRING: TwoPointFiveGigabitEthernet1
IF-MIB::ifAlias.10 = STRING: TwoPointFiveGigabitEthernet2
IF-MIB::ifAlias.11 = STRING: TenGigabitEthernet1
IF-MIB::ifAlias.12 = STRING: TenGigabitEthernet2
IF-MIB::ifCounterDiscontinuityTime.1 = Timeticks: (0) 0:00:00.00
IF-MIB::ifCounterDiscontinuityTime.2 = Timeticks: (0) 0:00:00.00
IF-MIB::ifCounterDiscontinuityTime.3 = Timeticks: (0) 0:00:00.00
IF-MIB::ifCounterDiscontinuityTime.4 = Timeticks: (0) 0:00:00.00
IF-MIB::ifCounterDiscontinuityTime.5 = Timeticks: (0) 0:00:00.00
IF-MIB::ifCounterDiscontinuityTime.6 = Timeticks: (0) 0:00:00.00
IF-MIB::ifCounterDiscontinuityTime.7 = Timeticks: (0) 0:00:00.00
IF-MIB::ifCounterDiscontinuityTime.8 = Timeticks: (0) 0:00:00.00
IF-MIB::ifCounterDiscontinuityTime.9 = Timeticks: (0) 0:00:00.00
IF-MIB::ifCounterDiscontinuityTime.10 = Timeticks: (0) 0:00:00.00
IF-MIB::ifCounterDiscontinuityTime.11 = Timeticks: (0) 0:00:00.00
IF-MIB::ifCounterDiscontinuityTime.12 = Timeticks: (0) 0:00:00.00
```

</details>


### print_stats

ROS node that uses `ZyxelAPI` to print switch statistics to console.

#### Parameters
- `~address` (str): Address of the HTTP API (including 'http://').
- `~password` (str): Password for the HTTP API.
- `~rate` (float): Printing frequency in Hz.
- `~clear_screen` (bool, default False): If true, a clear screen command will be printed before each iteration.
- `~num_prints` (int, default 0): If nonzero, this is the number of prints after which the node exits.
- `~demo_port_info` (bool, default False): If true, `~port_info` will be populated with a demonstration content.
- `~port_info` (dict): Extra configuration of switch ports. Keys are port names (e.g. `GigabitEthernet1`) and values
                       are dicts. These dicts can contain the following keys:
                       `name`: This is an alias of the port reported as `ifAlias` IF-MIB value.
                       `speed`: Desired speed of the port in bps. If the runtime speed is different, an error is
                                printed.

#### Example output

```
-------------------------------------------------------------------
               port |  status  | Rx (kpkts) | Tx (kpkts) |  loop  | 
   GigabitEthernet1 |     Down |          0 |          0 |  False | 
   GigabitEthernet2 |     Down |          0 |          0 |  False | 
   GigabitEthernet3 |     Down |          0 |          0 |  False | 
   GigabitEthernet4 |     Down |          0 |          0 |  False | 
             Bullet |   1 Gbps |        989 |       1901 |  False | 
              Cam 6 |   1 Gbps |         30 |        251 |  False | 
              Cam 7 |   1 Gbps |         30 |        251 |  False | 
            Top Box |     Down |          0 |          0 |  False | 
                IEI |   1 Gbps |      94387 |     692480 |  False | 
                NUC |   1 Gbps |    1278514 |     446201 |  False | 
             Jetson |  10 Gbps |     361071 |     594838 |  False | 
TenGigabitEthernet2 |     Down |          0 |          0 |  False | 
```