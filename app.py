from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.get_json(force=True)

        image_b64 = data.get("image")
        prompt = data.get("user_prompt", "What is in this image?")

        print("🧠 Prompt received:", prompt[:60])
        print("🖼️ Image Base64 size:", len(image_b64) if image_b64 else "None")

        # Safety check
        if not image_b64:
            raise ValueError("Missing image data")

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

        reply = response.choices[0].message.content
        print("✅ GPT-4o replied:", reply[:60])
        return jsonify({"reply": reply})

    except Exception as e:
        print("💥 ERROR:", str(e))
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
