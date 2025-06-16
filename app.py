from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.json
        image_b64 = data["image"]
        prompt = data.get("user_prompt", "Describe this image.")

        print("Prompt received:", prompt[:50])
        print("Image string length:", len(image_b64))

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
    
    except Exception as e:
        print("💥 Error occurred:", str(e))
        return jsonify({"error": str(e)}), 500


# ✅ Server startup (outside the route)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
