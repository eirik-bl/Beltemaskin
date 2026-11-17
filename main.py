#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

import _thread
import time

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.

# Create your objects here.

ev3 = EV3Brick()
#robot = DriveBase(motor2,motor1,wheel_diameter=56,axle_track=116) #definerer robot-objektet med klassen DriveBase()

colorSensor = ColorSensor(Port.S4)
nødstopp_sensor = TouchSensor(Port.S1)
info_sensor = TouchSensor(Port.S3)
skyvemotor = Motor(Port.B, positive_direction=Direction.CLOCKWISE, gears=None)
beltemotor = Motor(Port.D, positive_direction=Direction.COUNTERCLOCKWISE, gears=None)

sorteringsfarge = Color.RED
elimineringsfarge1 = Color.YELLOW

fjerner_blokk = False
blokker_fjernet = 0
start_tid = time.time()
current_farge=0
skannede_farger=[0,0,0]

brikke_i_kø = False
har_behandlet_brikke = False

#fargeverdi = 30 # Terskel for at fargen skal bli tatt bort i sjekk_farge - trengs ikke, bruker farge objekt fra pybricks.parameters

# Write your program here.

def ekstra_sjekk():
    global fjerner_blokk
    time.sleep(0.2)
    if sorteringsfarge == farge_skannet:
        fjerner_blokk = False
        fjern_blokk()
    else:
       return


def fjern_blokk():
    global fjerner_blokk
    global blokker_fjernet
    global har_behandlet_brikke
    global brikke_i_kø
    
    fjerner_blokk = True

    blokker_fjernet+=1
    ev3.speaker.beep()

    fjerner_blokk=True
    time.sleep(0.15) # 1 sek vanlig
    stopp_belte()
    skyvemotor.run_time(2000, 500, then=Stop.COAST, wait=True) # for at den ikke skal gå om og om igjen burde vi ha en sjekk for om den allerede fjerner blokker så den ikke vrir seg mer
    skyvemotor.run_time(-2000, 600,then=Stop.COAST, wait=True)
    start_belte()
    time.sleep(0.1)
    if brikke_i_kø:
        brikke_i_kø = False
        _thread.start_new_thread(fjern_blokk, ())
    else:
        fjerner_blokk=False

def sjekk_farge(): # red
    global sorteringsfarge
    global current_farge
    global skannede_farger
    global har_behandlet_brikke
    global brikke_i_kø
    farge_sett = farge_skannet

    if farge_sett != sorteringsfarge:
        har_behandlet_brikke = False
    
    #(red, green, blue) = colorSensor.rgb() # se linje 24

    skannede_farger[current_farge] = farge_sett
    if current_farge <2:
        current_farge +=1
    else:
        current_farge=0
    
    if har_behandlet_brikke:
        return

    if farge_sett == sorteringsfarge:
        if elimineringsfarge1 in skannede_farger:
            print("elimingeringsfarge har blitt skanna forrige " + str(len(skannede_farger)))
            return
        for i in range(3):
            dobbeltsjekk = colorSensor.color()
            print("sjekk " + str(i+1) + "er " + str(dobbeltsjekk))
            time.sleep(0.001)
            if dobbeltsjekk != sorteringsfarge:
                return
            
        har_behandlet_brikke = True

        if fjerner_blokk:
            if not brikke_i_kø:
                brikke_i_kø = True
        else:
            _thread.start_new_thread(fjern_blokk, ())

def info():
    global start_tid
    global blokker_fjernet

    tid_kjørt = int(time.time() - start_tid)
    stopp_belte()
    ev3.screen.clear()
    ev3.screen.print("The belt machine has")
    ev3.screen.print("removed " + str(blokker_fjernet))
    ev3.screen.print("red bricks, and has been")
    ev3.screen.print("going for " + str(tid_kjørt))
    ev3.screen.print("seconds.")
    ev3.speaker.say("The belt machine has removed " + str(blokker_fjernet) + " red bricks, and has been going for " + str(tid_kjørt) + " seconds.")
    start_belte()

def start_belte():
    beltemotor.run(1000) # 300

def stopp_belte():
    beltemotor.brake()

def stopp_sjekk():
    if nødstopp_sensor.pressed():
        stopp_belte()
        print("Nødstopp trykket!")
        raise SystemExit("Nødstopp ble trykket.")

def info_sjekk():
    if info_sensor.pressed():
        info()
        print("Info trykket.")

# Oppstartskode

start_belte()

ev3.speaker.set_speech_options(language='en',voice='m3') # m3
ev3.speaker.set_volume(100, "_all_")

while True:
    farge_skannet=colorSensor.color()
    ev3.screen.clear()
    ev3.screen.print("Røde brikker: " + str(blokker_fjernet))
    sjekk_farge()
    stopp_sjekk()
    info_sjekk()
    time.sleep(0.01)