# TODO: ChatGPT chatbot that responds to your questions based on Expert Knowledge uploaded data
# TODO: Train using jsonl as dataset


write_json_lines(data)

"""
# Use the actual file ID for fine-tuning
# Replace 'outcubatorModel' with a valid model name, e.g., 'gpt-3.5-turbo' for fine-tuning
fine_tune_response = openai.FineTune.create(
  training_file=file.id,
  model='gpt-3.5-turbo',  # Specify the correct base model for fine-tuning
  n_epochs=1  # Adjust the number of epochs as needed
)


print(fine_tune_response)
print(response["id"])
file_id = response["id"]  # Capture the uploaded file ID from the response


# Assuming you've captured the fine-tune job ID from fine_tune_response
fine_tune_job_id = fine_tune_response["id"]
status = openai.FineTune.retrieve(id=fine_tune_job_id)
print(status)

# Create a chat completion request
completion = client.chat.completions.create(model="gpt-4",
messages=[
    {"role": "user", "content": "How do I perform market sizing as a new entrepreneur?"}
])

print(completion.choices[0].message.content)

completion = openai.Completion.create(
  model='outcubatorModel',
  prompt='Your prompt here',
  max_tokens=50
)

print(completion.choices[0].text)
"""