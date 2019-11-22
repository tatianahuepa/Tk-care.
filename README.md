# TK-care

Our project is characterized by the completeness that it has, that is, our device not only offers a type of functionality;the user will be able to guarantee their safety in different ways, either by notifying immediately family members about a possible accident through an email where they will send the location and images of the place, and having a lighting system whenever necessary, which allows the cyclist to be seen and that other vehicles respect the minimum distance of the cyclist.

### Hardware Requirements:

   - Raspberry pi zero w [https://www.raspberrypi.org/products/raspberry-pi-zero-w/]
   - camera module for raspberry [https://www.raspberrypi.org/products/camera-module-v2/]
   - modulo gps REF.neo-6m [https://naylampmechatronics.com/sensores-posicion-inerciales-gps/106-modulo-gps.html]
   - tilt sensor REF.SW-520D [http://tdrobotica.co/sensor-de-inclinacion-sw-520d/1318.html?search_query=sensor+inclinacion&results=9]
   - photoresistor light module [http://tdrobotica.co/sensor-de-luz-modulo-fotoresistencia/779.html?search_query=ldr&results=3]
   - buzzer 6v REF.HS3606 [https://www.tuvoltio.com/categorias/2-electronica/1464-chicharra-6v-hs3606]
   - 1x swith [https://www.didacticaselectronicas.com/index.php/suiches-y-conectores/switch-basculante-3-pines-interruptores-interruptor-suiches-basculante-detail]
   - 2x bottom [https://www.didacticaselectronicas.com/index.php/suiches-y-conectores/suiches/pulsadores/suiche-pulsador-de-2-pines-6mm-x-5mm-momentaneo-moment%C3%A1neo-sw-sw-6x5-2p-sw-057b-switch-suiche-pulsador-lateral-bot%C3%B3n-pulsador-momentaneo-detail]
   - 1x sustained button [https://www.didacticaselectronicas.com/index.php/suiches-y-conectores/switch-pulsador-6-pines-interruptores-interruptor-suiche-4762-detail]
   - MicroSD 32 gb [https://www.sigmaelectronica.net/producto/microsd-32gb/]
   - led lights and laser lights [https://articulo.mercadolibre.com.co/MCO-453595790-stop-luz-led-laser-bicicleta-cicla-luz-trasera-roja-o-azul-_JM?quantity=1#position=1&type=item&tracking_id=fe0d5667-895f-4108-a231-51180c604fa3]
   - regulator step-down REF.LM2596 2A [http://tdrobotica.co/regulador-step-down-lm2596-2a/777.html?search_query=regulador&results=64]
   - LiPo battery [http://tdrobotica.co/bateria-lipo-300mah-74v/290.html?search_query=lipo&results=121]

# Software Requirements:

  - Ubuntu 16.04
  - Python 3 (smtplib,time,MIMEMultipart, MIMEText,MIMEImage,netifaces,gps)

# Steps to enable gps and install libraries:
  - **To enable gps:**

First let's edit the /boot/config.txt file

```sh
sudo nano /boot/config.txt
```
at the end of the document is added:

```sh
dtparam=spi=on
dtoverlay=pi3-miniuart-bt
core_freq=250
enable_uart=1
force_turbo=1
```
By default, bluetooth uses UART(AMA0), with this configuration we will get the gps to use the AMA0 and bluetooth the S0.
Second step, edit file backup :

```sh
sudo nano /boot.cmdline.txt
```
We replace the contents of the file with:

```sh
dwc_otg.lpm_enable=0 console=tty1 root=/dev/mmcblk0p2 rootfstype=ext4 elevator=deadline fsck.repair=yes rootwait quiet splash plymouth.ignore-serial-consoles
```
We reset the raspberry

```sh
sudo reboot
```
The next step is to disable the getty service of the Pi serial, the command will prevent it from starting again when rebooting:

```sh
sudo systemctl stop serial-getty@ttyAMA0.service
sudo systemctl disable serial-getty@ttyAMA0.service
```
We reset the raspberry again

```sh
sudo reboot
```

If we want to check what comes in by the gps, we can perform the following command:

```sh
sudo cat /dev/ttyAMA0
```
Now let's install a daemon to be able to visualize the data in a more attractive way:

```sh
sudo apt-get install gpsd gpsd-clients python-gps 
```
a systemd service that gpsd installs must be disabled.

```sh
sudo systemctl stop gpsd.socket
sudo systemctl disable gpsd.socket
```
To start the program we run:

```sh
sudo gpsd /dev/ttyAMA0 -F /var/run/gpsd.sock
```
Now if we want to test it, we must execute the following order:

```sh
cgsp -s
```
We reset the raspberry again

```sh
sudo reboot
```
Remember that it may be necessary to disable the console serial port with instruction:

```sh
sudo raspi-config
```

  - **To install libraries:**

it is necessary to install and update the libraries.
```sh
sudo apt-get update
sudo apt/get upgrade
```
the necessary bookstores are installed
```sh
pip3 install netifaces
pip3 install pygps
pip3 install smtplib
pip3 install ssh
```
  - **Connect the raspberry to our computer**

To connect the raspberry to our computer, let's change its hostname to easily identify it:
```sh
sudo nano /etc/hosts
```
on the line that says "raspberry", we'll replace this with the hostname we want,we exit and now edit the "hostname" file using the following line:
```sh
sudo nano /etc/hostname
```
We will replace the word "raspberrypi" with the same hostname that we put in the previous file, save and leave the same as before.
Finally, we must make the changes effective by putting the following two lines of code:
```sh
sudo /etc/init.d/hostname.sh
sudo reboot
```
in our computer:
```sh
ssh pi@newname.local
```
# How to execute:

The Raspberry Pi have their own network, which allows connecting to another computer through SSH, as well, to exercise the programs and have a preview of what is being done. For this, we need to be connected to the same wi-fi network on our computer and on the raspberry.
in our computer:
```sh
ssh pi@raspberryhostname.local
```
This will ask us for the password, we enter it and wait. Once connected, we can program our raspberry from here.
Find the folder where the codes are, it is recommended to save them in the location:
```sh
/home/pi/
```
to test the codes separately the following lines are executed:
```sh
python3 gpscorreo2.py
```
or
```sh
python3 ldr2.py
```
Remember that the raspberry camera must be enabled, this can be done with the following instruction:
```sh
sudo raspi-config
```
Once this is done, we need to run the two codes at the same time, that is, in parallel. For this we create a folder on the desktop called tk:
```sh
cd Desktop
mkdir tk
```
we enter this folder and create a file called auto_meg.sh
```sh
cd tk
nano auto-meg.sh
```
here, we write the instruction so that the codes are executed in parallel:
```sh
#!/bin/bash
python3 /home/pi/gpscorreo2.py & 
python3 /home/pi/ldr2.py
```
the first line is used to indicate to the system that instructions in bash language will be executed. we go out and enter the following line
```sh
cd
nano .bashrc
```
At the end of this script we will add the following line:
```sh
sudo gpsd /dev/ttyAMA0 -F /var/run/gpsd.sock
bash /home/pi/Desktop/tk/auto_meg.sh
```
the first line is for enable the gps every time that we reboot the raspberry, and the second is to run the codes as soon as the raspberry is turned on.
We reset the raspberry 
```sh
sudo reboot
```

# **Universidad de Ibagué**
Programa de Ingeniería Electrónica
Electrónica Digital III 2019B
Authors:
  - Ingrid Tatiana Huepa Velasquez
  - karla Liliana Penagos Viatela

Tutor:
Harold F. Murcia
