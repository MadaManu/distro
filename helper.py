import json
import math


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


# FUNCTIONS

# hash function
def hashCode(str_value):
	hash = 0
	for c in str_value:
		hash = hash * 31 + ord(c)
	return math.fabs(hash)

def build_join_message (node_id, target_id, ip_address):
	message_structure = {}
	message_structure["type"] = join_message
	message_structure["node_id"] = node_id # a non-negative number of order 2'^32^', indicating the id of the joining node
	message_structure["target_id"] = target_id # a non-negative number of order 2'^32^', indicating the target node for this message
	message_structure["ip_address"] = ip_address # the ip address of the joining node
	return json.dumps(message_structure, sort_keys=True, indent=4, separators=(',', ': '))

def build_join_relay_message (node_id, gateway_id):
	message_structure = {}
	message_structure["type"] = join_relay_message
	message_structure["node_id"] = node_id
	message_structure["gateway_id"] = gateway_id
	return json.dumps(message_structure, sort_keys=True, indent=4, separators=(',', ': '))

def build_routing_table_message (gateway_id, node_id, ip_address, route_table):
	message_structure = {}
	message_structure["type"] = routing_info_message
	message_structure["gateway_id"] = gateway_id
	message_structure["node_id"] = node_id
	message_structure["ip_address"] = ip_address
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