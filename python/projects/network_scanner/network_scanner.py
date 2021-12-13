#!/usr/bin/env python

import scapy.all as scapy # модуль сетевых протоколов 


def scan(ip):
	scapy.arping(ip)

scan("192.168.0.143") 
