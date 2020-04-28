from pythonping import ping
import subprocess
import socket
import time
import sys

# Ping Light
# Send start scan msg to server
# Client and server begin scan
# Server send .pcap to client
# Client Merge files
# Client JA3 and JA3S the file
# Check against hash on record
# If issue then send warning
# If not go back to wait
# go to top

def scan():
	''' Run tcpdump network scan '''
	duration = 4 # Scan time in seconds
	file_name = 'top' # File name, top or bottom depending on LAN tap
	interface = 'ens33' # Hardcode for each device?
	subprocess.run(['sudo','timeout',str(duration)+'s', 'tcpdump', '-i', interface, '-s', '65535', '-w', file_name+'.pcap'])
	return

def merge():
	''' Merge two pcap files into a single file '''
	targets = ['top.pcap', 'bot.pcap'] # Files to merge
	output = 'merged.pcap'
	subprocess.run(['mergecap',targets[0], targets[1], '-w', output])
	return

def checkAlive():
	''' Check if the host is connected to the network '''
	light_ip = '8.8.8.8'
	count = 3
	print('Checking if device is up.')
	result = ping(light_ip, count)
	if result.success(): # Successful ping evaluates to True
		return True
	else:
		return False

def connect():
	''' Connect to the TCP server on second device '''
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create socket
	server_address = ('localhost', 10000) # Set target 
	print(f'Connecting to {server_address[0]} at port {server_address[1]}')
	sock.connect(server_address)
	return sock

def loop():
	''' Main body of program '''
	wait_time = 10 # Time between scan attempts in seconds
	print(f'Waiting for: {wait_time} seconds')
	time.sleep(wait_time)
	try:
		if checkAlive():
			print('Device OK: Proceeding')
			sock = connect()
			sock.sendall(b'SCAN') # Connect to sever, initiate scan
			reply = sock.recv(4)
			if reply: # If data returned scan start
				# scan()
				print("SCANNING\n\n") # Testing purposes
			else:
				print("Restarting")
		else:
			print('Host Unreachable')
	finally:
		sock.close()
		loop()
def main():
	input("WARNING: IS PROGRAM RUNNING AS ROOT? \nWILL FAIL IF NOT\nANY KEY TO CONTINUE")
	loop()

if __name__ == '__main__':
	main()

