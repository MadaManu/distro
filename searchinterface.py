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
			data, addr = socket.recvfrom(1024)
			message_data = json.loads(data)
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
						# TODo
						# add to temporary bootstraps and send to new gateway!
						# something wierd is happening in some cases here and at routing back the table with these temporary bootstraping values and routing tables
						response_message = helper.build_join_relay_message(message_data["node_id"], min_key, self.node_id, message_data["ip_address"], message_data["port"])
						self.temporary_bootstraps[message_data["node_id"]] = message_data["gateway_id"]
						self.response_socket.sendto(response_message, tuple(self.routing_table[int(min_key)]))

					else:
						response_message = helper.build_routing_table_message(message_data["node_id"], self.node_id, self.socket.getsockname(), self.routing_table)
						self.response_socket.sendto(response_message, self.routing_table[int(message_data["gateway_id"])])
						self.routing_table[int(message_data["node_id"])] = (message_data["ip_address"], message_data["port"])


					

				
			elif message_data["type"] == helper.routing_info_message:
				# use the data only if the given node is the recipient
				if self.node_id == message_data["node_id"]:
					# save the routing table that we got from bootstraping
					self.routing_table = helper.append_to_routing_table(self.routing_table, message_data["route_table"])
					# self.routing_table = message_data["route_table"]
					self.routing_table[int(message_data["gateway_id"])] = (message_data["ip_address"], message_data["port"])
					# add the bootstrap node to the routing table !!!! 
				else: # if not recipient send routing table to next hop or receiver
					response_message = helper.build_routing_table_message (message_data["node_id"], message_data["gateway_id"], (message_data["ip_address"], message_data["port"]), message_data["route_table"])
					if type(self.temporary_bootstraps[message_data["node_id"]]) == tuple:
						# send routing table straight to saved data
						self.response_socket.sendto(response_message, self.temporary_bootstraps[message_data["node_id"]])
					else:
						# get the ip and port of the node to pass back on
						self.response_socket.sendto(response_message, self.routing_table[int(self.temporary_bootstraps[message_data["node_id"]])])
					# remove it from temporary bootstraps
					self.temporary_bootstraps.pop(message_data["node_id"])




			elif message_data["type"] == helper.leaving_message:
				# just remove the node_id from your routing table
				if int(message_data["node_id"]) in self.routing_table:
					self.routing_table.pop(message_data["node_id"])




			elif message_data["type"] == helper.index_message:
				for link in message_data["link"]:
					if link in self.urls:
						self.urls[link] = self.urls[link] + 1
					else:
						self.urls[link] = 1



			elif message_data["type"] == helper.search:
				if message_data["node_id"] == self.node_id:
					# build the search response
					response_message = helper.build_search_response_message(message_data["word"], message_data["sender_id"], self.node_id, self.urls)
					#find the ip and port of closest to sender or the sender itself
					if message_data["sender_id"] in self.routing_table:
						ip_port_addr = tuple(self.routing_table[int(message_data["sender_id"])])
					else:
						(min_key, min_difference) = helper.find_closest_node(self.routing_table, message_data["sender_id"])
						ip_port_addr = self.routing_table[min_key]
					self.socket.sendto(response_message, ip_port_addr)
				else:
					# find closest one to send to from the routing table
					response_message = helper.build_search_message(message_data["node_id"], message_data["node_id"], message_data["sender_id"])
					(min_key, min_difference) = helper.find_closest_node(self.routing_table, message_data["node_id"])
					ip_port_addr = self.routing_table[min_key]
					self.socket.sendto(response_message, ip_port_addr)

			elif message_data["type"] == helper.search_response_type:
				print 'this is the response of my search?'
			elif message_data["type"] == helper.ping:
				print 'Do u really want to know if i\'m alive?'
			elif message_data["type"] == helper.ack:
				print 'ok... u acknowledged... i take count of that'
			elif message_data["type"] == helper.ack_index_message:
				print "y acknowledged the indexing"
	
	def __init__ (self, udp_socket, node_id):
		# initialise with a udp socket
		self.socket = udp_socket
		self.node_id = helper.hashCode(node_id)
		self.routing_table = {}

		try:
			thread.start_new_thread( self.receive_messages, (udp_socket,) )
		except Exception as error:
			print error

# removed the need for identifier because the node that want's to join the network already has its own
# identifier saved as an attribute, therefore no need to pass it in.
	def joinNetwork (self, (bootstrap_node_ip,bootstrap_node_port), target_identifier):
		target_identifier = helper.hashCode(target_identifier)
		
		message = helper.build_join_message(self.node_id, target_identifier, self.socket.getsockname())
		self.response_socket.sendto(message, (bootstrap_node_ip, bootstrap_node_port))

	def leaveNetwork (self):
		response_message = helper.build_leaving_message(self.node_id)
		
		for node in self.routing_table:
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


	def search (self, word):
		node_id_to_send_to = int(helper.hashCode(word))
		response_message = helper.build_search_message(word, node_id_to_send_to, self.node_id)
		if node_id_to_send_to in self.routing_table:
			ip_port_addr = self.routing_table[node_id_to_send_to]
		else:
			# find closest one to send to from the routing table
			(min_key, min_difference) = helper.find_closest_node(self.routing_table, node_id_to_send_to)
			ip_port_addr = self.routing_table[min_key]

		self.response_socket.sendto(response_message, ip_port_addr)

	def print_routing(self):
		for key in self.routing_table:
			print `key` + ">>" + str(self.routing_table[key])

	def print_data(self):
		print '\n'
		for key in self.urls:
			print `key` + "-->" + str(self.urls[key])