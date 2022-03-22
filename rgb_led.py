import machine
import time

import colors


class RGBLed:
  def __init__(self, red_pin_id, green_pin_id, blue_pin_id):
      self.red_pin = machine.Pin(red_pin_id, machine.Pin.OUT)
      self.green_pin = machine.Pin(green_pin_id, machine.Pin.OUT)
      self.blue_pin = machine.Pin(blue_pin_id, machine.Pin.OUT)

  def set_color(self, r, g, b):
    self.red_pin.value(r)
    self.green_pin.value(g)
    self.blue_pin.value(b)
