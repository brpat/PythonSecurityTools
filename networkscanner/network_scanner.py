import scapy.all as scapy
import sys
import optparse

'''Basic ARP scanner'''


def arp_scan_simple(ip):
	scapy.arping(ip)


def arp_scan(ip):
	#scapy.arping(ip)
	# Set destination ip. pdst can't be in cidr notation
	arp_request = scapy.ARP(pdst=ip)
	# Print packet summary
	# print(arp_request.summary())
	# scapy.ls(scapy.ARP())
	# Final packet appended / is for append in scapy
	arp_request_broadcast = arp_broadcast_gen()/arp_request
	# print(arp_request_broadcast.show())

	# Send packet to network. Returns multiple values (lists). Answered responses and unanswered responses.
	# timeout prevents infinite waiting time
	#answer, unanswered = scapy.srp(arp_request_broadcast, iface="ens38", timeout=1)1st way
	# 2nd way
	answer = scapy.srp(arp_request_broadcast, iface="ens38", timeout=1)[0]
	#print(answer.summary())
	arp_response = parse_arp_response(answer)
	print_result_nice_format(arp_response)
	

def parse_arp_response(response_list):
	arp_response = {}
	for element in response_list:
		#print(element[1].psrc)
		#print(element[1].hwsrc)
		# IP to MAC address mapping
		arp_response[element[1].psrc] = element[1].hwsrc
	return arp_response
		
	
def print_result_nice_format(data):
	print("*" * 100)
	print(f"{len(data)} packets captured from {len(data)} hosts.")
	print("-" * 100)
	print("IP\t\t\t\t\tAt MAC Address")
	for key, val in data.items():
		print(f"{key}\t\t\t\t{val}")
	 s


def arp_broadcast_gen():
	# Create an Ethernet Packet that will have a broadcats destination mac addr.
	broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
	#scapy.ls(scapy.Ether())
	return broadcast
	

def get_arguments():
	parser = optparse.OptionParser()
	parser.add_option("-t", "--target", "--iprange", dest="target", help="Target IP / IP range")
	(options, arguments) = parser.parse_args()
	return options


def main():
	options = get_arguments()
	arp_scan(options.target)



if __name__ == '__main__':
	main()
	
