#!/bin/bash
import subprocess
import netifaces as ni
import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from picamera import PiCamera
from time import sleep
import RPi.GPIO as GPIO
import gps

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

inclinacion=7
#ldr=18 #enviar correo manual
pulsador=13     #pausar o reanudar el sistema
contador=0
buzzer=29
latitud=0
longitud=0
cont=0
sistema=1
#luzadelante=32
#luzatras=37
#luzderecha=23
#luzizquierda=21
#pulsadorluz=24
aux=0
pulsadorapagado=26

GPIO.setup(inclinacion, GPIO.IN)
#GPIO.setup(ldr, GPIO.IN)
GPIO.setup(pulsadorapagado, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(pulsador, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(buzzer, GPIO.OUT)
#GPIO.setup(luz,GPIO.OUT)

def protocoloCorreo(latitud,longitud,mode):
        coordenada="http://www.google.com/maps/place/"+str(latitud)+","+str(longitud)
        if mode==0:
                message = "Sali a montar bici y probablemente me encuentro en una situacion de riesgo. Esta es mi dirección y la imagen capturada por mi sistema  "+coordenada
        else:
                message = "Sali a montar bici y sufri un accidente, por favor comunicate conmigo. Esta es mi direccion y la imagen capturada por mi sistema "+coordenada
        P=PiCamera()
        #P.Resolution=(1024,768)
        P.start_preview()
        sleep(1)
        P.capture('prueba.jpg')
        #time.sleep(2)
        P.stop_preview()
        P.close()
        rutaImagen = 'prueba.jpg'
        proveedor = "smtp.gmail.com"
        puerto = 587
        direccionDe = "2420151014@estudiantesunibague.edu.co"
        contrasenaDe = "ithv1234640687"
        direccionPara = "tatianahuepa1998@gmail.com"                                        # REVISA$
        asunto= "NECESITO TU AYUDA"
        servidor = smtplib.SMTP(proveedor,puerto)
        servidor.starttls()
        servidor.login(direccionDe,contrasenaDe)
        print(servidor.ehlo())
        correo = MIMEMultipart()
        correo['From'] = direccionDe
        correo['To'] = direccionPara
        correo['Subject'] = asunto
        ni.ifaddresses('wlan0')                                                        # REVISAR CAM$
        mensaje = MIMEText(message)
        correo.attach(mensaje)
        picture = open(rutaImagen,"rb")
        imagen = MIMEImage(picture.read())
        # particion = rutaImagen.split("/")
        nombreImagen = rutaImagen #particion[5]
        imagen.add_header('Content-Disposition','attachment',filename = nombreImagen)
        correo.attach(imagen)
        servidor.sendmail(direccionDe,direccionPara,correo.as_string())


def obtainGPS():

        session = gps.gps("localhost", "2947")
        session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
        global contador
        global latitud
        global longitud
        while latitud==0 and longitud ==0: #contador<7:
                report = session.next()
                if report['class']=='TPV':
                        if hasattr(report,'lat'):
                                latitud=report.lat
                        if hasattr(report,'lon'):
                                longitud=report.lon
#               contador+=1
        return latitud,longitud

while(True):
        while GPIO.input(pulsadorapagado)==True:
                sleep(0.1)
                if sistema==1:
                        if GPIO.input(inclinacion)==True:
                                contador+=1
                                print("inclinacion")
                                if GPIO.input(inclinacion)==False:
                                        contador=0
                                while contador>=10000:
                                        print ("caida")
                                        sleep(0.1)
                                        if GPIO.input(pulsadorapagado)==False:
                                                break
                                        for i in range (0,20000):
                                                GPIO.output(buzzer,GPIO.HIGH)
                                                if GPIO.input(pulsador)==False or GPIO.input(inclinacion)==False:
                                                        cont=0
                                                        contador=0
                                                        GPIO.output(buzzer,GPIO.LOW)
                                                        break
                                        if GPIO.input(pulsador)==False or GPIO.input(inclinacion)==False:
                                                cont=0
                                                contador=0
                                                GPIO.output(buzzer,GPIO.LOW)
                                                break
                                        for i in range (0,20000):
                                                GPIO.output(buzzer,GPIO.LOW)
                                                if GPIO.input(pulsador)==False or GPIO.input(inclinacion)==False:
                                                        cont=0
                                                        contador=0
                                                        GPIO.output(buzzer,GPIO.LOW)
                                                        break
                                        if GPIO.input(pulsador)==False or GPIO.input(inclinacion)==False:
                                                cont=0
                                                contador=0
                                                GPIO.output(buzzer,GPIO.LOW)
                                                break
                                        cont+=1
                                        if cont==10:
                                                GPIO.output(buzzer,GPIO.LOW)
                                                mode=1
                                                print ("buscando coordenadas")
                                                lat,lon=obtainGPS()
                                                print (lat,lon)
                                                print("enviando correo")
                                                protocoloCorreo(lat,lon,mode)
                                                sleep(0.3)
                                                print("enviado")
                                                GPIO.output(buzzer,GPIO.HIGH)
                                                sleep(0.2)
                                                GPIO.output(buzzer,GPIO.LOW)
                                                sleep(0.2)
                                                GPIO.output(buzzer,GPIO.HIGH)
                                                sleep(0.2)
                                                GPIO.output(buzzer,GPIO.LOW)
                                                sistema=0
                                                cont=0
                                                break

                        elif GPIO.input(pulsador)==False:
                                mode=0
                                print ("buscando coordenadas")
                                lat,lon=obtainGPS()
                                print (lat,lon)
                                protocoloCorreo(lat,lon,mode)
                                GPIO.output(buzzer,GPIO.HIGH)
                                sleep(0.5)
                                GPIO.output(buzzer,GPIO.LOW)

                if GPIO.input(pulsadorapagado)==False:
                        break


                elif GPIO.input(pulsador)==False:
                        sistema=1
                        contador=0
                        cont=0
                        GPIO.output(buzzer,GPIO.HIGH)
                        sleep(0.2)
                        GPIO.output(buzzer,GPIO.LOW)
                        sleep(0.2)
                        GPIO.output(buzzer,GPIO.HIGH)
                        sleep(0.2)
                        GPIO.output(buzzer,GPIO.LOW)


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




