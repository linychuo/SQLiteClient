import pymongo

def get_db(host, port, dbname):
	connection = pymongo.Connection(host, port)
	return connection[dbname]

def get_conn(host, port):
	connection = pymongo.Connection(host, port)
	return connection