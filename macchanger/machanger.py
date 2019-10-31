import subprocess
import sys
import optparse
import re


# Important MAC Address's first octet must be even
# Change mac address



def get_arguments():
	# Parser Object
	parser = optparse.OptionParser()
	parser.add_option("-i", "--interface", dest="interface", help="Interface to change its 		MAC address")
	parser.add_option("-m", "--mac", dest="macaddress", help="new MAC Address")
	#options = value arguments = arguments
	(options, arguments) = parser.parse_args()

	if not options.interface:
		parser.error("Invalid Arguments (Interface). Proper Syntax: python3 machanger.py -i <interface> -m <MAC Address>")
	elif not options.macaddress:
		parser.error("Invalid Arguments (Interface). Proper Syntax: python3 machanger.py -i <interface> -m <MAC Address>")
	else:
		return (options, arguments)
	


def change_mac(interface, macaddress):
	print(f"[+] Changing MAC address for {interface}")
	print(f"MAC Address for {interface} changed to {macaddress}")

	#subprocess.call("ifconfig", shell=True)
	subprocess.call(f"ifconfig {interface} down", shell=True)
	subprocess.call(f"ifconfig {interface} hw ether {macaddress}", shell=True)
	subprocess.call(f"ifconfig {interface} up", shell=True)


def reset_mac(interface):
	print("Resetting MAC Address")
	change_mac(interface, "00:0c:29:5f:cc:87")


(options, arguments) = get_arguments()
interface =options.interface
macaddress = options.macaddress

change_mac(interface, macaddress)
ifconfig_result = subprocess.check_output(["ifconfig", interface])

# ifconfig_result is currently represented as a string of bytes. We need to convert it into a normal string
ifconfig_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result.decode('utf-8'))
print(ifconfig_result.group(0))


# Use hardcoded harware address.
reset_mac(interface)
ifconfig_result = subprocess.check_output(["ifconfig", interface])

# ifconfig_result is currently represented as a string of bytes. We need to convert it into a normal string
ifconfig_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result.decode('utf-8'))
print(ifconfig_result.group(0))







