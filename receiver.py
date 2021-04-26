import socket
import pickle
import sys
import numpy as np
from walsh_gen import walsh_code_generator
from copy import deepcopy

class UserDecode():
	"""Class to contain decoding for CDMA
	"""
	
	def __init__(self, uId, code):

		# * uId is just for logging purposes
		self.uId = uId
		self.code = np.reshape(code, (1, -1))

	def decode(self, data):
		"""Decodes channel data with code of user

		Args:
			data (ndarray): multi-dimensional channel data received from transmitter

		Returns:
			ndarray: Decoded data of current user
		"""
		for i, user_data in enumerate(data):
			data[i] = data[i] * self.code
		user_data = np.reshape(np.sum(data, axis=1)/no_of_users, (1, -1)).astype(int)
		return user_data

def binarr2text(binary_array):
	"""Converts text to binary array 

	Args:
		bin2arr (ndarray): 2D binary array
		
	Returns:
		message (str): text string
	"""
	temp = list(zip(*[iter(binary_array.flat)]*8))
	message = ""

	for char in temp:
		binstr = int("".join(str(bit) for bit in char), 2)
		message += chr(binstr)
	
	return message

def cdma_get_message(no_of_users, channel_data):

	# ? Generate Walsh Matrix 
	# * Use same initial matrix as transmitter to get the same codes
	# TODO: (optional) manual code sequences from user.

	walsh = np.array(walsh_code_generator([[-1]], no_of_users), dtype=int)

	# ? Create user with uid and their respective walsh code
	for i in range(no_of_users):
		u = UserDecode(uId=i, code=walsh[i])
		
		# ? Encodes the data with code and updates the channel data
		# * Deepcopy is done to prevent modifications to channel data

		user_data = u.decode(deepcopy(channel_data))

		user_message = binarr2text(user_data).rstrip()
		print(f"User {u.uId} message is \"{user_message}\"")


if __name__ == "__main__":

	# ? Create socket instance
	# * Connection type is IPv4 and TCP

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind((socket.gethostname(), int(sys.argv[1])))
	sock.listen(1)

	conn, _addr = sock.accept()
	print("Received connection from: ", _addr)

	no_of_users = int(sys.argv[2])

	# * Buffer size might truncate packet if too low
	channel_data = pickle.loads(conn.recv(1024 * no_of_users))

	cdma_get_message(no_of_users, channel_data)
	conn.close()
		 
