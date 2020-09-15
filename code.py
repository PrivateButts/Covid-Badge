import time
import board
import busio
import neopixel
import adafruit_us100
import audioio
import displayio
import digitalio
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label
from adafruit_display_shapes.rect import Rect
from gamepadshift import GamePadShift

uart = busio.UART(board.TX, board.RX, baudrate=9600)
# Create a US-100 module instance.
us100 = adafruit_us100.US100(uart)

speakerEnable = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
speakerEnable.switch_to_output(value=True)
dac = audioio.AudioOut(board.SPEAKER)
alert = audioio.WaveFile(open("Alarm2.wav", "rb"))
sound_on = False

BUTTON_LEFT = const(128)
BUTTON_UP = const(64)
BUTTON_DOWN = const(32)
BUTTON_RIGHT = const(16)
BUTTON_SEL = const(8)
BUTTON_START = const(4)
BUTTON_A = const(2)
BUTTON_B = const(1)
pad = GamePadShift(digitalio.DigitalInOut(board.BUTTON_CLOCK),
                   digitalio.DigitalInOut(board.BUTTON_OUT),
                   digitalio.DigitalInOut(board.BUTTON_LATCH))

pixel = neopixel.NeoPixel(
    board.NEOPIXEL, 1, brightness=0.2, auto_write=True, pixel_order=neopixel.GRB
)

trigger_distance = 182.88

display = board.DISPLAY
display.rotation=270

# Set text, font, and color
text = "HELLO WORLD"
font = bitmap_font.load_font("/Helvetica-Bold-16.bdf")
font2 = bitmap_font.load_font("/Dustfine-65.bdf")
color = 0xFFFFFF

top_text_area = label.Label(font, text=text, color=color)
top_text_area.x = 10
top_text_area.y = 20

dist_text_area = label.Label(font2, text="0.00'", color=color)
dist_text_area.x = 10
dist_text_area.y = 80

rect = Rect(0, 0, 140, 160, fill=0x000000)

display_group = displayio.Group(max_size=25)
display_group.append(rect)
display_group.append(top_text_area)
display_group.append(dist_text_area)

current_buttons = pad.get_pressed()
last_read = 0

while True:
    if (last_read + 0.1) < time.monotonic():
        buttons = pad.get_pressed()
        last_read = time.monotonic()
    if current_buttons != buttons:
        # Respond to the buttons
        if (buttons & BUTTON_START) > 0:
            sound_on = True
        elif (buttons & BUTTON_SEL) > 0:
            sound_on = False
            if dac.playing:
                dac.stop()
    temperature = us100.temperature
    distance = us100.distance
    dist_text_area.text = str(round(distance/30.48, 2)) + "'"
    if distance < trigger_distance:
        print("TOO CLOSE!", distance)
        top_text_area.text = "TOO CLOSE!"
        rect.fill = 0xFF0000
        pixel.fill((255, 0, 0))
        if not dac.playing and sound_on:
            dac.play(alert)
    else:
        print("Safe")
        top_text_area.text = "Safe"
        rect.fill = 0x00FF00
        pixel.fill((0, 255, 0))
        if dac.playing:
            dac.stop()
    display.show(display_group)
    time.sleep(.1)