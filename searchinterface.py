import thread
import time
import socket
import json
import helper

# thread function to deal with all the messages that are received
def receive_messages(socket):
	print socket.getsockname()
	while 1:
		data, addr = socket.recvfrom(1024)
		print "received message:", data
		message_data = json.loads(data)
		if message_data["type"] == helper.join_message:
			print 'Wanna join?'

class PeerSearchSimplified:
	socket = None
	

	def __init__ (self, udp_socket):
		# initialise with a udp socket
		socket = udp_socket;
		print socket.getsockname()
		try:
			thread.start_new_thread( receive_messages, (udp_socket,) )
		except Exception as error:
			print error
	def joinNetwork (self, (bootstrap_node_ip,bootstrap_node_port), identifier, target_identifier):
		print "JOINING! (bootstrap @ "+ bootstrap_node_ip + ':' + `bootstrap_node_port` + ')'
		message = helper.build_join_message(42, 33, bootstrap_node_ip)
		message_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		message_socket.sendto(message, (bootstrap_node_ip, bootstrap_node_port))
		# returns network_id, a locally
		# generated number to identify peer network

	def leaveNetwork (self, network_id):
		# parameter is previously returned peer network identifier
		print ('HEllo')

	def indexPage (self, url, unique_words):
		print (url+' '+str(unique_words))

	def search (self, words):
		print ('HEllo')



	