import uasyncio as asyncio

import machine
import time

import ssd1306

OLED = None
PIR = None

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LILA = (165, 105, 189)

RED_PIN_PWM, GREEN_PIN_PWM, BLUE_PIN_PWM = None, None, None


def set_led(r, g, b):
    RED_PIN_PWM.duty(r * 4)
    GREEN_PIN_PWM.duty(g * 4)
    BLUE_PIN_PWM.duty(b * 4)


def apagar_led():
    set_led(0, 0, 0)


def setup_led(red_pin_id, green_pin_id, blue_pin_id):
    global RED_PIN_PWM, GREEN_PIN_PWM, BLUE_PIN_PWM
    red_pin = machine.Pin(red_pin_id, machine.Pin.OUT)
    green_pin = machine.Pin(green_pin_id, machine.Pin.OUT)
    blue_pin = machine.Pin(blue_pin_id, machine.Pin.OUT)
    RED_PIN_PWM = machine.PWM(red_pin, freq=2000)
    GREEN_PIN_PWM = machine.PWM(green_pin, freq=2000)
    BLUE_PIN_PWM = machine.PWM(blue_pin, freq=2000)


def setup_oled():
    i2c = machine.SoftI2C(scl=machine.Pin(15), sda=machine.Pin(2))
    oled_width = 128
    oled_height = 64
    oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
    oled.show()

    return oled


async def main():
    global PIR
    global OLED

    setup_led(red_pin_id=18, green_pin_id=19, blue_pin_id=5)

    OLED = setup_oled()

    PIR = machine.Pin(27, machine.Pin.IN)  # create input pin on GPIO2
    # pir.irq(trigger=machine.Pin.IRQ_RISING, handler=detecta)

    while True:
        if PIR.value():
            set_led(*RED)
            # OLED.text("Pillat!", 0, 0)
            # OLED.scroll(0, 10)
            # OLED.show()
        else:
            set_led(*GREEN)


asyncio.run(main())
