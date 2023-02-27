import os
import json
from PIL import Image
import urllib.request
from reportlab.lib.pagesizes import portrait, landscape
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

MAX_DATE_URL = "https://epaper.eenadu.net/Home/GetMaxdateJson"
ALL_PAGES_URL_TEMPLATE = "https://epaper.eenadu.net/Home/GetAllpages?editionid=3&editiondate={date}"
IMAGE_DIRECTORY = "./images"

# Retrieve the max date and edition ID from the first URL
response = urllib.request.urlopen(MAX_DATE_URL).read().decode("utf-8")
max_date = response.strip('"')
edition_id = "Edition3"  # Replace with the actual edition ID

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
    jpeg_file_name = f"{page_number}.jpg"
    png_file_name = f"{page_number}.png"
    jpeg_file_path = os.path.join(IMAGE_DIRECTORY, jpeg_file_name)
    png_file_path = os.path.join(IMAGE_DIRECTORY, png_file_name)

    urllib.request.urlretrieve(x_high_res_url, jpeg_file_path)

    png_url = x_high_res_url.replace(".jpg", ".png")
    urllib.request.urlretrieve(png_url, png_file_path)

    print(f"Downloaded {jpeg_file_name} and {png_file_name}")

    # Load the JPEG and PNG images and overlay them
    jpeg_image = Image.open(jpeg_file_path)
    png_image = Image.open(png_file_path)
    composite_image = Image.alpha_composite(jpeg_image.convert("RGBA"), png_image.convert("RGBA"))

    # Save the overlayed image
    composite_file_name = f"{page_number}_overlay.jpg"
    composite_file_path = os.path.join(IMAGE_DIRECTORY, composite_file_name)
    composite_image.save(composite_file_path, "JPEG")

    print(f"Created overlay image {composite_file_name}")

# Create a PDF file from the images
pdf_file_name = f"Eenadu-{edition_id}-{max_date.replace('/','-')}.pdf"
pdf_file_path = os.path.join(IMAGE_DIRECTORY, pdf_file_name)

c = canvas.Canvas(pdf_file_path, pagesize=landscape(portrait((composite_image.size for composite_image in map(Image.open, sorted(os.listdir(IMAGE_DIRECTORY)))))))
for file_name in sorted(os.listdir(IMAGE_DIRECTORY)):
    if file_name.endswith(".jpg"):
        image_path = os.path.join(IMAGE_DIRECTORY, file_name)
        img = ImageReader(image_path)
        c.drawImage(img, 0, 0, *landscape(img.getSize()))
        c.showPage()
c.save()

print(f"Created PDF file {pdf_file_name}")

print("All images downloaded and overlayed successfully. PDF file created successfully.")