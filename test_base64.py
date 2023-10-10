import cv2
import base64
import numpy as np
import paho.mqtt.client as mqtt
import cv2 as cv


def on_connect(client, userdata, flags, rc):
    print("[CONNECTED]")


def on_message(client, userdata, msg):
    if msg.topic == "/labsyms/image":
        b64_im = msg.payload.decode().split(",")[1]
        im = decode_base64_to_image(b64_im)
        # print(im)
        cv.imshow("Frame", im)
        cv.waitKey(1)


def decode_base64_to_image(base64_encoded_image_str):
    try:
        # Decode the base64 string to bytes
        img_data = base64.b64decode(base64_encoded_image_str)
        
        # Convert bytes to numpy array
        nparr = np.frombuffer(img_data, np.uint8)
        
        # Decode numpy array to image using OpenCV
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        return img
    except Exception as e:
        print("Error:", str(e))
        return None

if __name__ == "__main__":
    mqttc = mqtt.Client(transport="websockets")
    mqttc.connect("127.0.0.1", 9001)

    mqttc.on_connect = on_connect
    mqttc.on_message = on_message

    mqttc.subscribe("/labsyms/image")

    mqttc.loop_forever()