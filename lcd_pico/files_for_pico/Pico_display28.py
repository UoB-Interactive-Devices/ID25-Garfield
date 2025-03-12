import machine
import sdcard
import os
from time import sleep_ms

class ST7789:
    def __init__(self, spi, cs, dc, rst, width=240, height=320):
        self.spi = spi
        self.cs = cs
        self.dc = dc
        self.rst = rst
        self.width = width
        self.height = height

        self.cs.init(self.cs.OUT, value=1)
        self.dc.init(self.dc.OUT, value=1)
        self.rst.init(self.rst.OUT, value=1)

        self.reset()
        self.init_display()

    def reset(self):
        self.rst(1)
        sleep_ms(50)
        self.rst(0)
        sleep_ms(50)
        self.rst(1)
        sleep_ms(50)

    def command(self, cmd):
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def data(self, data):
        self.dc(1)
        self.cs(0)
        self.spi.write(data)
        self.cs(1)

    def init_display(self):
        self.command(0x36)  # MADCTL
        self.data(bytearray([0x00]))  # Normal orientation (adjust if needed)

        self.command(0x3A)  # COLMOD - Pixel format
        self.data(bytearray([0x55]))  # 16-bit color (RGB565)

        self.command(0x21)  # Display Inversion On (for most ST7789 panels)

        self.command(0x11)  # Sleep Out
        sleep_ms(120)

        self.command(0x29)  # Display On

    def set_window(self, x0, y0, x1, y1):
        self.command(0x2A)  # Column Address Set
        self.data(bytearray([
            x0 >> 8, x0 & 0xFF,
            x1 >> 8, x1 & 0xFF
        ]))

        self.command(0x2B)  # Row Address Set
        self.data(bytearray([
            y0 >> 8, y0 & 0xFF,
            y1 >> 8, y1 & 0xFF
        ]))

        self.command(0x2C)  # Memory Write - start sending pixel data

    def display_raw_image(self, filename):
        """Load and display a raw 240x320 RGB565 image from SD card."""
        self.set_window(0, 0, self.width - 1, self.height - 1)

        with open(filename, 'rb') as f:
            buffer = bytearray(512)
            while True:
                read_bytes = f.readinto(buffer)
                if not read_bytes:
                    break
                self.data(buffer[:read_bytes])

# Pin setup (adjust as needed)
LCD_DC = machine.Pin(8, machine.Pin.OUT)
LCD_CS = machine.Pin(9, machine.Pin.OUT)
LCD_SCK = machine.Pin(10)
LCD_MOSI = machine.Pin(11)
LCD_MISO = machine.Pin(12)
LCD_BL = machine.Pin(13, machine.Pin.OUT)
LCD_RST = machine.Pin(15, machine.Pin.OUT)
SD_CS = machine.Pin(22, machine.Pin.OUT)

# SPI setup (shared for SD card and LCD)
spi = machine.SPI(1, baudrate=20000000, polarity=0, phase=0,
                  sck=LCD_SCK, mosi=LCD_MOSI, miso=LCD_MISO)

# Mount the SD card
sd = sdcard.SDCard(spi, SD_CS)
os.mount(sd, '/sd')

# Turn on the backlight
LCD_BL.on()

# Initialize the ST7789 display
lcd = ST7789(spi, LCD_CS, LCD_DC, LCD_RST, width=240, height=320)

choice = input("Enter 1 or 2: ")

if choice == "1":
    # Display series for choice 1
    lcd.display_raw_image('/sd/hru/hruf1.raw')
    sleep_ms(1000)  # Wait 3 seconds
    lcd.display_raw_image('/sd/hru/hruf2.raw')
elif choice == "2":
    # Display series for choice 2
    lcd.display_raw_image('/sd/image4.raw')
    sleep_ms(1000)  # Wait 3 seconds
    lcd.display_raw_image('/sd/image5.raw')
else:
    print("Invalid choice. Please enter 1 or 2.")

# Unmount the SD card
os.umount('/sd')

print("Image displayed.")

