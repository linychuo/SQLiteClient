import pymongo

def get_conn(host,port,dbname):
	connection = pymongo.Connection(host,port)
	return connection[dbname]