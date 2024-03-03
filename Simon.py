# Names: Satyendra Raj Singh


import pineworkslabs.RPi as GPIO   #import pineworks
from time import sleep              #import time, it import sleep
from random import choice
import pygame                        
from pygame.mixer import Sound
from random import *
import os

pygame.init()  #initialize the pygame library

GPIO.setmode(GPIO.LE_POTATO_LOOKUP)  #use the Broadcom pin mode

class Button:     # crated class called button

    def __init__(self, switch:int, led:int, sound:str, color:str):   #intilzation
        self.switch = switch
        self.led = led
        self.sound: Sound = Sound(sound)
        self.color = color
        self.setupGPIO()
    
    def setupGPIO(self):
        GPIO.setup(self.switch, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.led, GPIO.OUT)

    def turnlighton(self):    #this function turns the led on
        GPIO.output(self.led, True)

    def turnlightoff(self):   #this function turns the led off
        GPIO.output(self.led, False)

    def is_pressed(self):      #recongizes switch pressed
        return GPIO.input(self.switch)

    def respond(self):        # function that turns led on and off at given time
        self.turnlighton()
        self.sound.play()
        sleep(1)
        self.turnlightoff()
        sleep(0.25)
    
    def __str__(self):
        return self.color


class Simon:     
    
    WELCOME_MESSAGE = "Welcome to Simon! Press ctrl+c to quit at anytime."


    BUTTONS = [
        Button(switch=20, led=6, sound=os.path.join("sounds", "one.wav"), color="red"),
        Button(switch=16, led=13, sound=os.path.join("sounds", "two.wav"), color="blue"),
        Button(switch=12, led=19, sound=os.path.join("sounds", "three.wav"), color="yellow"),
        Button(switch=26, led=21, sound=os.path.join("sounds", "four.wav"), color="green")
    ]         

    def __init__(self, debug=True):   # intilization
        self.debug = debug
        self.sequence: list(Button) = [] 
        self.score = 0

    def debug_out(self, *args):
        if self.debug:
            print(*args)

    def blink_all_buttons(self):  #function cretaed to blink the led bulbs on given time interval
        for button in Simon.BUTTONS:
            button.turnlighton()
            sleep(0.5)
            button.turnlightoff()
            sleep(0.5)

    def add_to_sequence(self):       
        random_Button = choice(Simon.BUTTONS)
        self.sequence.append(random_Button)

    def lose(self):        #
        for _ in range(4):
            self.blink_all_buttons()
        print(f"You made it to a sequence of {self.score}!")
        GPIO.cleanup()
        exit()

    def playback(self):    #function created to blink the bulb in given time interval and speed
        lightspeed = 1
        waitspeed = 0.5
        length = len(self.sequence)
        if length == 13:    #sequence gets 13 notes, time spent in this 0.6 sec 
            lightspeed = 0.6
            waitspeed = 0.15  # it delays the speed 0.15s
        elif length == 10:  #sequence gets 10 notes, time spent in this 0.25
            lightspeed = 0.7
            waitspeed = 0.25
        elif length == 7:
            lightspeed = 0.8
            waitspeed = 0.3
        elif length == 5:
            lightspeed = 0.9
            waitspeed = 0.4
        for Button in self.sequence:
            Button.turnlighton()
            Button.sound.play()
            sleep(lightspeed)
            Button.turnlightoff()
            sleep(waitspeed)

    def wait_for_press(self):
        while True:
            for Button in Simon.BUTTONS:
                if Button.is_pressed():
                    self.debug_out(Button.color)
                    Button.respond()
                    return Button # kill the while true and tell us which button was pressed

    def check_input(self, pressed_Button, correct_Button):
        if pressed_Button.switch != correct_Button.switch:
            self.lose()

        




simon = Simon()
simon.run()
