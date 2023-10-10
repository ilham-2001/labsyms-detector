import cv2 as cv
import paho.mqtt.client as mqtt
import numpy as np
import base64
from model import create_boundingbox
import json

def decode_base64_to_image(base64_encoded_image_str):
    try:
        # Decode the base64 string to bytes
        img_data = base64.b64decode(base64_encoded_image_str)
        
        # Convert bytes to numpy array
        nparr = np.frombuffer(img_data, np.uint8)
        
        # Decode numpy array to image using OpenCV
        img = cv.imdecode(nparr, cv.IMREAD_COLOR)
        
        return img
    except Exception as e:
        print("Error:", str(e))
        return None


def encode_image_to_base64(im):
    try:
        # Convert the image array to bytes
        _, img_encoded = cv.imencode('.jpg', im)
        
        # Encode the image bytes into base64
        base64_encoded_image = base64.b64encode(img_encoded)

        # Convert the base64 bytes to a string
        base64_encoded_image_str = base64_encoded_image.decode('utf-8')

        return base64_encoded_image_str
    except Exception as e:
        print("Error:", str(e))
        return None
    

def on_connect(client, userdata, flags, rc):
    print("[CONNECTED]")

def on_message(client, userdata, msg):
    if msg.topic == "/labsyms/image":
        b64_im = msg.payload.decode().split(",")[1]
        im = decode_base64_to_image(b64_im)
        # cv.imshow("frame", im)
        # cv.waitKey(1)
        bb = json.dumps(create_boundingbox(im))
        client.publish("/labsyms/image-pos", bb)

if __name__ == "__main__":
    # print(encode_decode_image.decode_base64_to_image([1, 2, 3, 4]))
    # decode_base64_to_image([[1, 2, 3, 4]])
    mqttc = mqtt.Client(transport="websockets")
    mqttc.connect("127.0.0.1", 9001)

    mqttc.on_connect = on_connect
    mqttc.on_message = on_message

    mqttc.subscribe("/labsyms/image")
    mqttc.loop_forever()
