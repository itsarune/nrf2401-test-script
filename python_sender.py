from RF24 import RF24, RF24_PA_LOW

# CE = CS1 on usb to sp
# CSN = CS0

import time
import struct

# TODO: update bus
BUS = 0

# TODO: update device
DEVICE = 0

CE_PIN = 2 # gpio 2

CSN_PIN = 0 # spidev 0.0

radio = RF24(CE_PIN, CSN_PIN)

payload = [0]

def setup():
    if not radio.begin():
        raise RuntimeError("radio hardware not responding")

    radio.setPALevel(RF24_PA_LOW)

    radio.openWritingPipe(b"1Node")
    radio.openReadingPipe(1, b"2Node")

    radio.payloadSize = struct.calcsize("i")

    try:
        loop()
    except KeyboardInterrupt:
        radio.powerDown()

def loop():
    radio.stopListening()  # put radio in TX mode
    while True:
        # use struct.pack() to packet your data into the payload
        # "<f" means a single little endian (4 byte) float value.
        buffer = struct.pack("<i", payload[0])
        result = radio.write(buffer)
        if not result:
            print("Transmission failed or timed out")
        else:
            print(
                "Transmission successful!"
            )
            payload[0] += 1
            print(payload[0])
        time.sleep(1)

if __name__ == "__main__":
    setup()
    loop()
