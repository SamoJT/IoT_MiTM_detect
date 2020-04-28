import subprocess
import socket
import time
import sys

print("WARNING: IS PROGRAM RUNNING AS ROOT? \nWILL FAIL IF NOT\n")

def scan(duration):
	''' Run tcpdump network scan '''
	file_name = 'bot' # File name, top or bottom depending on LAN tap
	interface = 'wlan0' # Hardcode for each device
	subprocess.run(['sudo','timeout',str(duration)+'s', 'tcpdump', '-i', interface, '-s', '65535', '-w', file_name+'.pcap'])
	return

def scp():
	src = 'bot.pcap'
	dest = 'root@10.88.1.139:~/IoT_verification/'
	subprocess.run(['scp',src,dest])
	return

def startServer():
	''' Start sever to accept TCP connection from client program '''
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create socket
	server_address = ('localhost', 10000) # Assign IP and Port
	print(f'Starting server {server_address[0]} at port {server_address[1]}')
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Allow resuse of socket
	sock.bind(server_address) # Bind socket
	sock.listen(1) # Listen for connections
	return sock

def listen(sock, duration):
	''' Listen for incoming connection '''
	while True:
		print('Waiting for connection')
		connection, client_address = sock.accept()
		try:
			print('Connection from: ', client_address)
			data = connection.recv(4)
			print(f'Received: {data}')
			if data: # If data not empty reply then start scan
				connection.sendall(b'SCAN')
				print(f"Begining scan: Duration {duration} seconds")
				# scan(duration)
				print("SCANNING\n\n") # Testing purposes
				print("Scan complete\nSending file")
				# scp()
				print("File sent")
			else:
				break
		finally:
			connection.close()
			sock.close() # Need to close to allow anoher to be created
			return

def main():
	duration = 60 # Scan time in seconds

	sock = startServer()
	listen(sock, duration)
	return main()

if __name__ == '__main__':
	main()