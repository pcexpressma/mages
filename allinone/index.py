
# ------------------------------------

import os
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import mimetypes

# List of products with title and link
# Example array of objects with title and link
products = [{'title': 'Dell OptiPlex 3011 All In One', 'link': 'https://acisolutions.ma/product/dell-optiplex-3011-all-in-one/'}, {'title': 'DELL OptiPlex 9030 ALL IN ONE', 'link': 'https://acisolutions.ma/product/dell-optiplex-9030-all-in-one/'}, {'title': 'HP 3420 Pro All-in-One', 'link': 'https://acisolutions.ma/product/hp-3420-pro-all-in-one/'}, {'title': 'HP Compaq Pro 6300 All-In-One', 'link': 'https://acisolutions.ma/product/hp-compaq-pro-6300-all-in-one/'}, {'title': 'HP ELITEONE 600 G2 ALL IN ONE', 'link': 'https://acisolutions.ma/product/11653/'}, {'title': 'HP EliteOne 800 G2 ALL IN ONE', 'link': 'https://acisolutions.ma/product/hp-eliteone-800-g2-all-in-one/'}, {'title': 'HP EliteOne 800 G2 all in one Core i3 6100', 'link': 'https://acisolutions.ma/product/hp-eliteone-800-g2-all-in-one-core-i3-6100/'}, {'title': 'HP EliteOne 800 G3 I5-7600 All in One', 'link': 'https://acisolutions.ma/product/hp-eliteone-800-g3-i5-7600-all-in-one/'}, {'title': 'HP EliteOne 800 G3 I7-7700 All in One', 'link': 'https://acisolutions.ma/product/hp-eliteone-800-g3-all-in-one-desktop-computer/'}, {'title': 'HP EliteOne 800 G4, All-In-One', 'link': 'https://acisolutions.ma/product/hp-eliteone-800-g4-all-in-one/'}, {'title': 'HP EliteOne 800 G5 All-in-One Computer', 'link': 'https://acisolutions.ma/product/hp-eliteone-800-g5-all-in-one-computer/'}, {'title': 'HP EliteOne 800 G5 I5-7600 All in One', 'link': 'https://acisolutions.ma/product/11688/'}, {'title': 'HP ProOne 400 G1 All in One', 'link': 'https://acisolutions.ma/product/hp-proone-400-g1-all-in-one/'}, {'title': 'HP ProOne 440 G6 ALL IN ONE', 'link': 'https://acisolutions.ma/product/11668/'}, {'title': 'HP TouchSmart Elite 7320  All in One', 'link': 'https://acisolutions.ma/product/hp-touchsmart-elite-7320-all-in-one/'}]

# Function to process a single product
def process_product(product):
    title = product['title']
    url = product['link']

    # Send a request to fetch the page content
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the page content with BeautifulSoup
        soup = BeautifulSoup(response.content, 'lxml')

        # Sanitize the folder name by replacing spaces with hyphens
        folder_name = title.replace(' ', '-')
        
        # Create a folder with the sanitized title
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        # Extract all images from the slider with class 'product-image-thumbnail'
        image_elements = soup.find_all('div', class_='product-image-thumbnail')
        image_urls = []

        for img in image_elements:
            img_tag = img.find('img')
            if img_tag and 'srcset' in img_tag.attrs:
                # Get the last URL in the srcset attribute
                srcset = img_tag['srcset']
                last_url = srcset.split(',')[-1].split()[0]
                image_urls.append(last_url)

        # Download, resize, and save each image into the created folder
        for idx, img_url in enumerate(image_urls):
            # Get the image content
            img_response = requests.get(img_url)
            if img_response.status_code == 200:
                # Open the image
                img = Image.open(BytesIO(img_response.content))
                # Resize the image
                img = img.resize((550, 500))
                # Determine the image format from the response headers or URL
                content_type = img_response.headers.get('content-type')
                extension = mimetypes.guess_extension(content_type)
                if extension is None:
                    extension = os.path.splitext(img_url)[1]  # Fallback to URL extension

                # Handle image format conversion for JPEG
                if extension.lower() == '.jpeg' or extension.lower() == '.jpg':
                    if img.mode == 'RGBA':
                        img = img.convert('RGB')

                # Save the image in the folder with a unique name and original format
                img_path = os.path.join(folder_name, f'image_{idx + 1}{extension}')
                img.save(img_path)

        # Print the extracted information
        print(f"Processed {title}: Images saved in folder '{folder_name}'")
    else:
        print(f"Failed to retrieve the page for {title}. Status code: {response.status_code}")

# Process each product
for product in products:
    process_product(product)
