# --- GLOBAL OPTIONS ---
default-lease-time 600;
max-lease-time 7200;
authoritative;

# Déclaration de l'option 150 (TFTP server address - Cisco phones)
option option-150 code 150 = ip-address;

# --- HOST RESERVATIONS ---
host cam-IP8166 {
  hardware ethernet 00:02:D1:4B:20:F8;
  fixed-address 192.168.32.114;
}
host cam-FE8391-V {
  hardware ethernet 00:02:D1:57:4E:78;
  fixed-address 192.168.32.115;
}

# --- SUBNETS ---

# VLAN 21: PRODUCTION
subnet 192.168.32.0 netmask 255.255.255.240 {
  range 192.168.32.3 192.168.32.14;
  option routers 192.168.32.1;
  option domain-name-servers 10.0.0.1;
}

# VLAN 22: ADMINISTRATIF
subnet 192.168.32.16 netmask 255.255.255.240 {
  range 192.168.32.18 192.168.32.30;
  option routers 192.168.32.17;
  option domain-name-servers 10.0.0.1;
}

# VLAN 23: IT
subnet 192.168.32.32 netmask 255.255.255.240 {
  range 192.168.32.34 192.168.32.46;
  option routers 192.168.32.33;
  option domain-name-servers 10.0.0.1;
}

# VLAN 25: DCP
subnet 192.168.32.48 netmask 255.255.255.240 {
}

# VLAN 26: TELEPHONIE
subnet 192.168.32.80 netmask 255.255.255.240 {
  range 192.168.32.83 192.168.32.94;
  option routers 192.168.32.81;
  option option-150 192.168.32.82;
}

# VLAN 29: CAMERAS + subnet relay agent groupés
shared-network CAMERAS {

  # Subnet passerelle/switch (relay agent - 192.168.32.97)
  subnet 192.168.32.96 netmask 255.255.255.240 {
  }

  # VLAN 29: CAMERAS
  subnet 192.168.32.112 netmask 255.255.255.240 {
    range 192.168.32.116 192.168.32.125;
    option routers 192.168.32.113;
    option domain-name-servers 10.0.0.1;
  }

}
