#!/usr/bin/env python3
# ------------------------------------------------------------
#       A(ntidote)RP - Defence against ARP Poisoning
# Basic Python Script to detect and prevent ARP Poisoning
# attacks. It has two main objectives:
# 1st -> Create an IPTables rule to lock an  IP Address to 
#      a MAC Address (aka MAC Address Locking).
# 2nd -> Monitor the log file to detect ARP Poisoning attacks.
#
# João Antunes, Portugal
# ------------------------------------------------------------
import os
import sys
import subprocess
import select

def monitorLogs():
	"""Monitors /var/log/kern.log file for IPTables logs alerting for the rules created by this script"""

	print("Monitoring IPTables logs for ARP Poisoning attacks...\n")
	# Spawns a new process to mon
	f = subprocess.Popen(["tail", "-f" , "-n 0", "/var/log/kern.log"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	# Polls object
	p = select.poll()
	# Register a file descriptor
	p.register(f.stdout)

	while True:
		if p.poll(1):
			# Decodes log to UTF-8
			log = f.stdout.readline().decode("utf-8")~
			# Checks if log line has been created by this Script
			if '[ARP Poison] Packet dropped' in log:
				print(log)

def createRule():
	"""User provides IP Address and MAC Address of the host being locked. IPTables rule is created to drop packets coming
	from a different MAC Address and generate a log."""
	
	# User needs to provide an IP Address
	while(1):
		print("Provide IP Address of the host (XXX.XXX.XXX.XXX)")
		ipAddress = input(">> ")
		if len(ipAddress.split(".")) == 4:
			break
	# User needs to provide a MAC Address
	while(1):
		print("Provide MAC Address of the host (XX:XX:XX:XX:XX:XX)")
		macAddress = input(">> ")
		if len(macAddress.split(":")) == 6:
			break
	# Removing IPTables rule for that IP and MAC Addresses to prevent duplicating rules
	os.system(f"sudo iptables -D INPUT -s {ipAddress} -i eth0 -m mac ! --mac-source {macAddress} -j LOG --log-prefix '[ARP Poison] Packet dropped'")
	os.system(f"sudo iptables -D INPUT -s {ipAddress} -i eth0 -m mac ! --mac-source {macAddress} -j DROP ")
	# Adding IPTables rule 
	os.system(f"sudo iptables -A INPUT -s {ipAddress} -i eth0 -m mac ! --mac-source {macAddress} -j LOG --log-prefix '[ARP Poison] Packet dropped'")
	os.system(f"sudo iptables -A INPUT -s {ipAddress} -i eth0 -m mac ! --mac-source {macAddress} -j DROP")
	print("Rule successfuly created!\n")
	# Go to the monitoring phase by default
	monitorLogs()


if __name__ == '__main__':
	# Basic Menu interaction to choose the option
	print("Welcome to the ARP Spoofing Antidote")
	print("1 - Create IPTables rule")
	print("2 - Monitor")
	while(1):
		option = input(">> ")
		if option == "1":
			createRule()
			break
		elif option == "2":
			monitorLogs()
			break
		else:
			print("Error! Write 1 to create a new IPTables rule and 2 to monitor IPTables logs.")
