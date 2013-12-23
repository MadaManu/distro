import socket
import json
import sys
from searchinterface import PeerSearchSimplified
import helper

UDP_IP = "127.0.0.1" # localhost
UDP_PORT = 8767 # default port

# get arguments for the starting PORT
if len(sys.argv)>1:
	if "--port" in sys.argv:
		port_val = None
		try: # make sure the --port specifies a value after too
			port_val = int(sys.argv[sys.argv.index("--port")+1])
		except IndexError:
			sys.exit('No value for the port argument (--port value). Error')
		if port_val> 65530 or port_val < 0:
			sys.exit("Port must be 0 - 65530. Error") # make sure the port value is somehow sensible
		else:
			UDP_PORT = port_val
			print "First port set to be: " + `UDP_PORT` + '\n'
	else:
		sys.exit("Command line argument not accepted! (only --port). Error")
else:
	print "Port not specified using as default: " + `UDP_PORT` + '\n'



# define the socket to deal with the connections of the first node (first_object)
first_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP connections
# bind first socket to selected IP and PORT (because port could be changed from arguments)
first_socket.bind((UDP_IP, UDP_PORT))
# create first object (first node) - assigning the word distributed to it
first_object = PeerSearchSimplified(first_socket, "distributed")


# add one more node to first port+1 and same IP
second_port = UDP_PORT + 1
second_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
second_socket.bind((UDP_IP, second_port))		# assigning the word systems to second node
second_object = PeerSearchSimplified(second_socket, "systems")
# picked the node called distributed as the bootstrap node - joinNetwork requires the tuple (IP,PORT)
# of the bootstrap node (in this case distributed)
second_object.joinNetwork((UDP_IP, UDP_PORT), "distributed")

third_port = UDP_PORT + 2
third_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
third_socket.bind((UDP_IP, third_port))
third_object = PeerSearchSimplified(third_socket, "testing")
								# third node joining the network through the 'distributed' node too
third_object.joinNetwork((UDP_IP, UDP_PORT), "distributed") 


fourth_port = UDP_PORT + 3
fourth_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
fourth_socket.bind((UDP_IP, fourth_port))
fourth_object = PeerSearchSimplified(fourth_socket, "tcd")
fourth_object.joinNetwork((UDP_IP, UDP_PORT), "distributed")

print "Network consisting of 4 nodes has been built.\n"

raw_input("Press Enter to index some pages...\n")
first_object.indexPage("systems", ["google.ie","wikipedia.org","blog.me","sys.com"])
second_object.indexPage("distributed", ["wikipedia.org","dsg.ie", "google.com"])
fourth_object.indexPage("systems", ["dsg.ie","google.com", "sys.com"])
third_object.indexPage("tcd", ["google.com"])

print "\n Acknowledgements from indexing pages to different keywords \n"

raw_input("Press Enter to search on the `tcd` node for keyword `distributed`...\n")
fourth_object.search("distributed")


raw_input("Press Enter to display routing table and data stored...\n")

print "`distributed` (" + `helper.hashCode("distributed")` + ")\n"
print "Routing Table\n"
first_object.print_routing()
print "-------------------"
print "Links Indexed and count"
first_object.print_data()
print "===================\n"

print "`systems` (" + `helper.hashCode("systems")` + ")\n"
print "Routing Table\n"
second_object.print_routing()
print "-------------------"
print "Links Indexed and count"
second_object.print_data()
print "===================\n"

print "`testing` (" + `helper.hashCode("testing")` + ")\n"
print "Routing Table\n"
third_object.print_routing()
print "-------------------"
print "Links Indexed and count"
third_object.print_data()
print "===================\n"


print "`tcd` (" + `helper.hashCode("tcd")` + ")\n"
print "Routing Table\n"
fourth_object.print_routing()
print "-------------------"
print "Links Indexed and count"
fourth_object.print_data()
print "===================\n"
