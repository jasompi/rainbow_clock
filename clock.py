#!/usr/bin/env python

import colorsys
import datetime
import enum
import rainbowhat
import time

HUE_COLD = 225
HUE_WARM = 0

T_COLD = 30
T_WARM = 40

print("Rainbow Clock Started")

def set_rainbow(temp, second=0x7f):
    temp = max(temp,T_COLD)
    temp = min(temp,T_WARM)

    temp -= T_COLD
    temp /= float(T_WARM - T_COLD)

    hue = (1.0-temp) * abs(HUE_WARM - HUE_COLD) / 360.0

    r, g, b = [int(c * 255) for c in  colorsys.hsv_to_rgb(hue, 1.0, 1.0)]

    for i in range(7):
        if second & (1<<i):
            rainbowhat.rainbow.set_pixel(i, r, g, b, brightness=0.1)
        else:
            rainbowhat.rainbow.set_pixel(i, 0, 0, 0)
    rainbowhat.rainbow.show()


class ClockMode(str, enum.Enum):
  TIME = "%H%M"
  DATE = "%m%d"
  YEAR = "%Y"
  WEEKDAY = "%a "

rainbowhat.display.clear()
rainbowhat.display.show()

def show_clock(clock_mode=None):
    if clock_mode:
        show_clock.clock_mode = clock_mode
    if show_clock.clock_mode == ClockMode.TIME:
        show_clock.show_dot = not show_clock.show_dot
    else:
        show_clock.show_dot = False
    now = datetime.datetime.now()
    rainbowhat.display.print_str(now.strftime(show_clock.clock_mode.value))
    rainbowhat.display.set_decimal(1, show_clock.show_dot)
    rainbowhat.display.show()
    temperature = rainbowhat.weather.temperature()
    second = now.second
    set_rainbow(temperature, second)

show_clock.show_dot = False
show_clock.clock_mode = ClockMode.TIME

@rainbowhat.touch.A.press()
def touch_a(channel):
    rainbowhat.lights.rgb(1,0,0)
    show_clock(ClockMode.YEAR)

@rainbowhat.touch.B.press()
def touch_b(channel):
    rainbowhat.lights.rgb(0,1,0)
    show_clock(ClockMode.DATE)

@rainbowhat.touch.C.press()
def touch_c(channel):
    rainbowhat.lights.rgb(0,0,1)
    show_clock(ClockMode.WEEKDAY)

@rainbowhat.touch.release()
def release(channel):
    rainbowhat.lights.rgb(0,0,0)
    show_clock(ClockMode.TIME)


try:
    while True:
        show_clock()
        time.sleep(0.5)

except:
    pass


rainbowhat.display.clear()
rainbowhat.display.show()

print("Rainbow Clock Stopped")
