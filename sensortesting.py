from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

import time
import _thread



colorSensor = ColorSensor(Port.S4)
skyvemotor = Motor(Port.B, positive_direction=Direction.CLOCKWISE, gears=None)


def utfor_en_jobb():
    skyvemotor.run_time(2000, 300, then=Stop.COAST, wait=True) # for at den ikke skal gå om og om igjen burde vi ha en sjekk for om den allerede fjerner blokker så den ikke vrir seg mer
    skyvemotor.run_time(-2000, 300,then=Stop.COAST, wait=True)


while True:
    print(colorSensor.color())
    time.sleep(0.1)
    if colorSensor.color() == Color.RED:
        _thread.start_new_thread(utfor_en_jobb, ())