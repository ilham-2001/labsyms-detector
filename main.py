import cv2 as cv
import paho.mqtt.client as mqtt
from encode_decode_image import encode_image_to_base64
from model import detect_object

def on_connect(client, userdata, flags, rc):
    print(f"[CONNECTED] with code {rc}")

cam = cv.VideoCapture(0)

mqttc = mqtt.Client(transport="websockets")
mqttc.connect("127.0.0.1", 9001)

mqttc.on_connect = on_connect

# mqttc.loop_forever()

mqttc.loop_start()


while True:
    _, frame = cam.read()
    detected_im, labels = detect_object(frame)
    im = cv.resize(detected_im, (520, 320))
    im64 = encode_image_to_base64(im)

    mqttc.publish("/labsyms/gloves-info", labels[0])
    mqttc.publish("/labsyms/mask-info", labels[1])
    mqttc.publish("/labsyms/coat-info", labels[2])
    mqttc.publish("/labsyms/enter-info", labels[3])
    mqttc.publish("/labsyms/image", im64)