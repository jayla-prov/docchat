"""Send one example message to the model and print its reply."""
from chat import llm

reply = llm([
    {'role': 'system', 'content': 'You are a helpful assistant.'},
    {'role': 'user', 'content': 'What is the capital of France?'},
], temperature=0)
print(reply)