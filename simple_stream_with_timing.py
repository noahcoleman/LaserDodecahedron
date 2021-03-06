#!/usr/bin/python
import serial
import os
import time as clock
from datetime import datetime
from datetime import time

# x travel = 1400
# total travel on y = 400

# GET FILES FROM CORRECT DIRECTORY
os.chdir('/Users/Noah/Documents/Python/ncFiles') # change present working directory to one with all the files
allFiles = os.listdir('.') # makes an array from the filenames in the pwd
# print allFiles

files = [] # this is the list of files that we will read from in sequence ....
lines = [] # this is the current set of lines

# def initializeMachine(s):
# 	# Zero the printer.
# 	printAndWait(s, "G10P0L20X0Y0\n") # zero out the thing
# 	print "Initialized."

def beginDraw(s):
	print "Begin drawing."
	# If we add this we "force" the machine to always be in an on state, which might not be true if it was in an "off" state when it turned off.
	# printAndWait(s, "M3S255\n") # turn on laser

def endDraw(s):
	printAndWait(s, "M5\n") # turn off laser
	print "endDraw M5"
	printAndWait(s, "G0X0Y0\n") # go to 0,0


def getNextLine():
	global files
	global lines

	if lines:
		return lines.pop(0)
	elif files:
		with open(files.pop(0), 'r') as job:
			lines = job.readlines()
			job.close()
		return getNextLine()
	else:
		files = allFiles[:]
		return getNextLine()

# def printAndWait(s, message): # send a line to serial and wait for a carriage return
# 	print "Sending: " + message

# 	# if(s.port is None):
# 	# 	# Pretend like we're waiting ...
# 	# 	# clock.sleep(0.5)
# 	# 	print "Not connected."
# 	# else:
# 	print ">>> Striping <<<"
# 	l = message.strip() # Strip all EOL characters for consistency
# 	print "stripped >>>" + l + "<<<"  
# 	print "SENDING >>>"
# 	s.write(l + "\n") # Send g-code block to grbl
# 	print "<<<"
# 	print "READING >>>"
# 	grbl_out = s.readline()
# 	print ":" + grbl_out.strip() #print to console for debugging
# 	print "<<<"

def shouldBeOn():
	return True
	# # compare times/ time comparisons compare time to range
	# today = datetime.now()
	# testDay = 3 # dummy value for testing
	# weekday = datetime.weekday(today)
	# if 1 < weekday < 5:
	#	 print "The gallery is open today",
	#	 openTime = time(11, 00) # gallery opens at 11:00
	#	 closeTime = time(18, 00) # gallery closes at 6:00
	#	 testTime = time(15, 30) # dummy value for testing
	#	 t = testTime #datetime.time(today)
	#	 if closeTime > t > openTime:
	#		 print "and it is open now."
	#		 return(1)
	#	 else:
	#		 print "gallery is closed now"
	#		 clock.sleep(0.5)
	#		 return(0)
	# else:
	#	 print "gallery is closed today"
	#	 clock.sleep(0.5)
	#	 return (0)

def main():
	print("Let's get this laser party started!")

	glowWriter =  "/dev/tty.usbmodem1421" # "/dev/ttyACM0" is the default on the RPi "/dev/tty.usbmodem1411" or "/dev/tty.usbmodem1421" on Mac
	# s = serial.Serial()
	# # These are exceptions to keep the program running even if we don't connect to serial.
	# try:
	s = serial.Serial(glowWriter,115200,rtscts=1) # defines the serial port, baud rate, etc.
	# except serial.SerialException as e:
	#	 s = serial.Serial()
	#	 print "Serial error({0}): {1}".format(e.errno, e.strerror)
	# except:
	#	 s = serial.Serial()
	#	 print "Unexpected error:", sys.exc_info()[0]

	# if(s.port is None):
	#	 print("The printer is not connected, sending commands into the abyss.")
	#	 clock.sleep(2)
	# else:
	s.write("\r\n\r\n")
	clock.sleep(2)   # Wait for grbl to initialize 
	s.flushInput()  # Flush startup text in serial input

		# print("Sending to a  %s " % glowWriter)

	# Initialize the machine.
	# initializeMachine(s)
	# printAndWait(s, "G10P0L20X0Y0") # zero out the thing

	wasOn = False

	# HERE IS WHERE ALL THE THINGS THAT SHOULD HAPPEN GO ONCE SERIAL CONNECTION IS ESTABLISHED.
	while True:
		# if shouldBeOn():
		#	 if not wasOn:
		#		 # beginDraw(s)
		#		 wasOn = True

		#	 # Draw the next line.
			# printAndWait(s, getNextLine())



		l = "G91 X10".strip() #getNextLine().strip() # Strip all EOL characters for consistency
		print "stripped >>>" + l + "<<<"  
		print "SENDING >>>"
		s.write(l + "\n") # Send g-code block to grbl
		print "<<<"
		print "READING >>>"
		grbl_out = s.readline()
		print ":" + grbl_out.strip() #print to console for debugging


		# else:
		#	 if wasOn:
		#		 endDraw(s)
		#		 print "M5 G0X0Y0"
		#		 wasOn = False
		#	 # Sleep it for a bit so the while loop doesn't go out of control.

		# # clock.sleep(0.1) # Comment this out when running real code--response from gShield will act as delay


	print("Complete\n")


if __name__ == "__main__":
	main()