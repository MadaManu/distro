import socket
import json
import sys
from searchclass import SearchResult

UDP_IP = None
UDP_PORT = 8767 # default port




port_arg = '--port'
port_val = None
boot_arg = '--boot'
boot_val = None
bootstrap_arg = '--bootstrap'
bootstrap_val = None
id_arg = '--id'
id_val = None

if boot_arg in sys.argv:
	try:
		boot_val = sys.argv[sys.argv.index(boot_arg)+1] 
	except IndexError:
		sys.exit('No value for the id argument. (--id value) Error!')
else:
	if bootstrap_arg in sys.argv and id_arg in sys.argv:
		try:
			bootstrap_val = sys.argv[sys.argv.index(bootstrap_arg)+1]
			try:
				socket.inet_aton(bootstrap_val)
			except socket.error:
				sys.exit('Not a valid IP as bootstrap argument. Error!')
		except IndexError:
			sys.exit('No value for the bootstrap argument. (--bootstrap value) Error!')
		try:
			id_val = sys.argv[sys.argv.index(id_arg)+1]
		except IndexError:
			sys.exit('No value for the id argument. (--id value) Error!')
	else:
		if bootstrap_arg not in sys.argv and id_arg not in sys.argv:
			sys.exit("No arguments specified (--boot or --bootstrap and --id). Error!")
		if bootstrap_arg not in sys.argv:
			sys.exit("No bootstrap argument (--bootstrap) given. Error!")
		if id_arg not in sys.argv:
			sys.exit("No id argument (--id) given. Error!")

if port_arg in sys.argv:
	port_val = sys.argv[sys.argv.index(port_arg)+1]

if port_val:
	if int(port_val) > 65535 or int(port_val) < 0:
		sys.exit("Port must be 0 - 65535. Error!")
	else:
		UDP_PORT = int(port_val)

# define the socket to deal with all the connections
first_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP connections

# assign the specific IP 		
if boot_val:
	UDP_IP = "127.0.0.1" # localhost
else:
	if bootstrap_val:
		UDP_IP = bootstrap_val # connect to the given IP addr

first_socket.bind((UDP_IP, UDP_PORT))
first_object = SearchResult(first_socket)

# add one more node

second_port = UDP_PORT + 1;
second_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
second_socket.bind((UDP_IP, second_port))
second_object = SearchResult(second_socket)

second_object.joinNetwork((UDP_IP, UDP_PORT),'', '')

while 1:
	pass

# public int hashCode(String str) {
#   int hash = 0;
#   for (int i = 0; i < str.length(); i++) {
#     hash = hash * 31 + str.charAt(i);
#   }
#   return Math.abs(hash);
# }