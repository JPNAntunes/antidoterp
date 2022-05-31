# A(ntidote)RP

Python script that defends against basic forms of ARP Poisoning attacks. This defence locks a MAC Address to a specific IP Address, any packet coming from that IP Address that has a different MAC Address is dropped and a log is generated.

------------

## Rule Creation

User provides an IP and MAC Address that will be used to create an IPTables firewall rule to drop any packets coming from a different MAC Address.

## Monitoring

Script will read kernel.log file continuously and will alert the user in case of any ARP Poisoning attacks.
