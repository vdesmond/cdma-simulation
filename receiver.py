import socket
import pickle
import sys
import numpy as np
from walsh_gen import walsh_code_generator

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
		print(f"{self.uId} before = {user_data}")
		user_data = np.reshape(np.sum(data, axis=1)/no_of_users, (1, -1)).astype(int)
		print(f"{self.uId} after = {user_data}")
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
		# print(char)
		binstr = int("".join(str(bit) for bit in char), 2)
		# print(binstr)
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
		user_data = u.decode(channel_data)

		user_message = binarr2text(user_data)
		print(user_message)


if __name__ == "__main__":	
	# Create socket instance
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind((socket.gethostname(), int(sys.argv[1])))
	sock.listen(1)

	conn, _addr = sock.accept()
	print("Received connection from: ", _addr)

	no_of_users = int(sys.argv[2])

	channel_data = pickle.loads(conn.recv(1024 * no_of_users))

	print(channel_data)

	cdma_get_message(no_of_users, channel_data)
	
	conn.close()
		 
