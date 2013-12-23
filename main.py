import socket
import json
import sys
from searchinterface import PeerSearchSimplified
import helper

UDP_IP = "127.0.0.1" # localhost
UDP_PORT = 8767 # default port





# define the socket to deal with all the connections
first_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP connections

# assign the specific IP 		
# if boot_val:

# else:
	# if bootstrap_val:
		# UDP_IP = bootstrap_val # connect to the given IP addr



# bind first socket to selected IP and PORT (because port could be changed from arguments)
first_socket.bind((UDP_IP, UDP_PORT))
# create first object
first_object = PeerSearchSimplified(first_socket, "distributed")

# add one more node to first port+1 and same IP
second_port = UDP_PORT + 1
second_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
second_socket.bind((UDP_IP, second_port))
# create second object
second_object = PeerSearchSimplified(second_socket, "systems")


# ask second object to join the network!!!
# why need identifier, target_identifier in join network - if bootstrap is known and the peer
# to be added is just calling the method

# picked the node called distributed as the bootstrap node
second_object.joinNetwork((UDP_IP, UDP_PORT), "distributed")


third_port = UDP_PORT + 2
third_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
third_socket.bind((UDP_IP, third_port))
third_object = PeerSearchSimplified(third_socket, "testing")
third_object.joinNetwork((UDP_IP, UDP_PORT), "distributed")


fourth_port = UDP_PORT + 3
fourth_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
fourth_socket.bind((UDP_IP, fourth_port))
fourth_object = PeerSearchSimplified(fourth_socket, "tcd")
fourth_object.joinNetwork((UDP_IP, UDP_PORT), "distributed")

# make a node leave
# third_object.leaveNetwork() 





raw_input("Press Enter to index some pages...")
first_object.indexPage("systems", ["url1","url2","url3","url4"])
second_object.indexPage("systems", ["url2","NEW URL", "url3"])
fourth_object.indexPage("systems", ["url2","NEW URL", "url3"])

raw_input("Press Enter to search...")
first_object.search("distributed")


raw_input("Press Enter to display routing table and data stored...")
print "\n42 ROUTING INFO!!!!"
first_object.print_routing()
print "-------------------\n"

print "10 ROUTING INFO!!!!"
second_object.print_routing()
second_object.print_data()
print "-------------------\n"

print "7 ROUTING INFO!!!!"
third_object.print_routing()
print "-------------------\n"


print "8 ROUTING INFO!!!!"
fourth_object.print_routing()
print "-------------------\n"
