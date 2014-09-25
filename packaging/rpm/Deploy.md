Flex GateWay Deploy
===================

install rpms
------------

1. install strongswan

2. install openvpn

3. install flexgw

setting sysctl.conf
-------------------

vim /etc/sysctl.conf

1. Disable redirects.

    sysctl -a | egrep "ipv4.*(accept|send)_redirects" | awk -F "=" '{print $1"= 0"}' >> /etc/sysctl.conf

2. enable ip forward.

    net.ipv4.ip_forward = 1

run flexgw
----------

1. ln -s /etc/init.d/initflexgw /etc/rc3.d/S98initflexgw

2. reboot
