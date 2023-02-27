import os
import json
import urllib.request
from PIL import Image

MAX_DATE_URL = "https://epaper.eenadu.net/Home/GetMaxdateJson"
ALL_PAGES_URL_TEMPLATE = "https://epaper.eenadu.net/Home/GetAllpages?editionid=3&editiondate={date}"
IMAGE_DIRECTORY = "./images"

# Retrieve the max date from the first URL
response = urllib.request.urlopen(MAX_DATE_URL).read().decode("utf-8")
max_date = response.strip('"')

# Construct the URL for fetching all the pages for the given date
all_pages_url = ALL_PAGES_URL_TEMPLATE.format(date=max_date)

# Fetch the pages data and save the XHighResolution images
response = urllib.request.urlopen(all_pages_url).read().decode("utf-8")
pages = json.loads(response)

if not os.path.exists(IMAGE_DIRECTORY):
    os.makedirs(IMAGE_DIRECTORY)

for page in pages:
    x_high_res_url = page["XHighResolution"]
    page_number = page["PageNumber"].replace(" ", "_")
    file_name = f"{page_number}.jpg"
    file_path = os.path.join(IMAGE_DIRECTORY, file_name)

    urllib.request.urlretrieve(x_high_res_url, file_path)
    print(f"Downloaded {file_name}")

    # Download the PNG image and overlay it on the JPEG image
    png_url = x_high_res_url.replace(".jpg", ".png")
    png_file_name = f"{page_number}.png"
    png_file_path = os.path.join(IMAGE_DIRECTORY, png_file_name)
    urllib.request.urlretrieve(png_url, png_file_path)

    with Image.open(file_path) as img_jpeg, Image.open(png_file_path) as img_png:
        img_jpeg = img_jpeg.convert("RGBA")
        img_png = img_png.convert("RGBA")
        img_jpeg.alpha_composite(img_png)
        result_path = os.path.join(IMAGE_DIRECTORY, f"{page_number}.png")
        img_jpeg.save(result_path)

    print(f"Overlayed and saved {result_path}")

print("All images downloaded and overlayed successfully.")
