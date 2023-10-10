import paho.mqtt.client as mqtt
import cv2 as cv
import numpy as np
from encode_decode_image import decode_base64_to_image


def on_connect(client, userdata, flags, rc):
    print("[CONNECTED]")

def on_message(client, userdata, msg):
    if msg.topic == "/labsyms/image":
        b64_im = msg.payload.decode().split(",")[1]
        im = decode_base64_to_image(b64_im)
        
        cv.imshow("frame", im)
        cv.waitKey(1)


if __name__ == "__main__":
    # print(encode_decode_image.decode_base64_to_image([1, 2, 3, 4]))
    # decode_base64_to_image([[1, 2, 3, 4]])
    mqttc = mqtt.Client(transport="websockets")
    mqttc.connect("127.0.0.1", 9001)

    mqttc.on_connect = on_connect
    mqttc.on_message = on_message

    mqttc.subscribe("/labsyms/image")
    mqttc.loop_forever()
