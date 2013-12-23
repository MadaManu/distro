CS4032 - Distributed Systems Project

Vladut M. Druta
10345527

In order to run the tests, execute the file main.py (optional argument --port and the value of the port to use). If no specific port given it will default to start from: 8767
Warning: The program will run 4 ports including the specified one in ascending order!

The implementation is done based on the simplified specifications, therefore ignoring the PING and simple ACK of the PING, because there was mentioning that a dead node can be left out. Therefore the assumption was that all nodes are alive, therefore no need for a ping to check their availability. 

The implementation is straight forward and the code is commented throughout. 
For a general description of the code in a few lines, I would mention that each node stores a routing table as a python dict mapping another nodes id to a tuple (tuple consisting of IP and port on which that node is accepting messages). 
The node also saves a dict mapping the urls to a count of how many times that url was indexed for the specific word that the node indexes. 
There was a need of a temporary table that would store very similar information as the routing table, and this would act as a temporary bootstrap. 
This temporary table comes in place when a node joins through another node, and there is need to route the joining relay through multiple nodes until it finds it's final destination. 
To be able to route the routing information from the node that added the joining node, the temporary table will be able to map where the joining node can be found (backwards). 
Therefore the use of the temporary table. This temporary table would store a mapping of the node_id that wants to join, and where the request came from. So it could be another node id, or it could be an ip, port tuple.
Again, this is to facilitate the return message containing the routing information the joining node needs in order to be able to route messages accross the network (and implicitly to be part of the network).

The index function is implemented and can be used by all nodes. The index just forwards the request to the node that is indexing the specified word, and once the message is routed to it, it will add the urls (pages) to the table that it already has, returning to the sender node an acknoledgement of saving those indexes.

A search message would route around the network, and once it reaches the node that indexed the keyword, will responde with a search respond containing all the information that the node has on the urls (links/pages) indexed for that specific keyword. This search response will be routed through the network getting back to the originator node of the search.

I have made a helper module (helper.py) to include a few helpfull functions, mainly to build messages that will be sent accross the networ, and encode them in json format. This module also provides a few other functions that are self explanatory and more detailed explanations about them are found in the comments. (e.g: append_to_routing_table, prettyPrint ...)
