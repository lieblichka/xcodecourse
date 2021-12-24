#!/usr/bin/env python

import scapy.all as scapy 
import argparse 
import re 

def scan_network(options):
	if options.net_type == "ether":
		return scan_Ether_Broadcast(options.target) 
	elif options.net_type == "wlan":
		return scan_Wireless_Hosts(options.target)
	elif options.net_type == "wlan-lucky":
		return scan_Wireless_Hosts_Lucky(options.target)
	else:
		return None


def scan_Wireless_Hosts(ip):
	print(ip)
	if ip == None:
		return None
	clients_list = []
	if re.search(r"[/\s]\d\d", ip)[0] == "/24":
		ipv4_partial = re.search(r"\d{,3}.\d{,3}.\d{,3}.", ip)[0]
		arp_packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")/scapy.ARP(op=1, 
			hwlen=6, plen=4)
		for host in range(1,254):
			arp_packet.pdst = ipv4_partial + str(host)
			print(arp_packet.pdst)
			ans = scapy.srp1(arp_packet, timeout=0.5, verbose=False)
			if ans:
				client_dict = {"ip" : ans[0].psrc, "mac": ans[0].hwsrc}
				print(client_dict)
				clients_list.append(client_dict)

	return clients_list

def scan_Wireless_Hosts_Lucky(ip):
	print(ip)
	if ip == None:
		return None
	clients_list = []
	if re.search(r"[/\s]\d\d", ip)[0] == "/24":
		ipv4_partial = re.search(r"\d{,3}.\d{,3}.\d{,3}.", ip)[0]
		arp_packet = scapy.Ether()/scapy.ARP(op=1, hwlen=6, plen=4)
		arp_packet.dst = "ff:ff:ff:ff:ff:ff"
		arp_packet.hwdst = scapy.getmacbyip(ipv4_partial + '1')
		for host in range(1,254):
			arp_packet.pdst = ipv4_partial + str(host)
			print(arp_packet.pdst)
			ans = scapy.srp1(arp_packet, timeout=2, verbose=False)
			if ans:
				client_dict = {"ip" : ans[0].psrc, "mac": ans[0].hwsrc}
				print(client_dict)
				clients_list.append(client_dict)

	return clients_list


def scan_Ether_Broadcast(ip):
	if ip == None:
		return None
	arp_request = scapy.ARP(pdst=ip)
	broadcast = scapy.Ether()
	broadcast.dst = "ff:ff:ff:ff:ff:ff"
	broadcast.src = scapy.get_if_hwaddr(scapy.conf.iface) 
		
	arp_request_broadcast = broadcast/arp_request
	answered = scapy.srp(arp_request_broadcast, verbose=False,
		timeout=20,inter=0.1)[0]

	clients_list = []
	for element in answered:
		client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
		clients_list.append(client_dict)
	return clients_list

def print_result(results_list):
	if results_list:
		print("IP\t\t\tMAC address\n------------------------------------")
		for client in results_list:
			print(client["ip"] + "\t\t" + client["mac"])	
	else:
		print("Incorrect format")

def get_arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument("-t", "--target", dest="target",
		help="Target IP / IP range.")
	parser.add_argument("-nT", "--network_type", dest="net_type",
		help="Network Type: ether/wlan")
	options = parser.parse_args()
	return (options)

options = get_arguments()
scan_result = scan_network(options)
print_result(scan_result)


