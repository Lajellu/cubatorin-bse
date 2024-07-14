# WORKS: Basic ChatGPT chatbot that responds to your questions based on general training data
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Ensure your OPENAI_API_KEY environment variable is set

# Create a chat completion request
completion = client.chat.completions.create(model="gpt-4",
messages=[
   {"role": "user", "content": "How do I perform market sizing as a new entrepreneur?"}
])

print(completion.choices[0].message.content)

