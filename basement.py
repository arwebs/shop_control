#!/usr/bin/python
import relay8 as r
import RPi.GPIO as GPIO
import time

#x = raw_input("Go...")
#print "after input"

GPIO.setmode(GPIO.BCM)
GPIO.setup(26,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def debounceInput(pin_id):
    initial_value = GPIO.input(pin_id)
    counter = 0
    same_count = 0
    while counter < 20:
        latest_value = GPIO.input(pin_id)
        if latest_value == initial_value:
            same_count = same_count + 1
        time.sleep(0.01)
        counter = counter + 1
    if same_count > 17:
        return initial_value
    #try again if inconclusive
    print "debounce inconclusive"
    return debounceInput(pin_id)


def turnOnOff(val):
	for i in range(0,3):
		for j in range(1,9):
			r.set(i,j,val)
#			time.sleep(0.1)
def setLightMode(modeNumber):
	print "Mode: " + str(modeNumber)
	lightArray = [(1,2),(1,4),(0,3),(0,1),(0,4),(0,2),(0,6),(0,8),
			(0,7),(0,5),(0,3),(0,3),(1,7),(1,5),(2,7),(2,5),
			(2,1),(2,3),(2,8),(2,6),(1,8),(1,6),(2,2),(2,3),
			(1,1),(1,2)]
	if modeNumber == 0:
		for i in range(0,26):
			r.set(lightArray[i][0],lightArray[i][1],i % 2)
	if modeNumber == 1:
		for i in range(0,26):
			r.set(lightArray[i][0],lightArray[i][1],i < 8)
	if modeNumber == 2:
		for i in range(0,26):
			r.set(lightArray[i][0],lightArray[i][1],i < 14)
	if modeNumber == 3:
		for i in range(0,26):
			r.set(lightArray[i][0],lightArray[i][1],i < 14 and i % 2 == 1)
	if modeNumber == 4:
		turnOnOff(True)
#for i in range(0,3):
#	for j in range(1,9):
#		r.set(i,j,1)
#		print str(i) + " " + str(j)
#		time.sleep(0.25)

prevState = False
prevSelectorState = False
mode = 0
while True:
        mainSwitch = debounceInput(26)
	if mainSwitch:
		if not prevState:
			print "Turning On..."
			turnOnOff(True)
		else:
			selectorSwitchOpen = debounceInput(19)
			if not selectorSwitchOpen and prevSelectorState:
				mode = (mode + 1) % 5
				setLightMode(mode)
				print "selector switch" + str(selectorSwitchOpen)
			prevSelectorState = selectorSwitchOpen
	else:
		turnOnOff(False)
#	turnOnOff(mainSwitch)
	prevState = mainSwitch
	#if GPIO.input(26): # and prevState == "off":
	#	turnOnOff(1)
	#	prevState = 1
	#	print "input high"
	#if not GPIO.input(26): # and prevState == "on":
	#	turnOnOff(0)
	#	prevState = 0
	#	print "input low"

y = raw_input("stop....")
for i in range(0,3):
	for j in range(1,9):
		r.set(i,j,0)
GPIO.cleanup()
