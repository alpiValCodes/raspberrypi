import RPi.GPIO as GPIO
import time

# Setzt den GPIO-Modus auf BCM
GPIO.setmode(GPIO.BCM)

# Definiert den GPIO-Pin, der mit dem Mikro-Schalter verbunden ist
button_pin = 2

# Setzt den GPIO-Pin als Eingang und aktiviert den internen Pull-Down-Widerstand
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Eine Funktion, die ausgeführt wird, wenn der Schalter gedrückt wird
def button_pressed(channel):
    print("Taster wurde gedrückt!")

# Ereignisbindung, um den Taster zu überwachen
GPIO.add_event_detect(button_pin, GPIO.RISING, callback=button_pressed, bouncetime=300)

# Die Hauptschleife, damit das Programm weiterläuft
try:
    print("Warte auf Tastendruck...")
    while True:
        time.sleep(0.1)  # Kurze Pause, um die CPU nicht zu belasten
except KeyboardInterrupt:
    print("Programm beendet")

finally:
    # GPIO-Pins beim Beenden des Programms aufräumen
    GPIO.cleanup()
