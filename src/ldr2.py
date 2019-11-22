
#!/bin/bash
import subprocess
from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

ldr=18
luzadelante=32
luzatras=37
luzderecha=23
luzizquierda=21
pulsadorluz=24
aux=0
buzzer=29
pulsadorapagado=26

GPIO.setup(ldr, GPIO.IN)
GPIO.setup(luzadelante,GPIO.OUT)
GPIO.setup(luzatras,GPIO.OUT)
GPIO.setup(luzderecha,GPIO.OUT)
GPIO.setup(luzizquierda,GPIO.OUT)
GPIO.setup(pulsadorluz,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(pulsadorapagado, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(buzzer,GPIO.OUT)

def encenderluces():
        GPIO.output(luzadelante,GPIO.HIGH)
        GPIO.output(luzatras,GPIO.HIGH)
        GPIO.output(luzderecha,GPIO.HIGH)
        GPIO.output(luzizquierda,GPIO.HIGH)
def apagarluces():
        GPIO.output(luzadelante,GPIO.LOW)
        GPIO.output(luzatras,GPIO.LOW)
        GPIO.output(luzderecha,GPIO.LOW)
        GPIO.output(luzizquierda,GPIO.LOW)
    
while(True):
        while GPIO.input(pulsadorapagado)==True:
                sleep(0.2)
                if GPIO.input(ldr)==True:
                        encenderluces()
                        if GPIO.input(pulsadorapagado)==False:
                                break
                        if GPIO.input(pulsadorluz)==True:
                                if GPIO.input(ldr)==True:
                                        sleep(0.3)
                                        for i in range (0,5000):
                                                encenderluces()
                        if GPIO.input(pulsadorapagado)==False:
                                break
                        if GPIO.input(pulsadorluz)==True:
                                if GPIO.input(ldr)==True:
                                        sleep(0.3)
                                        for i in range (0,5000):
                                                encenderluces()
                                                if GPIO.input(pulsadorluz)==False:
                                                        break
                                        if GPIO.input(pulsadorluz)==False:
                                                break
                                        sleep(0.3)
                                        if GPIO.input(pulsadorapagado)==False:
                                                break
                                        for i in range (0,5000):
                                                apagarluces()
                                                if GPIO.input(pulsadorluz)==False:
                                                        break
                                        if GPIO.input(pulsadorluz)==False:
                                                break
                                        if GPIO.input(pulsadorapagado)==False:
                                                break

                elif GPIO.input(ldr)==False:
                        apagarluces()

        if GPIO.input(pulsadorapagado)==False:
                aux+=1
                print ("Cargando")
                if GPIO.input(pulsadorapagado)==True:
                        aux=0
                        print ("0")
                if aux==2000:
                        print ("apagar")
                        GPIO.output(buzzer,GPIO.HIGH)
                        sleep(0.2)
                        GPIO.output(buzzer,GPIO.LOW)
                        sleep(0.1)
                        GPIO.output(buzzer,GPIO.HIGH)
                        sleep(0.2)
                        GPIO.output(buzzer,GPIO.LOW)
                        sleep(0.1)
                        GPIO.output(buzzer,GPIO.HIGH)
                        sleep(0.2)
                        GPIO.output(buzzer,GPIO.LOW)
                        subprocess.call("sudo poweroff",shell=True)
                        break




