import threading 
import datetime 
import busio 
import board 
import digitalio 
import math 
import adafruit_mcp3xxx.mcp3008 as MCP 
from adafruit_mcp3xxx.analog_in import AnalogIn 
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)

btn = 26
sample_rate = 10  #  default is 10
start_time = datetime.datetime.now()

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

# create an analog input channel on pin 0
chan = AnalogIn(mcp, MCP.P0)

# creat an analog input channel on pin 1
chan1 = AnalogIn(mcp, MCP.P1)

def timed_thread():
	global sample_rate
	global start_time
	thread = threading.Timer(sample_rate, timed_thread)
	thread.daemon = True
	thread.start()
	current_time = math.trunc((datetime.datetime.now() - start_time).total_seconds())
	print(str(current_time) + "s\t" + str(chan.value) + "\t\t" + str(chan1.value) + "\t\t" + str(round(((chan1.voltage - 0.500)/0.010), 2)) + 'C')
	pass
	#  the Temp sensor needs working, not right

def callback(self):
	global sample_rate
	if sample_rate == 10:
		sample_rate = 5
	elif sample_rate == 5:
		sample_rate = 1
	else:
		sample_rate = 10
	pass

def setup():
	timed_thread() # call it once to start thread
	# GPIO.setmode(GPIO.BOARD)
	GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.add_event_detect(btn, GPIO.FALLING, callback=callback, bouncetime=500)
	pass
if __name__ == "__main__":
	print("Runtime" + "\t" + "LDR Reading" + "\t" + "Temp Reading" + "\t" + "Temp")
	setup() #  call setup

	# tell program to run indefinitely
	while True:
		pass
