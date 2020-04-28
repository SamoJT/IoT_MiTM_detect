from pythonping import ping
from os import path
import subprocess
import socket
import time
import sys

# First run:
#    set IP address, set interface, generate ssh key server, install ssh key on client 
#    https://adamdehaven.com/blog/how-to-generate-an-ssh-key-and-add-your-public-key-to-the-server-for-authentication/
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

def scan(duration):
	''' Run tcpdump network scan '''
	file_name = 'top' # File name, top or bottom depending on LAN tap
	interface = 'wlan0' # Hardcode for each device?
	subprocess.run(['sudo','timeout',str(duration)+'s', 'tcpdump', '-i', interface, '-s', '65535', '-w', file_name+'.pcap'])
	return

def merge():
	''' Merge two pcap files into a single file '''
	targets = ['top.pcap', 'bot.pcap'] # Files to merge
	output = 'merged.pcap'
	subprocess.run(['mergecap',targets[0], targets[1], '-w', output])
	return

def hash():
	''' Utilise JA3.py and generate hashes from merged pcap file '''
	ja3 = '/home/sam/Documents/disso/ja3/python/ja3.py'
	pcap = '/home/sam/Documents/disso/goodCaps/simultaneous_merged.pcap'
	subprocess.call(['python3', ja3 , '--json', pcap])
	return

def checkAlive():
	''' Check if the host is connected to the network '''
	count = 3
	light_ip = '8.8.8.8' # 8.8.8.8 is testing value
	print('Checking if device is up.')
	result = ping(light_ip, count)
	if result.success(): # Successful ping evaluates to True
		return True
	else:
		return False

def connect(addr):
	''' Connect to the TCP server on second device '''
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create socket
	server_address = (addr, 10000) # Set target 
	print(f'Connecting to {server_address[0]} at port {server_address[1]}')
	sock.connect(server_address)
	return sock

def loop(duration, wait_time, addr):
	''' Main body of program '''
	print(f'Waiting for: {wait_time} seconds')
	time.sleep(wait_time)
	try:
		if checkAlive():
			print('Device OK: Proceeding')
			sock = connect(addr)
			sock.sendall(b'SCAN') # Connect to sever, initiate scan
			reply = sock.recv(4)
			if reply: # If data returned scan start
				print(f"Begining scan: Duration {duration} seconds")
				scan(duration)
				# print("SCANNING\n\n") # Testing purposes
				print("Scan complete\nWaiting for file from server")
				time.sleep(0.75)
				if path.exists('bot.pcap') != True:
					print("Failed to get file")
					return
				print("Got file\nMerging files")
				merge() # Need to add try - catch to prevent breaking
				print("Files Merged\nHashing")
				# DO STUFF
			else:
				print("Restarting")
		else:
			print('Host Unreachable')
	finally:
		sock.close()
		loop(duration, wait_time, addr)
def main():
	''' Varaibles kept together for ease of testing '''
	duration = 10 # Scan time in seconds
	wait_time = 10 # Time between scan attempts in seconds
	addr = '10.88.1.128'
	''' ------------------------------------------- '''

	print("WARNING: IS PROGRAM RUNNING AS ROOT? \nWILL FAIL IF NOT\n")
	loop(duration, wait_time, addr)

if __name__ == '__main__':
	main()

