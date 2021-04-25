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

	messages = []

	for i in range(no_of_users):
		cur_message = input(f"Enter message for User {i}: ")
		messages.append(cur_message)

	print("\nNO_OF_USERS: {0}\nMESSAGES: {1}".format(no_of_users, messages))
	data = text2binary(messages[0])
	print(data)
	sock.sendall(pickle.dumps(data))
	sock.close()	
