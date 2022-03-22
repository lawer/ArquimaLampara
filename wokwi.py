import machine
import time
import network
import ntptime

from umqtt.simple import MQTTClient

import rgb_led
import colors


pir = machine.Pin(15, machine.Pin.OUT)
led = rgb_led.RGBLed(26, 25, 33)


def connect_network(ssid, passwd):
    print("Connecting to WiFi", end="")
    led.set_color(*colors.YELLOW)
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(ssid, passwd)

    while not sta_if.isconnected():
        print(".", end="")
        time.sleep(0.1)

    print(" Connected!")
    led.set_color(*colors.BLUE)
    time.sleep(2)


def connect_mqtt(server):
    client = MQTTClient("umqtt_client", server)
    client.connect()
    client.publish(b"foo_topic", b"hello")
    return client


def get_time():
    try:
        print("Local time before synchronization: %s" % str(time.localtime()))
        # make sure to have internet connection
        ntptime.settime()
        print("Local time after synchronization: %s" % str(time.localtime()))
    except:
        print("Error syncing time")


def main():
    connect_network("Wokwi-GUEST", "")
    get_time()
    client = connect_mqtt("broker.hivemq.com")

    last_event = 0

    while True:
        if pir.value():
            print("ei!")
            led.set_color(*colors.RED)
            event = time.time()

            if event - last_event > 5:
                client.publish(b"ecaib_pir", b"{}".format(time.time()))
                last_event = event
                time.sleep(1)
        else:
            print("nothing!")
            led.set_color(*colors.GREEN)

        time.sleep(1)


if __name__ == "__main__":
    main()
