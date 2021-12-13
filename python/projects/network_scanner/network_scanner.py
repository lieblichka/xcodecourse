#!/usr/bin/env python

import scapy.all as scapy # модуль сетевых протоколов 


def scany(ip):
	scapy.arping(ip)

def scan(ip):
	arp_request = scapy.ARP(pdst=ip) # метод создания ARP пакета
	broadcast = scapy.Ether( "ff:ff:ff:ff:ff:ff")
	
	
	arp_request_broadcast = broadcast/arp_request
	answered, unanswered = scapy.sr(arp_request_broadcast, timeout=1)
	print(answered.summary())
	#arp_request.show()
	#broadcast.show()
	#arp_request.pdst = ip # установка значения поля pdst 
	#scapy.ls(scapy.ARP()) # выводит инф. о полях пакета экз. класса ARP 
	# arp_request.summary выводит информацию о пакете


scan("192.168.0.1/24")

#scany("192.168.0.1")  # возвращает мак-адрес устройства по ip
#scany("192.168.0.1/24") # возвращает маки всех устройств подсети 

