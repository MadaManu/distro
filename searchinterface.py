class PeerSearchSimplified:
	socket = None
	def __init__ (self, udp_socket):
		# initialise with a udp socket
		socket = udp_socket;
		print socket.getsockname()
		if socket.getsockname()[0] == "127.0.0.1":
			print 'LOCALHOST'
			# add thread to accept connection parse messages and react to messages accordingly
			# some example code of threading at the bottom of the code here
		else:
			print 'NOT FIRST NODE !!!'

	def joinNetwork (self, bootstrap_node):
		print ('HEllo')
		# returns network_id, a locally
		# generated number to identify peer network

	def leaveNetwork (self, network_id):
		# parameter is previously returned peer network identifier
		print ('HEllo')

	def indexPage (self, url, unique_words):
		print (url+' '+str(unique_words))

	def search (self, words):
		print ('HEllo')
