import requests
from PIL import Image, ImageFilter

# NSFW detector API endpoint and API key
API_ENDPOINT = "https://api.deepai.org/api/nsfw-detector"
API_KEY = "quickstart-QUdJIGlzIGNvbWluZy4uLi4K"

# Image file path
image_path = 'image.jpg'

# Call NSFW detector API to get NSFW parts of the image
r = requests.post(
    API_ENDPOINT,
    files={'image': open(image_path, 'rb')},
    headers={'api-key': API_KEY}
)
nsfw_data = r.json()['output']

# Load the image as a PIL Image object
image = Image.open(image_path)

# Blur the NSFW parts of the image using the bounding box coordinates
for detection in nsfw_data['detections']:
    bbox = detection['bounding_box']
    # Convert bounding box pixel coordinates to percentages of image size
    width, height = image.size
    bbox = [
        bbox[0] / width, 
        bbox[1] / height, 
        (bbox[0] + bbox[2]) / width, 
        (bbox[1] + bbox[3]) / height
    ]
    # Convert percentages of image size to pixel coordinates
    bbox = [coord * size for coord, size in zip(bbox, image.size)]
    # Crop the NSFW part of the image using the bounding box
    nsfw_part = image.crop(bbox)
    # Blur the cropped NSFW part of the image
    blurred_nsfw_part = nsfw_part.filter(ImageFilter.GaussianBlur(radius=10))
    # Paste the blurred NSFW part back into the original image
    image.paste(blurred_nsfw_part, bbox)

# Save the blurred image
blurred_image_path = 'blurred_file.jpg'
image.save(blurred_image_path)
