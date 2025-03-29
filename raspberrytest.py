import time
import random
import _thread
from PIL import Image, ImageDraw, ImageFont
import st7735


# Create ST7735 LCD display class.
disp1 = st7735.ST7735(
    port=0,
    cs=st7735.BG_SPI_CS_BACK,  # BG_SPI_CS_BACK or BG_SPI_CS_FRONT. BG_SPI_CS_FRONT (eg: CE1) for Enviro Plus
    dc="GPIO24",                 # "GPIO9" / "PIN21". "PIN21" for a Pi 5 with Enviro Plus
    backlight="GPIO22", 
    rst="GPIO25",         # "PIN18" for back BG slot, "PIN19" for front BG slot. "PIN32" for a Pi 5 with Enviro Plus
    rotation=0,
    invert=False,
    spi_speed_hz=4000000
)

disp2 = st7735.ST7735(
    port=0,
    cs=st7735.BG_SPI_CS_BACK,  # BG_SPI_CS_BACK or BG_SPI_CS_FRONT. BG_SPI_CS_FRONT (eg: CE1) for Enviro Plus
    dc="GPIO17",                 # "GPIO9" / "PIN21". "PIN21" for a Pi 5 with Enviro Plus
    backlight="GPIO4", 
    rst="GPIO27",         # "PIN18" for back BG slot, "PIN19" for front BG slot. "PIN32" for a Pi 5 with Enviro Plus
    rotation=0,
    invert=True,
    spi_speed_hz=4000000
)

def sec_screen():
    disp2.display(image)


# Initialize display.
WIDTH = disp1.width
HEIGHT = disp1.height

# Initialize display.
disp1.begin()
disp2.begin()
image_file = f"n1.png"
image = Image.open(image_file)
image = image.resize((WIDTH, HEIGHT))

_thread.start_new_thread(sec_screen, ())

disp1.display(image)
