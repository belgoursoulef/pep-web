
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:05:c3:50 brd ff:ff:ff:ff:ff:ff
    inet 192.168.32.50/28 brd 192.168.32.63 scope global noprefixroute enp0s3
       valid_lft forever preferred_lft forever
    inet6 fe80::cb60:129e:dafa:916/64 scope link noprefixroute 
       valid_lft forever preferred_lft forever
3: br-1a766cc4740b: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default 
    link/ether 26:99:bb:10:1d:a9 brd ff:ff:ff:ff:ff:ff
    inet 172.18.0.1/16 brd 172.18.255.255 scope global br-1a766cc4740b
       valid_lft forever preferred_lft forever
    inet6 fe80::2499:bbff:fe10:1da9/64 scope link 
       valid_lft forever preferred_lft forever
4: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN group default 
    link/ether 4e:c7:b4:b7:1a:d3 brd ff:ff:ff:ff:ff:ff
    inet 172.17.0.1/16 brd 172.17.255.255 scope global docker0
       valid_lft forever preferred_lft forever
13: veth8968d66@if2: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master br-1a766cc4740b state UP group default 
    link/ether ca:98:b4:f6:c5:8e brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet6 fe80::c898:b4ff:fef6:c58e/64 scope link 
       valid_lft forever preferred_lft forever
14: veth605723c@if2: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master br-1a766cc4740b state UP group default 
    link/ether 12:ff:b2:2e:a2:48 brd ff:ff:ff:ff:ff:ff link-netnsid 1
    inet6 fe80::10ff:b2ff:fe2e:a248/64 scope link 
       valid_lft forever preferred_lft forever


juin 19 13:20:40 rt-mv dhcpd[36999]: Listening on LPF/enp0s3/08:00:27:05:c3:50/192.168.32.48/28
juin 19 13:20:40 rt-mv sh[36999]: Listening on LPF/enp0s3/08:00:27:05:c3:50/192.168.32.48/28
juin 19 13:20:40 rt-mv sh[36999]: Sending on   LPF/enp0s3/08:00:27:05:c3:50/192.168.32.48/28
juin 19 13:20:40 rt-mv sh[36999]: Sending on   Socket/fallback/fallback-net
juin 19 13:20:40 rt-mv dhcpd[36999]: Sending on   LPF/enp0s3/08:00:27:05:c3:50/192.168.32.48/28
juin 19 13:20:40 rt-mv dhcpd[36999]: Sending on   Socket/fallback/fallback-net
juin 19 13:20:40 rt-mv dhcpd[36999]: Server starting service.
juin 19 13:20:43 rt-mv dhcpd[36999]: DHCPDISCOVER from 00:02:d1:4b:20:f8 via 192.168.32.97: unknown network segment
juin 19 13:20:43 rt-mv dhcpd[36999]: DHCPDISCOVER from 00:02:d1:57:4e:78 via 192.168.32.97: unknown network segment
juin 19 13:20:46 rt-mv dhcpd[36999]: DHCPDISCOVER from 00:02:d1:57:4e:78 via 192.168.32.97: unknown network segment
