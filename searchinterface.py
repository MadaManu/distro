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
		while 1:
			# constantly receive data
			data, addr = socket.recvfrom(1024)
			# unload the data from json
			message_data = json.loads(data)


# JOIN MESSAGE RECEIVED
			if message_data["type"] == helper.join_message:
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
					response_message = helper.build_routing_table_message(message_data["node_id"], self.node_id, self.socket.getsockname(), self.routing_table)
					# send back the routing info that is saved in bootstrap node to the joining node
					self.response_socket.sendto(response_message, (message_data["ip_address"], message_data["port"]))
					# add the new node to the routing table
					self.routing_table[int(message_data["node_id"])] = (message_data["ip_address"], message_data["port"])
				else:																		# target,    gateway
					response_message = helper.build_join_relay_message(message_data["node_id"], min_key, self.node_id, message_data["ip_address"], message_data["port"])
					# save the temporary bootstrap
					self.temporary_bootstraps[message_data["node_id"]] = (message_data["ip_address"], message_data["port"])
					# send the relay!
					self.response_socket.sendto(response_message, self.routing_table[int(min_key)])




# JOIN RELAY MESSAGE
			elif message_data["type"] == helper.join_relay_message:
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
						# add to temporary bootstraps and send to new gateway!
						# temporary bootstraps to be able to rute back the routing table response to the joining node
						response_message = helper.build_join_relay_message(message_data["node_id"], min_key, self.node_id, message_data["ip_address"], message_data["port"])
						self.temporary_bootstraps[message_data["node_id"]] = message_data["gateway_id"]
						self.response_socket.sendto(response_message, tuple(self.routing_table[int(min_key)]))
					else:
						# if there is no need to pass it down through the routing table (meaning the current node is minimum)
						# build the routing table message and send it back routing hop by hop
						response_message = helper.build_routing_table_message(message_data["node_id"], self.node_id, self.socket.getsockname(), self.routing_table)
						self.response_socket.sendto(response_message, self.routing_table[int(message_data["gateway_id"])])
						self.routing_table[int(message_data["node_id"])] = (message_data["ip_address"], message_data["port"])




# ROUTING INFO MESSAGE RECEIVED
			elif message_data["type"] == helper.routing_info_message:
				# use the data only if the given node is the recipient
				if self.node_id == message_data["node_id"]:
					# append the routing table that we got from bootstraping
					self.routing_table = helper.append_to_routing_table(self.routing_table, message_data["route_table"])
					self.routing_table[int(message_data["gateway_id"])] = (message_data["ip_address"], message_data["port"])
				else: # if not recipient send routing table to next hop or receiver
					response_message = helper.build_routing_table_message (message_data["node_id"], message_data["gateway_id"], (message_data["ip_address"], message_data["port"]), message_data["route_table"])
					# check if saved a (ip,port) tuple or another node_id
					if type(self.temporary_bootstraps[message_data["node_id"]]) == tuple:
						# send routing table straight to saved data
						self.response_socket.sendto(response_message, self.temporary_bootstraps[message_data["node_id"]])
					else:
						# guaranteed that if there is another node_id it will have a match in the
						# routing table of the current node
						self.response_socket.sendto(response_message, self.routing_table[int(self.temporary_bootstraps[message_data["node_id"]])])
					# remove it from temporary bootstraps - because route is taken back (consumed by the above send to)
					self.temporary_bootstraps.pop(message_data["node_id"])




# LEAVING MESSAGE RECEIVED
			elif message_data["type"] == helper.leaving_message:
				# just remove the node_id from your routing table
				if int(message_data["node_id"]) in self.routing_table:
					self.routing_table.pop(message_data["node_id"])




# INDEX MESSAGE RECEIVED
			elif message_data["type"] == helper.index_message:
				if int(message_data["target_id"]) == int(self.node_id): 
					# the current node is the target node
					# save all links in node
					for link in message_data["link"]:
						if link in self.urls: # if exists already increase the count, otherwise add it as seen once
							self.urls[link] = self.urls[link] + 1
						else:
							self.urls[link] = 1
					# send ACK - based on exact match in routing or closer node to target
					response_message = helper.build_ack_index_message(message_data["sender_id"], message_data["keyword"])
					if message_data["sender_id"] in self.routing_table:
						ip_port_addr = tuple(self.routing_table[message_data["sender_id"]])
					else:
						(min_key, min_difference) = helper.find_closest_node(self.routing_table, message_data["sender_id"])
						ip_port_addr = tuple(self.routing_table[min_key])
					self.response_socket.sendto(response_message, ip_port_addr)
				else:
					# pass on the index message
					response_message = helper.build_index_message (message_data["target_id"], message_data["sender_id"], message_data["keyword"], message_data["link"])
					# find target exact match or closest
					if message_data["target_id"] in self.routing_table:
						ip_port_addr = tuple(self.routing_table[int(message_data["target_id"])])
					else:
						(min_key, min_difference) = helper.find_closest_node(self.routing_table, message_data["target_id"])
						ip_port_addr = tuple(self.routing_table[min_key])
					self.socket.sendto(response_message, ip_port_addr)




# SEARCH MESSAGE RECEIVED
			elif message_data["type"] == helper.search:
				if message_data["node_id"] == self.node_id:
					# build the search response
					response_message = helper.build_search_response_message(message_data["word"], message_data["sender_id"], self.node_id, self.urls)
					#find the ip and port of closest to sender or the sender itself
					if message_data["sender_id"] in self.routing_table:
						ip_port_addr = tuple(self.routing_table[int(message_data["sender_id"])])
					else:
						(min_key, min_difference) = helper.find_closest_node(self.routing_table, message_data["sender_id"])
						ip_port_addr = tuple(self.routing_table[min_key])

					self.socket.sendto(response_message, ip_port_addr)
				else:
					response_message = helper.build_search_message(message_data["node_id"], message_data["node_id"], message_data["sender_id"])
					if message_data["node_id"] in self.routing_table: # check if final hop not in current routing table
						ip_port_addr = tuple(self.routing_table[message_data["node_id"]])
					else: # find closest one to send to from the routing table and pass the search message
						(min_key, min_difference) = helper.find_closest_node(self.routing_table, message_data["node_id"])
						ip_port_addr = tuple(self.routing_table[min_key])
					self.socket.sendto(response_message, ip_port_addr)




# SEARCH RESPONSE MESSAGE RECEIVED
			elif message_data["type"] == helper.search_response_type:
				if message_data["node_id"] == self.node_id: # if final target of the search response
					print "Search response for '" + message_data["word"] + "': \n"
					helper.prettyPrint(message_data["response"]) # print results
				else: # otherwise pass the response closer to target (or to target itself)
					response_message = helper.build_search_response_message(message_data["word"], message_data["node_id"], message_data["sender_id"], message_data["response"])
					# route the response to target
					if message_data["node_id"] in self.routing_table:
						ip_port_addr = tuple(self.routing_table[int(message_data["node_id"])])
					else:
						(min_key, min_difference) = helper.find_closest_node(self.routing_table, message_data["node_id"])
						ip_port_addr = tuple(self.routing_table[min_key])
					self.response_socket.sendto(response_message, ip_port_addr)
				print '\n'




# PING MESSAGE RECEIVED
			elif message_data["type"] == helper.ping:
				# Ping not necessary as in the simplified version there's an 
				# assumption that the nodes requested will always be there
				print 'Am I alive?'




# ACK MESSAGE RECEIVED
			elif message_data["type"] == helper.ack:
				# Not used because the ping messaging is not used
				print 'ack received'




# ACK INDEX MESSAGE RECEIVED
			elif message_data["type"] == helper.ack_index_message:
				if message_data["node_id"] == self.node_id:
					print "ACK for indexing keyword (" + message_data["keyword"] + ") received."
				else:
					response_message = helper.build_ack_index_message(message_data["node_id"], message_data["keyword"])
					if message_data["node_id"] in self.routing_table:
						ip_port_addr = tuple(self.routing_table[message_data["node_id"]])
					else:
						(min_key, min_difference) = helper.find_closest_node(self.routing_table, message_data["node_id"])
						ip_port_addr = tuple(self.routing_table[min_key])
					self.response_socket.sendto(response_message, ip_port_addr)
# end of function dealing with all possible received messages

	# constructor	
	def __init__ (self, udp_socket, node_id):
		# initialise with a udp socket and the hash code of the node id (word)
		# rest of the specific values for each node to be empty
		self.socket = udp_socket
		self.node_id = helper.hashCode(node_id)
		self.routing_table = {}
		self.urls = {}
		try:
			thread.start_new_thread( self.receive_messages, (udp_socket,) )
		except Exception as error:
			print error

	# join network function to allow a specific node join a network (given it has a bootstrap node known and can be passed in)
	# removed the need for identifier because the node that want's to join the network already has its own
	# identifier saved as an attribute, therefore no need to pass it in.
	def joinNetwork (self, (bootstrap_node_ip,bootstrap_node_port), target_identifier):
		target_identifier = helper.hashCode(target_identifier) # hash the target identifier so it can be passed in as word
		message = helper.build_join_message(self.node_id, target_identifier, self.socket.getsockname())
		self.response_socket.sendto(message, (bootstrap_node_ip, bootstrap_node_port))

	# the function to leave the network
	def leaveNetwork (self):
		response_message = helper.build_leaving_message(self.node_id)
		for node in self.routing_table:
			self.response_socket.sendto(response_message, tuple(self.routing_table[node]))
		
	# index function - to initiate the index of a word to a list of urls
	# changed from list of unique_words to one word to index multiple urls
	def indexPage (self, word, list_of_urls):
		node_id_to_send_to = int(helper.hashCode(word))
		if node_id_to_send_to == self.node_id: # if the request of indexing a word is done at the node 
											# that indexes exactly that word, then save/add the new index
			for url in list_of_urls:
				if url in self.urls:
					self.urls[url] = self.urls[url] + 1
				else:
					self.urls[url] = 1
		else:
			# if the current node doesn't match the indexed word, pass on the message
			response_message = helper.build_index_message (node_id_to_send_to, self.node_id, word, list_of_urls)
			# find the ip and port to send to the index message
			if node_id_to_send_to in self.routing_table:
				# check local routing for match
				ip_port_addr = tuple(self.routing_table[node_id_to_send_to])
			else:
				# find closest one to send to from the routing table
				(min_key, min_difference) = helper.find_closest_node(self.routing_table, node_id_to_send_to)
				ip_port_addr = tuple(self.routing_table[min_key])
			self.response_socket.sendto(response_message, ip_port_addr)


	# search function to allow any node to search for urls of a given word
	def search (self, word):
		node_id_to_send_to = int(helper.hashCode(word))
		if node_id_to_send_to == self.node_id: # if looking for the word that is indexed by current node,
											# just display the results
			print "Search response for '" + word +"': \n"
			print self.urls
		else: # otherwise request it from network
			response_message = helper.build_search_message(word, node_id_to_send_to, self.node_id)
			# find the ip and port to send to the index message
			if node_id_to_send_to in self.routing_table:
				# check local routing for match
				ip_port_addr = tuple(self.routing_table[node_id_to_send_to])
			else:
				# find closest one to send to from the routing table
				(min_key, min_difference) = helper.find_closest_node(self.routing_table, node_id_to_send_to)
				ip_port_addr = tuple(self.routing_table[min_key])
			self.response_socket.sendto(response_message, ip_port_addr)

# usefull printing functions
	# print the routing table of a node
	def print_routing(self):
		helper.prettyPrint(self.routing_table)

	# print the indexing table of a node
	def print_data(self):
		helper.prettyPrint(self.urls)