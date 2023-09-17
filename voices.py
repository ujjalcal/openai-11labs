import requests


from config import  ELEVENLABS_API_KEY

# Set API keys



url = "https://api.elevenlabs.io/v1/voices"

headers = {
  "Accept": "application/json",
  "xi-api-key": ELEVENLABS_API_KEY
}

response = requests.get(url, headers=headers)

print(response.text)

# pretty_json = json.dumps(response.json(), indent=4)
# print(pretty_json)
