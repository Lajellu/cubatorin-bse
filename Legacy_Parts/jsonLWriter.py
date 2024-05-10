import os
import openai
from openai import OpenAI
import jsonlines
import json

# Ensure your OPENAI_API_KEY environment variable is set
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def write_json_lines(data):
    with open('upload-files.JSONL', 'wb') as f:
        for prompt, completion in data:
            writer.write({"prompt": prompt, "completion": completion})
