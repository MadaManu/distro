import socket
import json
import sys
from searchclass import SearchResult

UDP_IP = None
UDP_PORT = 8767





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

# define the socket to deal with all the connections
socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP connections

# assign the specific IP 		
if boot_val:
	UDP_IP = "127.0.0.1" # localhost
else:
	if bootstrap_val:
		UDP_IP = bootstrap_val # connect to the given IP addr

socket.bind((UDP_IP, UDP_PORT))
first_object = SearchResult(socket)





# public int hashCode(String str) {
#   int hash = 0;
#   for (int i = 0; i < str.length(); i++) {
#     hash = hash * 31 + str.charAt(i);
#   }
#   return hash;
# }




# import thread
# import time

# # Define a function for the thread
# def print_time( threadName, delay):
#    count = 0
#    while count < 5:
#       time.sleep(delay)
#       count += 1
#       print "%s: %s" % ( threadName, time.ctime(time.time()) )

# # Create two threads as follows
# try:
#    thread.start_new_thread( print_time, ("Thread-1", 2, ) )
#    thread.start_new_thread( print_time, ("Thread-2", 4, ) )
# except:
#    print "Error: unable to start thread"

# while 1:
#    pass