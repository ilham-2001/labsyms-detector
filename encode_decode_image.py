import base64
import cv2 as cv
import numpy as np

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