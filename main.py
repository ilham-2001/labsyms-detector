import cv2 as cv
import paho.mqtt.client as mqtt
from encode_decode_image import encode_image_to_base64
from model import detect_object

def on_connect(client, userdata, flags, rc):
    print(client)
    print("[CONNECTED]")

cam = cv.VideoCapture(0)

mqttc = mqtt.Client(transport="websockets")
mqttc.connect("127.0.0.1", 9001)

mqttc.on_connect = on_connect

# mqttc.loop_forever()

mqttc.loop_start()


while True:
    _, frame = cam.read()
    detected_im = detect_object(frame)
    im64 = encode_image_to_base64(detected_im )

    mqttc.publish("/labsyms/image", im64)