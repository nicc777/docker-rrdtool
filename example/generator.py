import time
import datetime
from random import randint
import telnetlib
from math import floor

# Borrowed from http://stackoverflow.com/questions/17610698/python-string-format-percentage-to-one-decimal-place
def floored_percentage(val, digits):
	val *= 10 ** (digits + 2)
	return '{1:.{0}f}%'.format(digits, floor(val) / 10 ** digits)

# Below is my own work... This was a quick hack to get example data in, so it can be optimized. 

TCP_IP = '127.0.0.1'
TCP_PORT = 5000

tn = telnetlib.Telnet(TCP_IP, TCP_PORT)

start_datetime = datetime.datetime.now() - datetime.timedelta(hours=25)
start_timestamp = int(time.mktime(start_datetime.timetuple()))
end_datetime = datetime.datetime.now() - datetime.timedelta(hours=1)
end_timestamp = int(time.mktime(end_datetime.timetuple()))

tstamp = start_timestamp
tn.write(b"BATCH\n")
time.sleep(1)
loop_counter = 0
pdivider = float(end_timestamp)-float(start_timestamp)
fst = float(start_timestamp)
iv = 0

while tstamp < end_timestamp:
	loop_counter += 1
	iv += 1
	if iv > 100:
		progress = (float(tstamp)-fst)/pdivider
		print('Loop nr {}   - {} complete'.format(loop_counter, floored_percentage(progress, 2)))
		iv = 0
	n1 = randint(0,100)
	n2 = randint(0,100)
	s = 'UPDATE random_number.rrd {}:{}:{}'.format(tstamp, n1, n2)
	tn.write(b"{}\n".format(s))
	tstamp += randint(5,15)
	time.sleep(0.02)

tn.write(b".\n")
time.sleep(1)
tn.write(b"QUIT\n")

print('Starting at \'{}\' ({}) and ending at \'{}\' ({})'.format(start_datetime, start_timestamp, end_datetime, end_timestamp))


# EOF
