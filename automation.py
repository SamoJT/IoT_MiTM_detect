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
	light_ip = '10.88.1.52'
	count = 3
	result = ping(light_ip, count)
	if result.success(): # Successful ping evaluates to True
		return True
	else:
		return False

def connect():
	''' Connect to the TCP server on second device '''
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create socket
	server_address = ('localhost', 10000) # Set target 
	print(f'connecting to {server_address[0]} port {server_address[1]}')
	sock.connect(server_address)
	return

def loop():
	''' Main body of program '''
	wait_time = 120 # Time between scan attempts in seconds
	begin = time.time()
	while True:
		if int(time.time()-begin) > wait_time:
			if checkAlive():
				# DO SOMETHING
			else:
				print('Host Unreachable')
				loop()
		else:
			continue

def main():
	pass

if __name__ == '__main__':
	main()
