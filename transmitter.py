import socket
import pickle
import sys

def text2binary(message):

	mes2bin = ''.join(format(ord(char), 'b') for char in message)
	return mes2bin

def cdma():

	# TODO not yet implemeted

	pass

if __name__ == "__main__":	
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect(
		(socket.gethostname(), int(sys.argv[1]))
	)

	no_of_users = int(sys.argv[2])
	message = sys.argv[3]

	print("NO_OF_USERS: {0}, MESSAGE: {1}".format(no_of_users, message))
	data = text2binary(message)
	sock.sendall(data)
	sock.close()	
