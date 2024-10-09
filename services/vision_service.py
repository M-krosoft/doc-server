import base64
import os
import requests

class VisionService:
    def __init__(self):
        self.api_key = os.getenv('GOOGLE_API_KEY')
        self.text_recognition_url = f"https://vision.googleapis.com/v1/images:annotate?key={self.api_key}"

    def detect_text_in_image(self, image_content: bytes) -> str | None:

        encoded_image = base64.b64encode(image_content).decode('utf-8')
        request_data = self.get_text_recognition_request_body(encoded_image)
        
        try:
            response = requests.post(self.text_recognition_url, json=request_data)
            response.raise_for_status()
            
            json_response = response.json()
            detected_text = json_response['responses'][0].get('textAnnotations', [])
            
            if detected_text:
                return detected_text[0]['description']
            else:
                return None
        except requests.exceptions.RequestException as e:
            raise Exception(f"API error: {e}")

    @staticmethod
    def get_text_recognition_request_body(encoded_image: str) -> dict:
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
