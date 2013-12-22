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
	temporary_bootstraps = {}
	urls = {}
	
	# thread function to deal with all the messages that are received
	def receive_messages(self, socket):
		# print socket.getsockname()
		while 1:
			data, addr = socket.recvfrom(1024)
			# print "received message:", data
			message_data = json.loads(data)
			if message_data["type"] == helper.join_message:
				# print 'Wanna join?'
				# check if the node that wants to join is closer to any other node in the
				# routing table of the bootstrap node
				(min_key, min_difference) = helper.find_closest_node (self.routing_table, message_data["node_id"])
				add_here = False
				# print "CLOSEST NODE FROM ROUTING IS: ", min_key
				if min_key:
					# check if the closest node from the routing is not further away than the current node
					local_min = self.node_id - message_data["node_id"] if self.node_id > message_data["node_id"] else message_data["node_id"] - self.node_id 
					# print "THE LOCAL MINIMUM IS: ", local_min
					if local_min < min_difference:
						add_here = True
				else:					
					add_here = True
				if add_here:
					# if there is no other node closer, reply with the existing routing table
					# print "sending back the routing table"

					response_message = helper.build_routing_table_message(message_data["node_id"], self.node_id, self.socket.getsockname(), self.routing_table)
					# send back the routing info that is saved in bootstrap node to the joining node
					self.response_socket.sendto(response_message, (message_data["ip_address"], message_data["port"]))
					# print "routing table sent to joining node"
					# add the new node to the routing table
					self.routing_table[int(message_data["node_id"])] = (message_data["ip_address"], message_data["port"])
					# print "joining node added to routing table"

				else:																		# target,    gateway
					response_message = helper.build_join_relay_message(message_data["node_id"], min_key, self.node_id, message_data["ip_address"], message_data["port"])
					# save the temporary bootstrap
					self.temporary_bootstraps[message_data["node_id"]] = (message_data["ip_address"], message_data["port"])
					# print "THE MIN KEY IP / PORT", self.routing_table[min_key]
					# send the relay!
					self.response_socket.sendto(response_message, self.routing_table[int(min_key)])




			elif message_data["type"] == helper.join_relay_message:
				# print 'the relay message'
				# print message_data
				if message_data["target_id"] == self.node_id:
					# check for hop in own routing table
					# if node minimum distance then reply with message
					# otherwise save in own temporary_bootstraps where to root back
					(min_key, min_difference) = helper.find_closest_node (self.routing_table, message_data["node_id"])
					to_be_passed = False
					if min_key:
						local_min = self.node_id - message_data["node_id"] if self.node_id > message_data["node_id"] else message_data["node_id"] - self.node_id
						if min_difference < local_min:
							to_be_passed = True
						else:
							to_be_passed = False

					if to_be_passed:
						# TODo
						# add to temporary bootstraps and send to new gateway!
						# something wierd is happening in some cases here and at routing back the table with these temporary bootstraping values and routing tables
						response_message = helper.build_join_relay_message(message_data["node_id"], min_key, self.node_id, message_data["ip_address"], message_data["port"])
						self.temporary_bootstraps[message_data["node_id"]] = message_data["gateway_id"]
						self.response_socket.sendto(response_message, tuple(self.routing_table[int(min_key)]))

					else:
						response_message = helper.build_routing_table_message(message_data["node_id"], self.node_id, self.socket.getsockname(), self.routing_table)
						self.response_socket.sendto(response_message, self.routing_table[int(message_data["gateway_id"])])
						# print "routing table passed back to gateway (" + `message_data["gateway_id"]` + ")"
						self.routing_table[int(message_data["node_id"])] = (message_data["ip_address"], message_data["port"])

					

				
			elif message_data["type"] == helper.routing_info_message:
				# use the data only if the given node is the recipient
				if self.node_id == message_data["node_id"]:
					# save the routing table that we got from bootstraping
					self.routing_table = helper.append_to_routing_table(self.routing_table, message_data["route_table"])
					# self.routing_table = message_data["route_table"]
					self.routing_table[int(message_data["gateway_id"])] = (message_data["ip_address"], message_data["port"])
					# add the bootstrap node to the routing table !!!! 
					# print 'save the routing table'
				else: # if not recipient send routing table to next hop or receiver
					response_message = helper.build_routing_table_message (message_data["node_id"], message_data["gateway_id"], (message_data["ip_address"], message_data["port"]), message_data["route_table"])
					print self.temporary_bootstraps
					if type(self.temporary_bootstraps[message_data["node_id"]]) == tuple:
						# send routing table straight to saved data
						self.response_socket.sendto(response_message, self.temporary_bootstraps[message_data["node_id"]])
					else:
						# get the ip and port of the node to pass back on
						self.response_socket.sendto(response_message, self.routing_table[int(self.temporary_bootstraps[message_data["node_id"]])])
					# remove it from temporary bootstraps
					self.temporary_bootstraps.pop(message_data["node_id"])
					# print "pass the ROUTING TABLE ONWARDS!>!>!>!>!>!>"



			elif message_data["type"] == helper.leaving_message:
				# just remove the node_id from your routing table
				if int(message_data["node_id"]) in self.routing_table:
					self.routing_table.pop(message_data["node_id"])


			elif message_data["type"] == helper.index_message:
				# print message_data["keyword"]
				for link in message_data["link"]:
					if link in self.urls:
						self.urls[link] = self.urls[link] + 1
					else:
						self.urls[link] = 1
				# print 'I TRY TO INDEX SHIT UP FOR U!!!!'
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
		self.socket = udp_socket
		self.node_id = helper.hashCode(node_id)
		self.routing_table = {}
		# print self.socket.getsockname()
		try:
			thread.start_new_thread( self.receive_messages, (udp_socket,) )
		except Exception as error:
			print error

# removed the need for identifier because the node that want's to join the network already has its own
# identifier saved as an attribute, therefore no need to pass it in.
	def joinNetwork (self, (bootstrap_node_ip,bootstrap_node_port), target_identifier):
		target_identifier = helper.hashCode(target_identifier)
		# print "JOINING! (bootstrap @ "+ bootstrap_node_ip + ':' + `bootstrap_node_port` + ')'
		message = helper.build_join_message(self.node_id, target_identifier, self.socket.getsockname())
		self.response_socket.sendto(message, (bootstrap_node_ip, bootstrap_node_port))

	def leaveNetwork (self):
		response_message = helper.build_leaving_message(self.node_id)
		print self.routing_table
		for node in self.routing_table:
			print self.routing_table[node]
			self.response_socket.sendto(response_message, tuple(self.routing_table[node]))
		
	# changed from list of unique_words to one word to index multiple urls
	def indexPage (self, word, list_of_urls):
		node_id_to_send_to = int(helper.hashCode(word))
		response_message = helper.build_index_message (node_id_to_send_to, self.node_id, word, list_of_urls)
		# find the ip and port to send to the index message
		if node_id_to_send_to in self.routing_table:
			ip_port_addr = self.routing_table[node_id_to_send_to]
		else:
			# find closest one to send to from the routing table
			(min_key, min_difference) = helper.find_closest_node(self.routing_table, node_id_to_send_to)
			ip_port_addr = self.routing_table[min_key]

		self.response_socket.sendto(response_message, ip_port_addr)


	def search (self, words):
		print ('HEllo')

	def print_routing(self):
		for key in self.routing_table:
			print `key` + ">>" + str(self.routing_table[key])

	def print_data(self):
		print '\n'
		for key in self.urls:
			print `key` + "-->" + str(self.urls[key])