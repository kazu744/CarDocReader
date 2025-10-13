import base64
import requests


def detect_text_from_image(contents: bytes, vision_api: str = None) -> str:
    if not vision_api:
        return "エラー: Cloud Vision APIキーが設定されていません。"
    
    encoded_image = base64.b64encode(contents).decode("utf-8")

    request_data = {
        "requests": [
            {
                "image": {"content": encoded_image},
                "features": [{"type": "TEXT_DETECTION"}]
            }
        ]
    }

    endpoint_url = f"https://vision.googleapis.com/v1/images:annotate?key={vision_api}"

    response = requests.post(endpoint_url, json=request_data)


    if response.status_code == 200:
        try:
            response_data = response.json()
            return response_data["responses"][0]["textAnnotations"][0]["description"]
        except(KeyError, IndexError):
            return "テキストが検出されませんでした"
    
    else:
        return f"エラーが発生しました:{response.status_code}"