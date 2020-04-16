import subprocess

def main():
	targets = ['top.pcap', 'bot.pcap']
	output = 'merged.pcap'
	subprocess.run(['mergecap',targets[0], targets[1], '-w', output])

if __name__ == '__main__':
	main()