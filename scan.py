import subprocess

def main():
	duration = 4 # Scan time in seconds
	file_name = 'top' # File name, top or bottom depending on LAN tap
	interface = 'ens33' # Hardcode for each device?
	subprocess.run(['sudo','timeout',str(duration)+'s', 'tcpdump', '-i', interface, '-s', '65535', '-w', file_name+'.pcap'])

if __name__ == '__main__':
	main()