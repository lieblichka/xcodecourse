from scapy.all import *



arp_request = ARP(pdst="192.168.100.1/24")
broadcast = Ether() 
broadcast.dst = "ff:ff:ff:ff:ff:ff"
#broadcast.src = get_if_hwaddr("enp2s0")
#broadcast.type = "ARP"

arp_request_broadcast = broadcast/arp_request
arp_request_broadcast.show()
ans, unans = srp(arp_request_broadcast, timeout=10)

print(ans.summary())
