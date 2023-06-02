from RF24 import RF24, RF24_PA_LOW

CSN_PIN = 10
CE_PIN = 50     # gpio 50

def listen():
    radio.startListening()

    while True:
        has_payload, pipe_number = radio.available_pipe()
        if has_payload:
            # fetch 1 payload from RX FIFO
            buffer = radio.read(radio.payloadSize)
            # use struct.unpack() to convert the buffer into usable data
            # expecting a little endian float, thus the format string "<f"
            # buffer[:4] truncates padded 0s in case payloadSize was not set
            payload[0] = struct.unpack("<f", buffer[:4])[0]
            # print details about the received packet
            print(
                f"Received {radio.payloadSize} bytes",
                f"on pipe {pipe_number}: {payload[0]}",
            )

        # recommended behavior is to keep in TX mode while idle
        radio.stopListening()  # put the radio in TX mode

def main():
    radio = RF24(CE_PIN, CSN_PIN)

    if not radio.begin():
        raise RuntimeError("radio hardware not responding")

    radio.setPALevel(RF24_PA_LOW)

    radio.openReadingPipe(1, b"1Node") 

    radio.payloadSize = struct.calcsize("f")

    try:
        listen()
    except KeyboardInterrupt:
        radio.powerDown()

if __name__ == "__main__":
    main()
