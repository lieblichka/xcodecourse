#!/usr/bin/env python

import subprocess # подключение модуля subprocess
import optparse  # модуль для продвинутого парсинга
import re # модуль регулярных выражений

def get_arguments(): # объявление функции
	parser = optparse.OptionParser() 
	# функция OptionParser() возвращает объект модуля optparse
	parser.add_option("-i", "--interface", dest="interface", 
		help="Interface to change its MAC address")
	# функция add_option объекта Parser
	# "-flag short", "--flag long",
	# - dest="interface" переменная для введенего значения String,
	# - help="" подсказка при неправильном вводе или флаге help
	parser.add_option("-m", "--mac`", dest="new_mac",
		help="New MAC address")
	(options, arguments) = parser.parse_args()
	if not options.interface: # если !interface
		parser.error("[-] Please specify an interface,\
	use --help for more info")
	elif not options.new_mac: # eсли !new_mac
		parser.error("[-] Please specify a new mac,\
	use --help for more info")
	return options

def change_mac(interface, new_mac):
	print("[+] Changing MAC address for " + interface + " to " + new_mac)
	subprocess.call(["ifconfig", interface, "down"])
	# функция выполнения системной команды модуля subprocess со списком 
	subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
	subprocess.call(["ifconfig", interface, "up"])

def get_current_mac(interface):
	ifconfig_result = subprocess.check_output(["ifconfig", interface],
	universal_newlines=True)
	# сохранение результата вывода функции в переменную

	#print(ifconfig_result) # вывод значения перменной на экран
	current_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
	# re.search - метод поиска совпадений по регулярному выражению 
	if current_mac:
		return current_mac.group(0)
	return None


options = get_arguments()
change_mac(options.interface, options.new_mac)
mac_address = get_current_mac(options.interface)
if mac_address:
	print ("Current mac address: " + mac_address)
else:
	print ("[-] Could not read mac address")
