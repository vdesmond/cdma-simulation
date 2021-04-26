import socket
import pickle
import sys
import numpy as np
import utils
from copy import deepcopy
import logging

# ? Configure logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


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


def cdma_get_message(no_of_users, channel_data):
	"""
	This function recovers the individual messages from channel data using the 
	walsh codes for each user.

	Args:
		no_of_users (int): number of users that send data in the channel
		channel_data (ndarray): 2D array containing all data in channel
	"""

	# ? Generate Walsh Matrix 
	# * Use same initial matrix as transmitter to get the same codes
	# TODO: (optional) manual code sequences from user.

	walsh = np.array(utils.walsh_code_generator([[-1]], no_of_users), dtype=int)

	# ? Create user with uid and their respective walsh code
	for i in range(no_of_users):
		u = UserDecode(uId=i, code=walsh[i])
		
		# ? Encodes the data with code and updates the channel data
		# * Deepcopy is done to prevent modifications to channel data

		user_data = u.decode(deepcopy(channel_data))

		logging.debug("Decoded symbol for User %d:", u.uId)
		logging.debug(user_data)

		user_message = utils.binarr2text(user_data).rstrip()
		logging.info(f"User {u.uId} message is \"{user_message}\"")


if __name__ == "__main__":

	# ? Create socket instance
	# * Connection type is IPv4 and TCP

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind((socket.gethostname(), 3300))
	sock.listen(1)

	conn, _addr = sock.accept()
	logging.info(f"Received connection from: {_addr}")

	no_of_users = int(sys.argv[1])

	# * Buffer size might truncate packet if too low
	channel_data = pickle.loads(conn.recv(4096 * no_of_users))
	logging.debug(f"Received channel matrix\n{channel_data}")

	cdma_get_message(no_of_users, channel_data)
	conn.close()
		 
