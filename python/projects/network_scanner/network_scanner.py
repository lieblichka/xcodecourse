#!/usr/bin/env python

import scapy.all as scapy # модуль сетевых протоколов 
import argparse # новейший модуль парсинга аргументов 

def scany(ip):
	scapy.arping(ip)

def scan(ip):
	if ip == None:
		return None
	arp_request = scapy.ARP(pdst=ip) # метод создания ARP пакета
	broadcast = scapy.Ether()
	broadcast.dst = "ff:ff:ff:ff:ff:ff"
	broadcast.src = scapy.get_if_hwaddr(scapy.conf.iface) 
		# определение исходного мак-адреса
	#broadcast.type = "ARP" # задание типа марщрутизации 
	
	
	arp_request_broadcast = broadcast/arp_request
	#arp_request_broadcast.show()
	answered = scapy.srp(arp_request_broadcast, verbose=False,
		timeout=10)[0]

	clients_list = []
	for element in answered:
		client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
		clients_list.append(client_dict)
		#print(element[1].psrc + "\t\t" + element[1].hwsrc) 
		# вывод ip и мак адресы полученных пакетов
	return clients_list
	#print(answered.summary())
	#arp_request.show()
	#broadcast.show()
	#arp_request.pdst = ip # установка значения поля pdst 
	#scapy.ls(scapy.ARP()) # выводит инф. о полях пакета экз. класса ARP 
	# arp_request.summary выводит информацию о пакете

def print_result(results_list):
	if results_list:
		print("IP\t\t\tMAC address\n-------------------------------------")	
		for client in results_list:
			print(client["ip"] + "\t\t" + client["mac"])	

def get_arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument("-t", "--target", dest="target",
		help="Target IP / IP range.")
	options = parser.parse_args()
	return (options)

options = get_arguments()
scan_result = scan(options.target)
print_result(scan_result)

#scany("192.168.0.1")  # возвращает мак-адрес устройства по ip
#scany("192.168.0.1/24") # возвращает маки всех устройств подсети 

