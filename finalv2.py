import st7735
from PIL import Image
import time
import cv2
import numpy as np
import random
import RPi.GPIO as GPIO
import threading

gewinn = 0

#stepmotor configs
in1 = 26
in2 = 5
in3 = 13
in4 = 12
step_sleep = 0.0008
step_count = 682 #DAS ISCH PRO 60 GRAD
direction = False
step_sequence = [[1,0,0,1],
                 [1,0,0,0],
                 [1,1,0,0],
                 [0,1,0,0],
                 [0,1,1,0],
                 [0,0,1,0],
                 [0,0,1,1],
                 [0,0,0,1]]
GPIO.setmode( GPIO.BCM )
GPIO.setup( in1, GPIO.OUT )
GPIO.setup( in2, GPIO.OUT )
GPIO.setup( in3, GPIO.OUT )
GPIO.setup( in4, GPIO.OUT )
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


def main_func():
	'''
	global in1
	global in2
	global in3
	global in4
	global step_sleep
	global step_count
	global direction
	global step_sequence
	global motor_pins
	global motor_step_counter
'''
	global in1, in2, in3, in4, step_sleep, step_count, direction, step_sequence, motor_pins, motor_step_counter
	#ALLE BILDER PATHS
	image_paths = ['BAR CASINO NEW.png', 'CHERRY CASINO NEW.png', 'GRAPE CASINO NEW.png', 'JACKPOT CASINO NEW.png', 'NUMBER CASINO NEW.png', 'COIN CASINO NEW.png']

	#AUSGANGSLAGE WIRD DETERMINIERT
	slot_output1 = 'BAR CASINO NEW.png' #random.choice(image_paths)
	slot_output2 = 'BAR CASINO NEW.png' #random.choice(image_paths)

	print(f'OUTPUT 1; {slot_output1}')
	print(f'OUTPUT 2; {slot_output2}')

	def gewinnCALC(slot_output1, slot_output2):
		global gewinn
		if slot_output1 == slot_output2:
			print("win!")
			if slot_output1 == 'JACKPOT CASINO NEW.png':
				gewinn = 10
			if slot_output1 == 'NUMBER CASINO NEW.png':
				gewinn = 7
			if slot_output1 == 'BAR CASINO NEW.png':
				gewinn = 5
			if slot_output1 == 'COIN CASINO NEW.png':
				gewinn = 4
			if slot_output1 == 'GRAPE CASINO NEW.png':
				gewinn = 3
			if slot_output1 == 'CHERRY CASINO NEW.png':
				gewinn = 2
		else:
			print("noob")
			gewinn = 0
			
	gewinnCALC(slot_output1, slot_output2)
	print(f'GEWINN ONB: {gewinn}')


	#ABSPIELLISTE FÜR SCREEN 1 UND 2
	playlist1 = []
	playlist2 = []
	for x in range(9):
		playlist1.append(random.choice(image_paths))
		playlist2.append(random.choice(image_paths))
	for x in range(5): #NOCH PAAR MAL DAMIT DIE ZWEITE LISTE JEWEILS LÄNGER IST
		playlist2.append(random.choice(image_paths))
	playlist1.append(slot_output1)  #ABSPIELLISTE LETZTES ELEMENT IST JEWEILS DAS PREDETERMINIERTE
	playlist2.append(slot_output2)  #ABSPIELLISTE LETZTES ELEMENT IST JEWEILS DAS PREDETERMINIERTE
		
	#ABSPIELLISTE FÜR SCREEN 1 KONVERTIEREN    
	images1 = []
	for path in playlist1:
		img = cv2.imread(path)
		img = cv2.resize(img, (128, 160))
		images1.append(img)
		
	#ABSPIELLISTE FÜR SCREEN 2 KONVERTIEREN    
	images2 = []
	for path in playlist2:
		img = cv2.imread(path)
		img = cv2.resize(img, (128, 160))
		images2.append(img)    
		
	#ABSPIELLISTEN IN CHAT TERMINAL    
	print("playlist 1")
	for e in playlist1:
		print(e)
	print("\n\n\nplaylist 2")
	for e in playlist2:
		print(e)    


	#TRANSITION FÜR SCREEN 1
	def slide_transition1(img1, img2, speed=10):
		height, width = img1.shape[:2]
		for i in range(0, height + 1, 20):
			frame = np.zeros_like(img1)
			frame[:height - i] = img1[i:]
			frame[height - i:] = img2[:i]
			
			# Convert NumPy array to PIL image before displaying
			frame_image = Image.fromarray(frame.astype('uint8'), 'RGB')
			
			disp1.display(frame_image)
			if cv2.waitKey(speed) == 27:
				return False
		return True
		

	#TRANSITION FÜR SCREEN 2 (wenn nicht geht height width in try setzen für error)
	def slide_transition2(img1, img2, speed=10):
		height, width = img1.shape[:2]
		for i in range(0, height + 1, 20):
			frame = np.zeros_like(img1)
			frame[:height - i] = img1[i:]
			frame[height - i:] = img2[:i]
			
			# Convert NumPy array to PIL image before displaying
			frame_image = Image.fromarray(frame.astype('uint8'), 'RGB')
			
			disp2.display(frame_image)
			if cv2.waitKey(speed) == 27:
				return False
		return True    
		

	# Initialize both displays with different CS and DC pins
	disp1 = st7735.ST7735(
		port=0, 
		cs=0,  # CS for display 1
		dc="GPIO24",  # DC for display 1
		backlight="GPIO22",
		rst="GPIO25",
		rotation=180, 	
		spi_speed_hz=16000000,
		invert=False
	)

	disp2 = st7735.ST7735(
		port=0, 
		cs=1,  # CS for display 1
		dc="GPIO23",  # DC for display 1
		backlight="GPIO27",
		rst="GPIO17",
		rotation=180, 	
		spi_speed_hz=16000000,
		invert=False
	)

	# Start both displays
	disp1.begin()
	disp2.begin()

	# Clear both screens
	img_black = Image.new('RGB', (disp1.width, disp1.height), (0, 0, 0))
	disp1.display(img_black)
	disp2.display(img_black)
	time.sleep(0.5)  # Small delay to ensure both are cleared

	#loop
	for index in range(len(playlist1)):
		try: #screen 1
			img = images1[index]
			img2 = images1[index + 1]
			keep_going = slide_transition1(img, img2)
		except:
			continue
		try: #screen 2
			img = images2[index]
			img2 = images2[index + 1]
			keep_going = slide_transition2(img, img2)
		except:
			continue


	for index in range(len(playlist2) - len(playlist1)):
		try:
			time.sleep(0.2)
			img = images2[index + len(playlist1)]
			img2 = images2[index + len(playlist1) + 1]
			keep_going = slide_transition2(img, img2)
		except:
			continue

	#STEPMOTOR GEWINNAUSSCHÜTTUNG
	try:
		print("GEWINNAUSSCHÜTTUNG")
		print(gewinn)
		i = 0
		for i in range(step_count * gewinn):
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

	#cleanup()
	#exit( 0 )


GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Sperre für die Tastenblockade
lock = threading.Lock()
input_enabled = True

def enable_input():
    global input_enabled
    with lock:
        input_enabled = True
        print("Eingabe wieder aktiviert")

def button_pressed(channel):
    global input_enabled
    with lock:
        if not input_enabled:
            print("Eingabe blockiert – Taster ignoriert")
            return
        print("Taster wurde gedrückt!")
        input_enabled = False
        main_func()

    # Starte einen Timer, der nach 5 Sekunden input wieder aktiviert
    timer = threading.Timer(5, enable_input)
    timer.start()

GPIO.add_event_detect(2, GPIO.RISING, callback=button_pressed, bouncetime=300)

try:
    print("Warte auf Tastendruck...")
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Programm beendet")
finally:
    GPIO.cleanup()
    

