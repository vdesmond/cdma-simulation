import socket
import pickle
import sys

if __name__ == "__main__":	
	# Create socket instance
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind((socket.gethostname(), int(sys.argv[1])))
	sock.listen(1)

	conn, _addr = sock.accept()
	print("Received connection from: ", _addr)
	data = pickle.loads(conn.recv(1024))
	print(data)
	conn.close()
		 
