import platform
import os
import sys
import errno
import pwd
try:
	from cStringIO import StringIO
except:
	from StringIO import StringIO

from xmodem import XMODEM,CRC,NAK
import serial
from time import sleep

def readUntil(char = None):
	def serialPortReader():
		while True:
			tmp = port.read(1)
			if not tmp or (char and char == tmp):
				break
			yield tmp
	return ''.join(serialPortReader())


def getc(size, timeout=1):
	return port.read(size)

def putc(data, timeout=1):
	port.write(data)
	sleep(0.001) # give device time to send ACK

port = serial.Serial(port='/dev/ttys001',parity=serial.PARITY_NONE,bytesize=serial.EIGHTBITS)
sleep(2) # give device time to handle command

port.write("xput\r\n")
sleep(0.02)

#readUntil(CRC)
readUntil(NAK)
output = StringIO()
stream = open('test.txt','rb')

for line in stream:
	output.write(line)

XMODEM(getc, putc).send(buffer, crc_mode = 0, quiet = 0)

output.close()

readUntil()
