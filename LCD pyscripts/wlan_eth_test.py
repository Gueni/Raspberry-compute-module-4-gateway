
import os
import time
import math
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import subprocess

# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used
# 128x32 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=0x3C)
# Initialize library.
disp.begin()
# Clear display.
disp.clear()
disp.display()
# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)
# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=255)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0
# Load default font.
font = ImageFont.load_default()
offset = height/2-4
# Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
# font = ImageFont.truetype('Minecraftia.ttf', 8)

while True:

        #'\' is used to splite python line
    ipaddress = os.popen("ifconfig wlan0 \
                        | grep 'inet addr' \
                        | awk -F: '{print $2}' \
                        | awk '{print $1}'").read()
    ssid = os.popen("iwconfig wlan0 \
                    | grep 'ESSID' \
                    | awk '{print $4}' \
                    | awk -F\\\" '{print $2}'").read()

    print("ssid: " + ssid)
    print("ipaddress: " + ipaddress)

    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    cmd = "hostname -I | cut -d\' \' -f1"
    IP = subprocess.check_output(cmd, shell = True )

    cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
    CPU = subprocess.check_output(cmd, shell = True )

    cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell = True )

    cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
    Disk = subprocess.check_output(cmd, shell = True )
    y   = offset
    # Write two lines of text.
    draw.text((x, y),       "ssid: " + str(ssid),  font=font, fill=0)
    # Display image.
    disp.image(image)
    disp.display()
    time.sleep(2)
    # Clear display.
    disp.clear()
    disp.display()

    draw.text((x, y),       "IP: " + str(IP),  font=font, fill=0)
    # Display image.
    disp.image(image)
    disp.display()
    time.sleep(2)
    # Clear display.
    disp.clear()
    disp.display()
    
    draw.text((x, y),     str(CPU), font=font, fill=0)
       # Display image.
    disp.image(image)
    disp.display()
    time.sleep(2)
    # Clear display.
    disp.clear()
    disp.display()
    draw.text((x, y),    str(MemUsage),  font=font, fill=0)
       # Display image.
    disp.image(image)
    disp.display()
    time.sleep(2)
    # Clear display.
    disp.clear()
    disp.display()
    draw.text((x, y),    str(Disk),  font=font, fill=0)
       # Display image.
    disp.image(image)
    disp.display()
    time.sleep(2)
    