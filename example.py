import requests
r = requests.post(
    "https://api.deepai.org/api/nsfw-detector",
    data={
        #'image': 'YOUR_IMAGE_URL',
      'image': open('/path/to/your/file.jpg', 'rb'),
    },
    headers={'api-key': 'quickstart-QUdJIGlzIGNvbWluZy4uLi4K'}
)
print(r.json())