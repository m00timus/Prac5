import threading 
import datetime
import busio
import digitalio
import board
import math
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

sample_rate = 10
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

# print('Raw ADC value: ', chan.value)
# print('ADC Voltage: ' + str(chan.voltage) + 'V')

# print('Raw ADC value for temp sensor: ' + str(chan1.value))
# print('ADC voltage for temp sensor: ' + str(chan1.voltage) + 'V')

def timed_thread():
	global sample_rate
	global start_time
	thread = threading.Timer(sample_rate, timed_thread)
	thread.daemon = True
	thread.start()
	current_time = math.trunc((datetime.datetime.now() - start_time).total_seconds())
	print(str(current_time) + "s\t" + str(chan.value) + "\t\t" + str(chan1.value) + "\t\t" + str(round((chan1.value/600), 2)) + 'C')
	# the Temp sensor needs working, not right
# print(datetime.datetime.now())

if __name__ == "__main__":
	print("Runtime" + "\t" + "LDR Reading" +"\t" + "Temp Reading" + "\t" + "Temp")
	timed_thread() # call it once to start thread

	# tell program to run indefinitely
	while True:
		pass
