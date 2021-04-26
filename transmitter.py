import socket
import pickle
import sys
import numpy as np
from walsh_gen import walsh_generator_matrix

class UserPair():
    def __init__(self, uId, code):
        self.uId = uId
        self.code = np.reshape(code, (1, -1))


def text2binarr(message):

	mes2bin = "".join(f"{ord(char):08b}" for char in message)
	bin2arr = np.array([[int(i) for i in mes2bin]], dtype=int)
	return bin2arr

def cdma(no_of_users, messages):

	userPairs = []

	# Find longest message
	max_len = len(max(messages, key=len))
	print(max_len)
	equilen_messages = [msg.ljust(max_len, ' ') for msg in messages]

	walsh = np.array(walsh_generator_matrix([[-1]], no_of_users), dtype=int)
	
	symbols = map(text2binarr, equilen_messages)
	for symbol in symbols:
		print(symbol)
		print(symbol.shape)

	channel = np.zeros((max_len, walsh.shape[0]), dtype=int)


	return "10000010011" # temp

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
	data = cdma(no_of_users, messages)
	sock.sendall(pickle.dumps(data))
	sock.close()	
