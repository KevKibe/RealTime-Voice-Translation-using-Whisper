import requests

# Define the API endpoint
api_url = 'http://127.0.0.1:5000/translate'  # Change the URL if your API is running on a different host or port

# Sample data for translation
data = {
    'text': 'Hello, world!',
    'target_language': 'fr'
}

# Send a POST request to the API
response = requests.post(api_url, json=data)

if response.status_code == 200:
    # Print the response JSON
    print('Response JSON:')
    print(response.json())
else:
    # Print an error message if the request was not successful
    print(f'Error: {response.status_code}, {response.text}')
