import lib.st7789py as st7789
import time #mostly fro sleep
from machine import Pin, SoftSPI, reset # for display and buttons
from fonts.romfonts import vga1_16x32 as font
import os
from lib.Button import Button


Button1_Pin = 35; #right button
Button2_Pin = 0;  #left button
val_button1=False
val_button2=False
list_files=0
menu_pos=0
menu_array=[]
windows=0

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
    rotation=0)

display.fill(0)

def clean_menu():
    list_menu=os.listdir()
    list_menu.remove("main.py")
    list_menu.remove("boot.py")
    list_menu.remove("core")
    list_menu.remove("lib")
    list_menu.remove("fonts")
    global menu_array
    menu_array = list_menu
    return list_menu
    
def save(): #Sauvegarde de Main.py
    #display.fill(0)
    f = open('main.py', 'w')
    f2 = open('core/main.txt', 'w')
    command = menu_array[menu_pos]
    array_cmd= command.split(".")
    f.write("import "+array_cmd[0])
    f2.write(command)
    try:
        display.fill(0)
        display.text(font, menu_array[menu_pos]+"        ",0,0 ,st7789.color565(255, 0, 255),st7789.color565(0, 0, 0))
        display.hline(0,33,135,st7789.color565(255, 0, 255))
        display.hline(0,35,135,st7789.color565(255, 0, 255))
        display.text(font, "REBOOT",10,60 ,st7789.color565(255, 0, 0),st7789.color565(0, 0, 0))
        display.text(font, "WAIT",10,90 ,st7789.color565(255, 0, 0),st7789.color565(0, 0, 0))

    except :
        print("error")
    f.close()
    f2.close()
    time.sleep(2)
    reset()
    
def read(): #Sauvegarde de Main.py
    display.fill(0)
    f = open('core/main.txt', 'r')
    file_select = f.read()
    try:
        display.text(font, file_select,0,0 ,st7789.color565(255, 0, 255),st7789.color565(0, 0, 0))
        display.hline(0,33,135,st7789.color565(255, 0, 255))
        display.hline(0,35,135,st7789.color565(255, 0, 255))
    except :
        print("error")
    f.close()
    
def show_menu(pos):
    global list_files
    list_files = len(menu_array)
    for i in range(windows,list_files):
        if i == pos:
            try:
                display.text(font, menu_array[i]+"      ",0,40+(i-windows)*30,st7789.color565(155, 190, 0),st7789.color565(0, 0, 0))
            except :
                print("error")
        else:
            try:
                display.text(font, menu_array[i]+"      ",0,40+(i-windows)*30,st7789.color565(0, 0, 255),st7789.color565(0, 0, 0))
            except :
                print("error")

def menu_moins(p, event):
    global val_button2
    global windows
    if event == Button.RELEASED:
        global menu_pos
        menu_pos= menu_pos - 1
        if menu_pos < 0 :
            menu_pos=0            
        val_button2=False        
        if menu_pos<(windows+1) and windows>0:         
            windows-=1
            
        show_menu(menu_pos)
    if event == Button.PRESSED:        
        val_button2=True
        if val_button1 and val_button2:
            save()
    
def menu_plus(p, event):
    global val_button1
    global windows
    if event == Button.RELEASED:
        global menu_pos
        menu_pos= menu_pos + 1
        if menu_pos > list_files-1 :
            menu_pos = list_files-1
        val_button1=False
        if menu_pos>5:                        
            if windows<list_files-6:
                windows+=1
               
            
        show_menu(menu_pos)
    if event == Button.PRESSED:        
        val_button1=True
        if val_button1 and val_button2:
            save()

button1 = Button(Button1_Pin, callback = menu_plus, internal_pullup = True)
button2 = Button(Button2_Pin, callback = menu_moins, internal_pullup = True)

clean_menu()
read()
show_menu(menu_pos)

while True:
    button1.update()
    button2.update()
   
