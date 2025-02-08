import openai
import os

# Initialize OpenAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Chat history storage
chat_history = [{"role": "system", "content": "You are a helpful assistant."}]

# Start a loop for user input
while True:
    user_input = input("You: ")  # Ask for user input
    
    if user_input.lower() in ["exit", "quit", "bye"]:  # Exit condition
        print("Chatbot: Goodbye!")
        break

    # Append user input to chat history
    chat_history.append({"role": "user", "content": user_input})

    # Send the chat history to OpenAI
    response = client.chat.completions.create(
        model="gpt-4",
        messages=chat_history  # Send the entire chat history
    )

    # Get AI's response
    ai_response = response.choices[0].message.content
    print("Chatbot:", ai_response)

    # Append AI response to chat history
    chat_history.append({"role": "assistant", "content": ai_response})
