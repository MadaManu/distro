import thread
import time
import socket
import json
import helper




class PeerSearchSimplified:
	socket = None
	node_id = None
	routing_table = None
	
	# thread function to deal with all the messages that are received
	def receive_messages(self, socket):
		print socket.getsockname()
		while 1:
			data, addr = socket.recvfrom(1024)
			print "received message:", data
			message_data = json.loads(data)
			if message_data["type"] == helper.join_message:
				print 'Wanna join?'
			elif message_data["type"] == helper.join_relay_message:
				print 'the relay message'		
			elif message_data["type"] == helper.routing_info_message:
				print 'save the routing table'
			elif message_data["type"] == helper.leaving_message:
				print 'u telling me u want to leave? so fast?'
			elif message_data["type"] == helper.index_message:
				print 'let me index that for u'
			elif message_data["type"] == helper.search:
				print 'what do we search?'
			elif message_data["type"] == helper.search_response_type:
				print 'this is the response of my search?'
			elif message_data["type"] == helper.ping:
				print 'Do u really want to know if i\'m alive?'
			elif message_data["type"] == helper.ack:
				print 'ok... u acknowledged... i take count of that'
	
	def __init__ (self, udp_socket, node_id):
		# initialise with a udp socket
		socket = udp_socket;
		self.node_id = node_id;
		print socket.getsockname()
		try:
			thread.start_new_thread( self.receive_messages, (udp_socket,) )
		except Exception as error:
			print error

	def joinNetwork (self, (bootstrap_node_ip,bootstrap_node_port), identifier, target_identifier):
		print "JOINING! (bootstrap @ "+ bootstrap_node_ip + ':' + `bootstrap_node_port` + ')'
		message = helper.build_join_message(self.node_id, target_identifier, bootstrap_node_ip)
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
