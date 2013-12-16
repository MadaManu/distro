from searchinterface import PeerSearchSimplified
class SearchResult(PeerSearchSimplified):
	# set to default values
	words = []  # strings matched for this url
	url = '' # url matching search query 
	frequency = 0 # number of hits for page 