from flask import Flask, request, jsonify, session
from flask_cors import CORS
import openai
import os
import uuid
import datetime  # Importing datetime in the correct place

app = Flask(__name__)
CORS(app)

# Use secret key for session management
app.secret_key = os.getenv("FLASK_SECRET_KEY", "default-secret-key")  # Change this in production!

# Initialize OpenAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Store chat history per user session
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    # Generate a unique user ID if it doesn't exist
    if "user_id" not in session:
        session["user_id"] = str(uuid.uuid4())

    # Store chat history per user
    if "chat_history" not in session:
        session["chat_history"] = [{"role": "system", "content": "You are a helpful assistant."}]

    # Append user input to session chat history
    session["chat_history"].append({"role": "user", "content": user_message})

    # Generate AI response
    response = client.chat.completions.create(
        model="gpt-4",
        messages=session["chat_history"]
    )

    ai_response = response.choices[0].message.content
    session["chat_history"].append({"role": "assistant", "content": ai_response})

    # Log the chat
    log_chat(session["user_id"], user_message, ai_response)

    return jsonify({"response": ai_response})


def log_chat(user_id, user_message, ai_response):
    """Logs chat messages to a file with timestamps."""
    with open("chat_logs.txt", "a", encoding="utf-8") as log_file:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"[{timestamp}] User ({user_id}): {user_message}\n")
        log_file.write(f"[{timestamp}] Bot: {ai_response}\n\n")


if __name__ == "__main__":
    app.run(debug=True)
