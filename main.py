import requests
from PIL import Image, ImageFilter

# NSFW detector API endpoint and API key
API_ENDPOINT = "https://api.deepai.org/api/nsfw-detector"
API_KEY = "quickstart-QUdJIGlzIGNvbWluZy4uLi4K"

# Image file path
image_path = 'image.jpg'

# Load the image as a PIL Image object
image = Image.open(image_path)

# Resize the image if necessary (maximum size of 512 pixels)
max_size = 512
if max(image.size) > max_size:
    image.thumbnail((max_size, max_size), Image.LANCZOS)

# Call NSFW detector API to get NSFW parts of the image
r = requests.post(
    API_ENDPOINT,
    files={'image': image.tobytes()},
    headers={'api-key': API_KEY}
)

# Check if the API request was successful
if r.status_code != 200:
    print("Error: API request failed with status code", r.status_code)
else:
    # Parse the API response
    response_data = r.json()
    if 'output' not in response_data:
        print("Error: 'output' key not found in API response")
    else:
        nsfw_data = response_data['output']
        # Blur the NSFW parts of the image using the bounding box coordinates
        for detection in nsfw_data['detections']:
            bbox = detection['bounding_box']
            # Scale the bounding box coordinates if necessary
            if max(image.size) > max_size:
                scale_factor = max(image.size) / max_size
                bbox = [coord * scale_factor for coord in bbox]
            # Convert bounding box pixel coordinates to integer values
            bbox = [int(coord) for coord in bbox]
            # Crop the NSFW part of the image using the bounding box
            nsfw_part = image.crop(bbox)
            # Blur the cropped NSFW part of the image
            blurred_nsfw_part = nsfw_part.filter(ImageFilter.GaussianBlur(radius=10))
            # Paste the blurred NSFW part back into the original image
            image.paste(blurred_nsfw_part, bbox)

        # Save the blurred image
        blurred_image_path = 'blurred_file.jpg'
        image.save(blurred_image_path)
