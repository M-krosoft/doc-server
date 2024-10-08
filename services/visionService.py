import base64
import os
import requests

class VisionService:
    def __init__(self):
        self.api_key = os.getenv('GOOGLE_API_KEY')
        self.text_recognition_url = f"https://vision.googleapis.com/v1/images:annotate?key={self.api_key}"

    def detect_text_in_image(self, image_content):

        encoded_image = base64.b64encode(image_content).decode('utf-8')

        request_data = self.get_text_recognition_request_body(encoded_image)

        response = requests.post(self.text_recognition_url, json=request_data)

        if response.status_code == 200:
            json_response = response.json()
            detected_text = json_response['responses'][0].get('textAnnotations', [])
            if detected_text:
                return detected_text[0]['description']
            else:
                return None
        else:
            raise Exception(f"API Error: {response.status_code}, Message: {response.text}")

    @staticmethod
    def get_text_recognition_request_body(encoded_image):
        return {
            "requests": [
                {
                    "image": {
                        "content": encoded_image
                    },
                    "features": [
                        {
                            "type": "TEXT_DETECTION"
                        }
                    ]
                }
            ]
        }
