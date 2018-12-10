import time
import board
import busio

MY_SSID = "foo"
MY_PASSWORD = "bar"

from digitalio import DigitalInOut, Direction, Pull
from adafruit_espatcommands import adafruit_espatcommands

uart = busio.UART(board.TX, board.RX, baudrate=115200, timeout=1)
resetpin = DigitalInOut(board.D3)

print("ESP AT commands")
esp = adafruit_espatcommands.espatcommands(uart, 115200, reset_pin = resetpin, debug=True)

if not esp.soft_reset():
    esp.hard_reset()
    esp.soft_reset()

esp.echo(False)
print("Connected to AT software version ", esp.get_version())
if esp.mode != esp.MODE_STATION:
    esp.mode = esp.MODE_STATION
print("Mode is now", esp.mode)
for ap in esp.scan_APs():
    print(ap)
esp.join_AP(MY_SSID, MY_PASSWORD)
print("My IP Address:", esp.local_ip)