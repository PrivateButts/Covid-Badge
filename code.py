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


# User config for convenience
AlarmSample = "Alarm2.wav"
DisplayRotation = 270
TriggerDistance = 182.88 # Use centimeters
LabelFont = "/Helvetica-Bold-16.bdf"
DistanceFont = "/Dustfine-65.bdf"
CycleDelay = .1
BGSafe = 0x00FF00
BGUnsafe = 0xFF0000
TxtSafe = "Safe"
TxtUnsafe = "TOO CLOSE!"
DistanceTextColor = 0xFFFFFF
LabelTextColor = 0xFFFFFF


# Connect to the range finder
uart = busio.UART(board.TX, board.RX, baudrate=9600)
us100 = adafruit_us100.US100(uart)

# Prep the speaker
speakerEnable = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
speakerEnable.switch_to_output(value=True)
dac = audioio.AudioOut(board.SPEAKER)
sound_on = False

# Load the audio file
alert = audioio.WaveFile(open(AlarmSample, "rb"))

# Button Prep
BUTTON_SEL = const(8)
BUTTON_START = const(4)
pad = GamePadShift(
    digitalio.DigitalInOut(board.BUTTON_CLOCK),
    digitalio.DigitalInOut(board.BUTTON_OUT),
    digitalio.DigitalInOut(board.BUTTON_LATCH)
)

# Prep the neopixel
pixel = neopixel.NeoPixel(
    board.NEOPIXEL, 1, brightness=0.2, auto_write=True, pixel_order=neopixel.GRB
)

# Prep the Display
display = board.DISPLAY
display.rotation=DisplayRotation

# Prep Text Elements
font = bitmap_font.load_font(LabelFont)
font2 = bitmap_font.load_font(DistanceFont)

top_text_area = label.Label(font, text="Loading...", color=LabelTextColor)
top_text_area.x = 10
top_text_area.y = 20

dist_text_area = label.Label(font2, text="0.00'", color=DistanceTextColor)
dist_text_area.x = 10
dist_text_area.y = 80

# Prep the background fill
rect = Rect(0, 0, 140, 160, fill=0x000000)

# Display groups for organization
display_group = displayio.Group(max_size=25)
display_group.append(rect)
display_group.append(top_text_area)
display_group.append(dist_text_area)

# Loop prep
current_buttons = pad.get_pressed()
last_read = 0

# Main loop
while True:
    # PyBadges don't like having their input read too fast
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

    # Pull in the latest data
    temperature = us100.temperature
    distance = us100.distance
    dist_text_area.text = str(round(distance/30.48, 2)) + "'"

    # Update display elements
    if distance < TriggerDistance:
        print(TxtUnsafe, distance)
        top_text_area.text = TxtUnsafe
        rect.fill = BGUnsafe
        pixel.fill((255, 0, 0))
        if not dac.playing and sound_on:
            dac.play(alert)
    else:
        print(TxtSafe)
        top_text_area.text = TxtSafe
        rect.fill = BGSafe
        pixel.fill((0, 255, 0))
        if dac.playing:
            dac.stop()

    # Flip the display
    display.show(display_group)

    # Sleep until next cycle
    time.sleep(CycleDelay)