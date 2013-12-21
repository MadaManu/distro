import thread
import time
import socket
import json
import helper




class PeerSearchSimplified:
	node_id = None
	routing_table = {}
	response_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	socket = None
	
	# thread function to deal with all the messages that are received
	def receive_messages(self, socket):
		print socket.getsockname()
		while 1:
			data, addr = socket.recvfrom(1024)
			print "received message:", data
			message_data = json.loads(data)
			if message_data["type"] == helper.join_message:
				print 'Wanna join?'
				# check if the node that wants to join is closer to any other node in the
				# routing table of the bootstrap node
				(min_key, min_difference) = helper.find_closest_node (self.routing_table, message_data["node_id"])
				add_here = False
				if min_key:
					# check if the closest node from the routing is not further away than the current node
					local_min = self.node_id - message_data["node_id"] if self.node_id > message_data["node_id"] else message_data["node_id"] - self.node_id 
					if local_min < min_difference:
						add_here = True
				else:					
					add_here = True
				if add_here:
					# if there is no other node closer, reply with the existing routing table
					print "sending back the routing table"
					response_message = helper.build_routing_table_message(message_data["node_id"], self.node_id, self.socket.getsockname(), self.routing_table)
					# send back the routing info that is saved in bootstrap node to the joining node
					self.response_socket.sendto(response_message, (message_data["ip_address"], message_data["port"]))
					print "routing table sent to joining node"
					# add the new node to the routing table
					self.routing_table[message_data["node_id"]] = (message_data["ip_address"], message_data["port"])
					print "joining node added to routing table"

				else:
					print "THIS IS THE MINIMUM KEEEY!"
					print min_key
					response_message = helper.build_join_relay_message(message_data["node_id"], min_key, self.node_id)
					# print response_message
					print "THE MIN KEY IP / PORT"
					print self.routing_table[min_key][1]

					self.response_socket.sendto(response_message, self.routing_table[min_key])
					print "PASS ON THE JOIN REQUEST! USING RELAY!!!!!!!!!<<!<<!<!<!<!<<!<!<!"

			elif message_data["type"] == helper.join_relay_message:
				response_message = helper.build_routing_table_message(message_data["node_id"], message_data["gateway_id"], self.socket.getsockname(), self.routing_table)

				print 'the relay message'		
			elif message_data["type"] == helper.routing_info_message:
				# save the routing table that we got from bootstraping
				self.routing_table = message_data["route_table"]
				self.routing_table[message_data["gateway_id"]] = (message_data["ip_address"], message_data["port"])
				# add the bootstrap node to the routing table !!!! todo
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
		self.socket = udp_socket;
		self.node_id = node_id;
		print self.socket.getsockname()
		try:
			thread.start_new_thread( self.receive_messages, (udp_socket,) )
		except Exception as error:
			print error

# removed the need for identifier because the node that want's to join the network already has its own
# identifier saved as an attribute, therefore no need to pass it in.
	def joinNetwork (self, (bootstrap_node_ip,bootstrap_node_port), target_identifier):
		print "JOINING! (bootstrap @ "+ bootstrap_node_ip + ':' + `bootstrap_node_port` + ')'
		message = helper.build_join_message(self.node_id, target_identifier, self.socket.getsockname())
		self.response_socket.sendto(message, (bootstrap_node_ip, bootstrap_node_port))

		# returns network_id, a locally
		# generated number to identify peer network

	def leaveNetwork (self, network_id):
		# parameter is previously returned peer network identifier
		print ('HEllo')

	def indexPage (self, url, unique_words):
		print (url+' '+str(unique_words))

	def search (self, words):
		print ('HEllo')

	def print_routing(self):
		for key in self.routing_table:
			print `key` + ">>" + str(self.routing_table[key])