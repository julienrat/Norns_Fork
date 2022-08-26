from uosc.client import Bundle, Client, create_message
from time import sleep
import random
from machine import Pin,ADC, SoftSPI
import lib.st7789py as st7789
from fonts.romfonts import vga1_16x16 as font
from fonts.romfonts import vga1_8x8 as mini_font
ip_adress = '192.168.0.33' #adresse ip du Norns defaut : 10.42.0.1
port = 10111 #port du Norns defaut : 10111
pot = ADC(Pin(37)) #Broche du capteur analogique
####################### INITIALISATION AFFICHAGE
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
#################################################

osc = Client(ip_adress, port)
while True :
    pot_value=pot.read()*11-3700 #Lecture de la broche capteur analogique
    random_value=random.uniform(0.1,3.2) #du rendom pour tester
    try : #on essaie d'envoyer les valeurs pour ne pas bbloquer le soft
        b = Bundle()
        b.add(create_message("/params/cutoff", random_value)) #envoi des valeurs en OSC
        osc.send(b)
        display.text(mini_font, "WIFI OK               ",0,110 ,st7789.color565(24, 255, 0),st7789.color565(0, 0, 0))

    except Exception as e:
        print("ERROR : "+str(e))
        print(e)
        display.text(mini_font, "WIFI PB TRY TO CONNECT",0,110 ,st7789.color565(255, 0, 0),st7789.color565(0, 0, 0))

    print("Random value : ",random_value)
    ######## AFFICHAGE OLED #######################
    display.text(font, "ENVOI OSC ",0,0 ,st7789.color565(255, 0, 255),st7789.color565(0, 0, 0))
    display.text(font, str(random_value),0,40 ,st7789.color565(255, 0, 255),st7789.color565(0, 0, 0))

    sleep(0.5)

