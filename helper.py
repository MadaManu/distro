import json

join_message = "JOINING_NETWORK_SIMPLIFIED"

def build_join_message (node_id, target_id, ip_address):
	message_structure = {}
	message_structure["type"] = "JOINING_NETWORK_SIMPLIFIED"
	message_structure["node_id"] = node_id # a non-negative number of order 2'^32^', indicating the id of the joining node
	message_structure["target_id"] = target_id # a non-negative number of order 2'^32^', indicating the target node for this message
	message_structure["ip_address"] = ip_address # the ip address of the joining node
	print "DATA STRUCTURE BUILT!!!!!!"

	return json.dumps(message_structure,sort_keys=True,indent=4, separators=(',', ': '))