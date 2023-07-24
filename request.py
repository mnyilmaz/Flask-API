import requests

# Replace 'your_message' with the actual message you want to send to the chatbot
msg = "Bye"

# Set the headers to specify that the data is in JSON format
headers = {
    'Content-Type': 'application/json'
}

# Create a dictionary with the 'message' key and the message as the value
data = {
    'msg': msg
}

# Send the POST request with the correct Content-Type header
response = requests.post('http://localhost:5000/api/chatbot', headers=headers, json=data)

# Print the response from the server
print(f"User: {msg}")
print(response.json())

#curl -X POST -H "Content-Type: application/json" -d '{"message": "Hello"}' http://127.0.0.1:5000/api/chatbot
