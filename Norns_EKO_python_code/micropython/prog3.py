#programme2
import lib.st7789py as st7789
from machine import Pin, SoftSPI # for display and buttons
from fonts.romfonts import vga1_16x32 as font

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

display.text(font, "Prog 3",0,0 ,st7789.color565(255, 0, 255),st7789.color565(0, 0, 0))
     