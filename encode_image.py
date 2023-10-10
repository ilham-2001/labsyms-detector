import base64
import cv2 as cv

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