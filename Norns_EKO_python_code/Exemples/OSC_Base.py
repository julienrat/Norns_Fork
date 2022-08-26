from uosc.client import Bundle, Client, create_message
from time import sleep
import random
from machine import Pin,ADC, SoftSPI
import lib.st7789py as st7789
from fonts.romfonts import vga1_16x16 as font
from fonts.romfonts import vga1_8x8 as mini_font
    
###### Configuration générale

ip_adress = '192.168.0.33' #adresse ip du Norns defaut : 10.42.0.1
port = 10111 #port du Norns defaut : 10111
pot_1 = ADC(Pin(37)) #Broche du capteur analogique numero 1
pot_2 = ADC(Pin(38)) #Broche du capteur analogique numero 2
osc = Client(ip_adress, port) #demarrage du client OSC

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
################################ BOUTONS
Button1_STOP = 35; #Boutons pour coupure de la boucle
Button2_STOP = 0;
pin1 = Pin(Button1_STOP, Pin.IN, Pin.PULL_UP)
pin2 = Pin(Button2_STOP, Pin.IN, Pin.PULL_UP)
#################################################


while True :
    pot_1_value=pot_1.read()*11-3700 #Lecture de la broche capteur analogique 1
    pot_2_value=pot_2.read()*11-300 #Lecture de la broche capteur analogique 1
    random_value=random.uniform(0.1,3.2) #du rendom pour tester
    try : #on essaie d'envoyer les valeurs pour ne pas bbloquer le soft
        b = Bundle()
        b.add(create_message("/params/cutoff", random_value)) #envoi des valeurs en OSC        
        b.add(create_message("/params/release", pot_1_value)) #envoi des valeurs en OSC        
        b.add(create_message("/params/XXXX", pot_2_value)) #envoi des valeurs en OSC
        osc.send(b)
        
        display.text(mini_font, "WIFI OK               ",0,120 ,st7789.color565(24, 255, 0),st7789.color565(0, 0, 0))

    except Exception as e:
        print("ERROR : "+str(e))
        print(e)
        display.text(mini_font, "WIFI PB TRY TO CONNECT",0,120 ,st7789.color565(255, 0, 0),st7789.color565(0, 0, 0))
    ########## AFFICHAGE DANS THONNY ##########################
    print("Random value : ",random_value)
    print("Pot 1        : ",pot_1_value)
    print("Pot 2        : ",pot_2_value)
    ######## AFFICHAGE OLED #######################
    display.text(font, "ENVOI OSC ",0,0 ,st7789.color565(255, 0, 255),st7789.color565(0, 0, 0))
    display.text(mini_font, "--------------------",0,20 ,st7789.color565(0, 0, 255),st7789.color565(0, 0, 0))
    display.text(mini_font, "Rand  : "+str(random_value),0,30 ,st7789.color565(0, 0, 255),st7789.color565(0, 0, 0))
    display.text(mini_font, "Pot 1 : "+str(pot_1_value),0,45 ,st7789.color565(0, 0, 255),st7789.color565(0, 0, 0))
    display.text(mini_font, "Pot 2 : "+str(pot_2_value),0,60 ,st7789.color565(0, 0, 255),st7789.color565(0, 0, 0))
    ###############################################
    sleep(0.5)
    ################ QUITTER LA BOUCLE en appuyant sur un des deux boutons pour programmer
    if(pin1.value()==0 or pin2.value()==0):
        break

