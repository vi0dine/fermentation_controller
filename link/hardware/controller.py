import RPi.GPIO as GPIO
from w1thermsensor import W1ThermSensor
import time
import board
import neopixel
import time
from database import db

GPIO.setmode(GPIO.BCM)

HEATER_PIN = 22
COOLER_PIN = 23
LED_RING_PIN = board.D18
LEDS_COUNT = 16

GPIO.setup(HEATER_PIN, GPIO.OUT)
GPIO.setup(COOLER_PIN, GPIO.OUT)
GPIO.output(HEATER_PIN, GPIO.HIGH)
GPIO.output(COOLER_PIN, GPIO.HIGH)

sensor = W1ThermSensor()
pixels = neopixel.NeoPixel(LED_RING_PIN, LEDS_COUNT, brightness = 0.4)
conn = db.create_connection(r"./brew_valley_link.db")

current_batch = None
current_step = None
desired_temperature = None

def call():
    current_batch = db.get_current_batch(conn)
    current_step = db.get_current_step(conn)

    while True:
        desired_temperature = current_step["temperature"]
        temperature = sensor.get_temperature()
        check_temperature_settings(temperature)
        change_step()
        led_cycle(220, 0, 255, 0.05, 1)
        db.create_reading(conn, current_batch, current_step, temperature)
        time.sleep(30)

def check_temperature_settings(current):
    if abs(temperature - desired_temperature) > hysteresis:
        if temperature > desired_temperature:
            toggle_heater("OFF")
            time.sleep(1)
            toggle_cooler("ON")
        elif temperature < desired_temperature:
            toggle_cooler("OFF")
            time.sleep(1)
            toggle_heater("ON")

def change_step():
    if current_step["end_date"] >= time.time():
        steps = db.get_steps(conn)
        current_index = steps.index(current_step)
        if steps[current_index + 1]:
            current_step = steps[current_index + 1]


def toggle_heater(state):
    if state == "ON" and GPIO.input(HEATER_PIN):
        led_cycle(255, 0, 0)
        GPIO.output(HEATER_PIN, GPIO.LOW)
    elif state == 'OFF' and not GPIO.input(HEATER_PIN):
        GPIO.output(HEATER_PIN, GPIO.HIGH)

def toggle_cooler(state):
    if state == "ON" and GPIO.input(COOLER_PIN):
        led_cycle(0, 0, 255)
        GPIO.output(COOLER_PIN, GPIO.LOW)
    elif state == "OFF" and not GPIO.input(COOLER_PIN):
        GPIO.output(COOLER_PIN, GPIO.HIGH)


def led_cycle(r,g,b, wait = 0.01, occurences = 3):
    for _ in range(occurences):
        for i in range(LEDS_COUNT):
            pixels[i] = (r, g, b)
            time.sleep(wait)
        for i in range(LEDS_COUNT):
            pixels[i] = (0, 0, 0)
            time.sleep(wait)