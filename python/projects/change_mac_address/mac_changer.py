#!/usr/bin/env python

import subprocess # подключение модуля subprocess
import optparse  # модуль для продвинутого парсинга


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


options = get_arguments()
#change_mac(options.interface, options.new_mac)
ifconfig_result = subprocess.check_output(["ifconfig", options.interface])
# сохранение результата вывода функции в переменную

print(ifconfig_resul) # вывод значения перменной на экран

