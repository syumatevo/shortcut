from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    image_b64 = data["image"]
    prompt = data.get("user_prompt", "Answer to the questions.")

    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64," + image_b64}}
            ],
        }
    ]

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )

    return jsonify({"reply": response.choices[0].message.content})
