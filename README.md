# A(ntidote)RP

Python script that defends against basic forms of ARP Poisoning attacks. This defense "locks" a MAC address to a specific IP address, any packet coming from that IP address that has a different MAC Address is dropped and a log is generated.

------------

## Rule Creation

This is the main function of this script, it asks the user to provide an IP and MAC address that will be used to create an IPTables firewall rule, this rule will drop any incoming packets that has the same IP address of the device but different MAC address.

## Monitoring

This is a secondary function, the function will read the kernel.log file (the file IPTables writes its logs to) continuously and will alert the user in case of any packets being dropped due to an ARP Poisoning attack.
