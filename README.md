# Covid-Badge
A PyBadge Application that alerts people if they get within 6 ft of the badge holder

## Why?
Bored

## Installation
1. Find a [Circuit Python](https://circuitpython.readthedocs.io/en/5.3.x/README.html) board like the [PyBadge](https://www.adafruit.com/?q=pybadge&sort=BestMatch)
2. Hook up a [US100 Range Finder](https://www.adafruit.com/product/4019) to the UART ports on your board
3. Extract the zip file from the releases tab to the filesystem of your board
4. Turn it on and clip it to a lanyard or badge clip!

## Configuration
Starting on line 16 of the code.py file there is some settings that you can tweak to personalize your device.

- AlarmSample: Filename of the WAV file you want to play if people get too close.
- DisplayRotation: Used for orienting the application's display. Can be 0, 90, 180, or 270. You may have to tweak the position of the display elements if you put it in landscape.
- TriggerDistance: In centimeters, how close you want the trigger distance to be.
- LabelFont: Filename of the BDF font file used for the upper label. [Follow this guide to make BDF files.](https://learn.adafruit.com/custom-fonts-for-pyportal-circuitpython-display/overview)
- DistanceFont: Filename of the BDF font file used for the distance label. [Follow this guide to make BDF files.](https://learn.adafruit.com/custom-fonts-for-pyportal-circuitpython-display/overview)
- CycleDelay: How fast you want the display to refresh.
- BGSafe: HEX color of background when nothing is within TriggerDistance.
- BGUnsafe: HEX color of background when something is within TriggerDistance.
- TxtSafe: Upper label text when nothing is within TriggerDistance.
- TxtUnsafe: Upper label text when something is within TriggerDistance.
- DistanceTextColor: HEX color of distance text.
- LabelTextColor: HEX color of label text.