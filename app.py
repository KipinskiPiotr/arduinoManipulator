import serial
import time
import os
from pynput import keyboard

red = lambda text: '\033[0;31m' + text + '\033[0m'

step = 1
PORT = 'COM8'

PORT = input('Please enter USB port (COM7 for example): ')

def updateView():
    os.system('cls' if os.name == 'nt' else 'clear')
    print('Use numbers to pick servo and arrows (left and right) to change angle.')
    for s in servos:
        if s == selectedServo:
            print(red(s.name + ': ' + str(s.angle)))
        else:
            print(s.name + ': ' + str(s.angle))
    
class Servo:
    def __init__(self, name, angle, minAngle, maxAngle):
        self.name = name
        self.angle = angle
        self.minAngle = minAngle
        self.maxAngle = maxAngle

    def moveBy(self, angle):
        newAngle = self.angle + angle
        if newAngle >= self.minAngle and newAngle <= self.maxAngle:
            self.angle = newAngle
            return True
        else:
            #print("Cannot exceed angles!")
            return False

servos = [Servo('1', 90, 0, 180), Servo('2', 115, 55, 175), Servo('3', 128, 60, 135), Servo('4', 52, 45, 120)]
selectedServo = servos[0]

ser = serial.Serial(PORT, 115200, timeout=1)
if not ser.isOpen():
    print('Error opening serial port!')

def on_press(key):
    global selectedServo
    try:
        for i, servo in enumerate(servos):
            if key.char == servo.name:
                selectedServo = servos[i]
                #print('Picked Servo ' + servo.name)

    except AttributeError:
        if key == keyboard.Key.left or key == keyboard.Key.right:
            if(selectedServo.moveBy(step if key == keyboard.Key.right else -step)):
                ser.write((selectedServo.name + 'x' + str(selectedServo.angle) + '|').encode())
                ser.flush()
    updateView()

def on_release(key):
    if key == keyboard.Key.esc:
        # Stop listener
        return False

print('Waiting for Arduino to reboot')
time.sleep(3)
updateView()

# Starting keyboard input
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()

ser.close()
print('Serial connection closed!')
