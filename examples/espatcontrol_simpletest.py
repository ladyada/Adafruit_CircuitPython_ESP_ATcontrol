import time
import board
import busio
from digitalio import DigitalInOut
from adafruit_espatcontrol import adafruit_espatcontrol

# Get wifi details and more from a settings.py file
try:
    from settings import settings
except ImportError:
    print("WiFi settings are kept in settings.py, please add them there!")
    raise

uart = busio.UART(board.TX, board.RX, timeout=0.1)
resetpin = DigitalInOut(board.D5)

print("ESP AT commands")
esp = adafruit_espatcontrol.ESP_ATcontrol(uart, 115200, run_baudrate=9600,
                                          reset_pin=resetpin, debug=False)
print("Resetting ESP module")
esp.hard_reset()

while True:
    try:
        print("Checking connection...")
        while not esp.is_connected:
            print("Initializing ESP module")
            #print("Scanning for AP's")
            #for ap in esp.scan_APs():
            #    print(ap)
            # settings dictionary must contain 'ssid' and 'password' at a minimum
            print("Connecting...")
            esp.connect(settings)
            print("Connected to AT software version ", esp.version)
        print("Pinging 8.8.8.8...", end="")
        print(esp.ping("8.8.8.8"))
        time.sleep(10)
    except (RuntimeError, adafruit_espatcontrol.OKError) as e:
        print("Failed to get data, retrying\n", e)
        continue
