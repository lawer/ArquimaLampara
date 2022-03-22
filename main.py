import machine
import time
import network
import ntptime

from umqtt.simple import MQTTClient

import rgb_led
import colors


def connect_network(led, ssid, passwd):
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
    pir = machine.Pin(27, machine.Pin.IN)
    led = rgb_led.RGBLed(18, 19, 5)
    led.set_color(*colors.CYAN)

    connect_network(led, "ECAIB", "08034138")
    get_time()

    client = connect_mqtt("broker.hivemq.com")

    cycle = [colors.BLACK, colors.RED, colors.YELLOW, colors.WHITE]
    index = 0
    cycle_time = 0

    last_event = 0
    while True:
        if pir.value():
            print("ei! - {} - {}".format(time.time(), time.localtime()))
            # led.set_color(*colors.RED)
            event = time.time()

            if event - last_event > 5:
                client.publish(
                    b"ecaib_pir",
                    b"{}".format(time.time()),
                    retain=True
                )
                last_event = event
                print("Enviat!")
        else:
            print("nothing! - {} - {}".format(time.time(), time.localtime()))
            # led.set_color(*colors.GREEN)

        if time.time() - cycle_time > 10:
            index = index + 1
            cycle_time = time.time()
            client.publish(
                "ecaib_color_lamp",
                "{}".format(cycle[index]),
                retain=True
            )

        led.set_color(*cycle[index % len(cycle)])

        time.sleep(1)


if __name__ == '__main__':
    main()
