
payload = {
    "contents": [
        {
            "role": "user",
            "parts": [
                {"text": "Explain how AI works"}
            ]
        }
    ]
}

headers = {
    "Content-Type": "application/json"
}

import json


test_response = requests.post(
    url=f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}",
    headers=headers,
    data=json.dumps(payload)
)
test_response.json()
[
test_response.json()['candidates'][0]['content']['parts'][0]['text']