from chatbot.gemini_client import generate_response

response = generate_response(
    "What is data analysis? Explain in one sentence."
)

print(response)