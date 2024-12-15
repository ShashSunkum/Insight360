from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app)

client = OpenAI(
    base_url="https://api-inference.huggingface.co/v1/",
    api_key="YOUR_API_KEY"  # Replace with your HF API key
)

@app.route('/chat', methods=['POST'])
def chatbot():
    data = request.get_json()
    user_input = data.get('question', '')

    if not user_input.strip():
        return jsonify({"error": "No question provided"}), 400

    # Add a system message that sets the prompt style
    messages = [
        {
            "role": "system",
            "content": (
                "You are an expert soccer manager AI. When the user asks which players to buy or asks "
                "for recommendations, you must only provide the names of exactly 3 players each time. "
                "If the user asks for something else, still respond as a knowledgeable soccer manager. "
                "Do not exceed 3 player names in any recommendation."
            )
        },
        {
            "role": "user",
            "content": user_input
        }
    ]

    try:
        completion = client.chat.completions.create(
            model="mistralai/Mistral-7B-Instruct-v0.3",
            messages=messages,
            max_tokens=500
        )
        answer = completion.choices[0].message.content
        return jsonify({"answer": answer})
    except Exception as e:
        print("Error:", e)
        return jsonify({"answer": "I'm sorry, I couldn't process your request at this time."}), 500

if __name__ == '__main__':
    app.run(debug=True)
