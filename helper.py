import json
import math
import sys
import pprint


# Helper file containing constant values, and usefull functions

# CONSTANT VALUES
join_message = "JOINING_NETWORK_SIMPLIFIED"
join_relay_message = "JOINING_NETWORK_RELAY_SIMPLIFIED"
routing_info_message = "ROUTING_INFO"
leaving_message = "LEAVING_NETWORK"
index_message = "INDEX"
search = "SEARCH"
search_response_type = "SEARCH_RESPONSE"
ping = "PING"
ack = "ACK"
ack_index_message = "ACK_INDEX"


# FUNCTIONS

# prettyPrint function
def prettyPrint(data):
	pp = pprint.PrettyPrinter(width=60)
	pp.pprint(data)

# hash function
def hashCode (str_value):
	hash = 0
	for c in str_value:
		hash = hash * 31 + ord(c)
	return abs(hash)

# function to append dict to another dict by keeping tuples 
# in place and keys as int desired for type unification
def append_to_routing_table(existing_table, to_append):
	if to_append:
		for key in to_append:
			existing_table[int(key)] = tuple(to_append[key]) # enforce tuple values and int as key
	return existing_table

# find the closest node to the specified node from the supplied routing table
def find_closest_node (routing_table, node_id):
	min_difference = sys.maxsize
	min_key = None
	node_id = int(node_id)
	if routing_table:
		for node in routing_table:
			int_node = int(node)
			local_min = int_node - node_id if int_node > node_id else node_id - int_node
			if local_min < min_difference:
				min_key = int_node
				min_difference = local_min
	return (min_key, min_difference) # return a tuple containing the smallest distance found 
									# and the key at which the distance is smallest

def build_join_message (node_id, target_id, (ip_address, port)):
	message_structure = {}
	message_structure["type"] = join_message
	message_structure["node_id"] = node_id
	message_structure["target_id"] = target_id
	message_structure["ip_address"] = ip_address
	message_structure["port"] = port
	return json.dumps(message_structure, sort_keys=True, indent=4, separators=(',', ': '))

def build_join_relay_message (node_id, target_id, gateway_id, ip_address, port):
	message_structure = {}
	message_structure["type"] = join_relay_message
	message_structure["node_id"] = node_id
	message_structure["target_id"] = target_id
	message_structure["gateway_id"] = gateway_id
	message_structure["ip_address"] = ip_address
	message_structure["port"] = port
	return json.dumps(message_structure, sort_keys=True, indent=4, separators=(',', ': '))

def build_routing_table_message (node_id, gateway_id, (ip_address, port), route_table):
	message_structure = {}
	message_structure["type"] = routing_info_message
	message_structure["node_id"] = node_id
	message_structure["ip_address"] = ip_address
	message_structure["port"] = port
	message_structure["gateway_id"] = gateway_id
	message_structure["route_table"] = route_table
	return json.dumps(message_structure, sort_keys=True, indent=4, separators=(',', ': '))

def build_leaving_message (node_id):
	message_structure = {}
	message_structure["type"] = "LEAVING_NETWORK"
	message_structure["node_id"] = node_id
	return json.dumps(message_structure, sort_keys=True, indent=4, separators=(',', ': '))

def build_index_message (target_id, sender_id, keyword, link):
	message_structure = {}
	message_structure["type"] = index_message
	message_structure["target_id"] = target_id
	message_structure["sender_id"] = sender_id
	message_structure["keyword"] = keyword
	message_structure["link"] = link
	return json.dumps(message_structure, sort_keys=True, indent=4, separators=(',', ': '))

def build_search_message (word, node_id, sender_id):
	message_structure = {}
	message_structure["type"] = search
	message_structure["word"] = word
	message_structure["node_id"] = node_id
	message_structure["sender_id"] = sender_id
	return json.dumps(message_structure, sort_keys=True, indent=4, separators=(',', ': '))

def build_search_response_message (word, node_id, sender_id, response):
	message_structure = {}
	message_structure["type"] = search_response_type
	message_structure["word"] = word
	message_structure["node_id"] = node_id
	message_structure["sender_id"] = sender_id
	message_structure["response"] = response
	return json.dumps(message_structure, sort_keys=True, indent=4, separators=(',', ': '))

def build_ping_message (target_id, sender_id, ip_address):
	message_structure = {}
	message_structure["type"] = ping_message
	message_structure["target_id"] = target_id
	message_structure["sender_id"] = sender_id
	message_structure["ip_address"] = ip_address
	return json.dumps(message_structure, sort_keys=True, indent=4, separators=(',', ': '))

def build_ack_message (node_id, ip_address):
	message_structure = {}
	message_structure["type"] = ack
	message_structure["node_id"] = node_id
	message_structure["ip_address"] = ip_address
	return json.dumps(message_structure, sort_keys=True, indent=4, separators=(',', ': '))

def build_ack_index_message (node_id, keyword):
	message_structure = {}
	message_structure["type"] = ack_index_message
	message_structure["node_id"] = node_id
	message_structure["keyword"] = keyword
	return json.dumps(message_structure, sort_keys=True, indent=4, separators=(',', ': '))