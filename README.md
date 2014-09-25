Flex GateWay
============

介绍
-------

本程序提供了VPN、SNAT 基础服务。

主要提供以下几点功能：

1.  IPSec Site-to-Site 功能。可快速的帮助你将两个不同的VPC 私网以IPSec Site-to-Site 的方式连接起来。
2.  拨号VPN 功能。可让你通过拨号方式，接入VPC 私网，进行日常维护管理。
3.  SNAT 功能。可方便的设置Source NAT，以让VPC 私网内的VM 通过Gateway VM 访问外网。

软件组成
----------

Strongswan

* 版本：5.1.3
* Website：http://www.strongswan.org

OpenVPN

* 版本：2.3.2
* Website：https://openvpn.net/index.php/open-source.html

程序说明
-----------

ECS VPN（即本程序）

* 目录：/usr/local/flexgw
* 数据库文件：/usr/local/flexgw/instance/website.db
* 日志文件：/usr/local/flexgw/logs/website.log
* 启动脚本：/etc/init.d/flexgw 或/usr/local/flexgw/website_console
* 实用脚本：/usr/local/flexgw/scripts

「数据库文件」保存了我们所有的VPN 配置，建议定期备份。如果数据库损坏，可通过「实用脚本」目录下的initdb.py 脚本对数据库进行初始化，初始化之后所有的配置将清空。

Strongswan

* 目录：/etc/strongswan
* 日志文件：/var/log/strongswan.charon.log
* 启动脚本：/usr/sbin/strongswan

如果strongswan.conf 配置文件损坏，可使用备份文件/usr/local/flexgw/rc/strongswan.conf 进行覆盖恢复。

ipsec.conf 和ipsec.secrets 配置文件，由/usr/local/flexgw/website/vpn/sts/templates/sts 目录下的同名文件自动生成，请勿随便修改。

OpenVPN

* 目录：/etc/openvpn
* 日志文件：/etc/openvpn/openvpn.log
* 状态文件：/etc/openvpn/openvpn-status.log
* 启动脚本：/etc/init.d/openvpn

server.conf 配置文件，由/usr/local/flexgw/website/vpn/dial/templates/dial 目录下的同名文件自动生成，请勿随便修改。
