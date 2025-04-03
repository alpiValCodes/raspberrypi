import st7735
from PIL import Image
import time
import random
import RPi.GPIO as GPIO

# Initialie stepmotor
in1 = 26
in2 = 5
in3 = 13
in4 = 12

# Initialize both displays with different CS and DC pins
disp1 = st7735.ST7735(
    port=0, 
    cs=0,  # CS for display 1
    dc=9,  # DC for display 1
    backlight=18, 
    rotation=0, 
    spi_speed_hz=4000000,
    invert=False
)

disp2 = st7735.ST7735(
    port=0, 
    cs=1,  # CS for display 2
    dc=6,  # DC for display 2y
    backlight=19, #23
    rotation=0, 
    spi_speed_hz=4000000,
    invert=False
)
'''
disp3 = st7735.ST7735(
    port=0, 
    cs=2,  # CS for display 3
    dc=4,  # DC for display 3
    backlight=20, #23
    rotation=0, 
    spi_speed_hz=4000000,
    invert=True
)'''

disp1.begin()
disp2.begin()


img_black = Image.new('RGB', (disp1.width, disp1.height), (0, 0, 0))
disp1.display(img_black)
disp2.display(img_black)

time.sleep(0.5)
# load pic

img1 = Image.open(f"n{1}.png").resize((disp1.width, disp1.height))
img2 = Image.open(f"n{1}.png").resize((disp2.width, disp2.height))
	
disp1.display(img1)
disp2.display(img2)


print("Both displays are working!")

# careful lowering this, at some point you run into the mechanical limitation of how quick your motor can move
step_sleep = 0.0008

step_count = 12000 # 5.625*(1/64) per step, 4096 steps is 360°

direction = False # True for clockwise, False for counter-clockwise

# defining stepper motor sequence (found in documentation http://www.4tronix.co.uk/arduino/Stepper-Motors.php)
step_sequence = [[1,0,0,1],
                 [1,0,0,0],
                 [1,1,0,0],
                 [0,1,0,0],
                 [0,1,1,0],
                 [0,0,1,0],
                 [0,0,1,1],
                 [0,0,0,1]]  

# setting up
GPIO.setmode( GPIO.BCM )
GPIO.setup( in1, GPIO.OUT )
GPIO.setup( in2, GPIO.OUT )
GPIO.setup( in3, GPIO.OUT )
GPIO.setup( in4, GPIO.OUT )

# initializing
GPIO.output( in1, GPIO.LOW )
GPIO.output( in2, GPIO.LOW )
GPIO.output( in3, GPIO.LOW )
GPIO.output( in4, GPIO.LOW )

motor_pins = [in1,in2,in3,in4]
motor_step_counter = 0 ;

def cleanup():
    GPIO.output( in1, GPIO.LOW )
    GPIO.output( in2, GPIO.LOW )
    GPIO.output( in3, GPIO.LOW )
    GPIO.output( in4, GPIO.LOW )
    GPIO.cleanup()

# the meat
try:
    i = 0
    for i in range(step_count):
        for pin in range(0, len(motor_pins)):
            GPIO.output( motor_pins[pin], step_sequence[motor_step_counter][pin] )
        if direction==True:
            motor_step_counter = (motor_step_counter - 1) % 8
        elif direction==False:
            motor_step_counter = (motor_step_counter + 1) % 8
        else: # defensive programming
            print( "uh oh... direction should *always* be either True or False" )
            cleanup()
            exit( 1 )
        time.sleep( step_sleep )

except KeyboardInterrupt:
    cleanup()
    exit( 1 )

cleanup()
exit( 0 )
