from openai import OpenAI
import json
import re

def extract_structure_data_from_text(
        ocr_text: dict, 
        openai_api: str = None
    ) -> dict:

    if not openai_api:
        return {"error": f"OpenAI APIキーが設定されていません"}
    
    prompt = f"""
        次の複数の書類のOCR結果をもとに、1件の車の登録に関する統合データをJSON形式で出力してください。
        #新所有者印鑑証明
        {ocr_text.get("new_owner_inkan", "")}
        ・「氏名」「住所」をそれぞれ抽出して、JSON形式で出力してください。  
        ・企業の場合は商号を取得してください。
        ・姓と名、または会社形態と会社名、会社名と会社形態の間は1文字空けてください。(例: 田中　太郎)  
        ・建物名（例：「○○マンション」「○○アパート」など）は削除してください。ただし、部屋番号（例：「201」「1104号室」など）は残し、数字のみ番地に結合してください。
        ・住所に含まれる「字」、それ以降の細かい町名・地名は削除し、数字が始まるまでの主要な地名を残してください（例: “今沢町”は残す）。
        ・丁目（◯丁目）の記載がある場合は、アラビア数字で抽出してください。◯丁目が存在しない場合は、address_street は空文字（""）にしてください。
        ・住所の番地は数字のみにしてください。例:18番地10 → 18-10
        ・以下のjsonフォーマットにしてください：
        {{
            "new_owner_name": "田中　太郎", 
            "new_owner_address_main": "兵庫県姫路市香寺町岩部", 
            "new_owner_address_street": "1", 
            "new_owner_address_number": "96-1-301"
        }}
    """

    try:
        client = OpenAI(api_key=openai_api)
        response = client.chat.completions.create(
            model = "gpt-4o",
            messages=[{"role": "user", "content":prompt}]
        )
        content = response.choices[0].message.content
        return extract_json_from_response(content)
    except Exception as err:
        return {"error": f"OpenAI APIエラー: {str(err)}. APIキーを確認してください"}
    
    
def extract_json_from_response(content: str) -> dict:
    match = re.search(r"\{.*\}", content, re.DOTALL)
    if match:
        return json.loads(match.group())
    else:
        return {"error": "JSON not found in response"}