import time
import RPi.GPIO as GPIO
import os.path
import os.remove
import datetime

from subprocess import call

GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.IN)
light_status_file = 'lightIsOn'
is_light_on = os.path.isfile(light_status_file)
set_light_on_command = 'sudo send 10001 3 1'
set_light_off_command = 'sudo send 10001 3 0'
light_sensor_has_light = 1
light_sensor_has_no_light = 0
on_time = datetime.time(15, 30)
off_time = datetime.time(10, 00)
current_time = datetime.datetime.now()


def is_time_for_light(time_to_check, on_time, off_time):
    if on_time > off_time:
        if time_to_check > on_time or time_to_check < off_time:
            return True
    elif on_time < off_time:
        if time_to_check > on_time and time_to_check < off_time:
            return True
    elif time_to_check == on_time:
        return True
    return False


def switch_light_on(current_time, on_time, off_time):
    if GPIO.input(25) == light_sensor_has_light \
        and False == is_light_on \
        and True == is_time_for_light(current_time, on_time, off_time):
        return True
    else:
        return False


while 1:
    if switch_light_on(current_time, on_time, off_time):
        call(set_light_on_command, shell=True)
        print("send on")
        is_light_on = True
        open(light_status_file, 'a').close()
    if GPIO.input(25) == light_sensor_has_no_light and is_light_on == True and True == is_time_for_light(current_time,
                                                                                                         on_time,
                                                                                                         off_time):
        call(set_light_off_command, shell=True)
        print("send off")
        is_light_on = False
        os.remove(light_status_file)
    print(GPIO.input(25))
    time.sleep(20)


