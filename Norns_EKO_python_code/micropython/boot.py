import lib.st7789py as st7789
import time #mostly fro sleep
from machine import Pin, SoftSPI # for display and buttons
from fonts.romfonts import vga1_bold_16x32 as font
from fonts.romfonts import vga1_8x16 as font2
import os


#Bloc de connexion au réseau Wifi
import network
import time
ssid_name = 'nornscool' #'nornscool'
ssid_passwd = 'nnnnnnnn'#'nnnnnnnn'
eko_name = "Yellow_1"
spi = SoftSPI(
        baudrate=20000000,
        polarity=1,
        phase=0,
        sck=Pin(18),
        mosi=Pin(19),
        miso=Pin(13))

display = st7789.ST7789(
    spi,
    135,
    240,
    reset=Pin(23, Pin.OUT),
    cs=Pin(5, Pin.OUT),
    dc=Pin(16, Pin.OUT),
    backlight=Pin(4, Pin.OUT),
    rotation=1)

display.fill(0)
display.text(font, eko_name ,0,15 ,st7789.color565(255, 0, 255),st7789.color565(0, 0, 0))
time.sleep(2)

sta_if = network.WLAN(network.STA_IF); sta_if.active(True)
sta_if.scan()
sta_if.connect(ssid_name,ssid_passwd)
print("Waiting for Wifi connection")
display.fill(0)
timeout=0
while not sta_if.isconnected():
    time.sleep(1)
    timeout=timeout+1
    print(timeout)
    if timeout > 10 :
        display.fill(st7789.color565(255, 0, 0))
        display.text(font, "Not connected" ,0,15 ,st7789.color565(255, 0, 255),st7789.color565(255, 0, 0))
        time.sleep(2)
        break
    else :
        display.text(font, "Connecting to" ,0,15 ,st7789.color565(255, 0, 255),st7789.color565(0, 0, 0))
        display.text(font, ssid_name ,0,40 ,st7789.color565(255, 0, 255),st7789.color565(0, 0, 0))
        display.text(font, str(10-timeout) ,0,80 ,st7789.color565(255, 0, 255),st7789.color565(0, 0, 0))

if sta_if.isconnected():
    display.fill(0)
    display.text(font, "Connected" ,0,15 ,st7789.color565(255, 0, 255),st7789.color565(0, 0, 0))
    display.text(font, ssid_name ,0,40 ,st7789.color565(255, 0, 255),st7789.color565(0, 0, 0))
    time.sleep(2)
    print("Connected")

# fin du bloc à copier





def read(): #Sauvegarde de Main.py
    display.fill(0)
    f = open('core/main.txt', 'r')
    file_select = f.read()
    try:
        display.text(font, "Running ..." ,40,15 ,st7789.color565(255, 0, 255),st7789.color565(0, 0, 0))
        display.text(font, file_select,40,40 ,st7789.color565(255, 0, 255),st7789.color565(0, 0, 0))
       # display.text(font2, "",10,95 ,st7789.color565(255, 0, 0),st7789.color565(0, 0, 0))
        display.text(font2, "Hold button to enter Menu",15,110 ,st7789.color565(255, 0, 0),st7789.color565(0, 0, 0))
    
    except :
        print("error")
    f.close()
    
Button1_Pin = 35; #right button
Button2_Pin = 0;  #left button

pin1 = Pin(Button1_Pin, Pin.IN, Pin.PULL_UP)
pin2 = Pin(Button2_Pin, Pin.IN, Pin.PULL_UP)
read()
time.sleep(2)
#spi.deinit()

if(pin1.value()==0 or pin2.value()==0):
    print("Enter menu")
    import core.Menu.py

