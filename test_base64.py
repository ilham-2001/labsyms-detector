import cv2
import base64
import numpy as np
import paho.mqtt.client as mqtt
import cv2 as cv
from encode_decode_image import decode_base64_to_image


def on_connect(client, userdata, flags, rc):
    print("[CONNECTED]")


def on_message(client, userdata, msg):
    if msg.topic == "/labsyms/image":
        b64_im = msg.payload.decode().split(",")[1]
        im = decode_base64_to_image(b64_im)
        # print(im)
        cv.imshow("Frame", im)
        cv.waitKey(1)


if __name__ == "__main__":
    mqttc = mqtt.Client(transport="websockets")
    mqttc.connect("127.0.0.1", 9001)

    mqttc.on_connect = on_connect
    mqttc.on_message = on_message

    mqttc.subscribe("/labsyms/image")

    mqttc.loop_forever()