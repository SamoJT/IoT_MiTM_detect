import socket
import sys

def startServer():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create socket
	server_address = ('localhost', 10000) # Assign IP and Port
	print(f'Starting server {server_address[0]} at port {server_address[1]}') 
	sock.bind(server_address) # Bind socket
	sock.listen(1) # Listen for connections
	return sock

def listen(sock):
	while True:
		print('Waiting for connection')
		connection, client_address = sock.accept()
		try:
			print('Connection from: ', client_address)
			data = connection.recv(16)
			print(f'Received: {data}')
			if data:
				connection.sendall(b'Success')
		finally:
			# Clean up the connection
			connection.close()
			return



def main():
	sock = startServer()
	listen(sock)
	print("DONE")

if __name__ == '__main__':
	main()