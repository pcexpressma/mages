
# ------------------------------------

import os
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import mimetypes

# List of products with title and link
# Example array of objects with title and link
products = [{'title': 'DELL Latitude 5290 2-in-1', 'link': 'https://acisolutions.ma/product/dell-latitude-5290-2-in-1/'}, {'title': 'DELL LATITUDE 7400', 'link': 'https://acisolutions.ma/product/dell-latitude-7400/'}, {'title': 'DELL LATITUDE 7490', 'link': 'https://acisolutions.ma/product/10794/'}, {'title': 'Dell Latitude Rugged 7414', 'link': 'https://acisolutions.ma/product/dell-latitude-rugged-7414/'}, {'title': 'DELL PRECISSION 5530', 'link': 'https://acisolutions.ma/product/dell-precission-5530/'}, {'title': 'Hp EliteBook 830 G5 TACTILE', 'link': 'https://acisolutions.ma/product/hp-elitebook-830-g5-14%e2%80%b3-i7-16gb-256-ssd-8th-generation-touch/'}, {'title': 'Hp EliteBook 830 G6', 'link': 'https://acisolutions.ma/product/hp-elitebook-830-g6/'}, {'title': 'HP EliteBook 840 G4 Core i5 7ème Génération', 'link': 'https://acisolutions.ma/product/hp-elitebook-840-g4-core-i5-7eme-generation/'}, {'title': 'Hp EliteBook 840 G5', 'link': 'https://acisolutions.ma/product/hp-elitebook-840-g4-core-i7-7eme-generation-copy/'}, {'title': 'HP ELITEBOOK 840 G5', 'link': 'https://acisolutions.ma/product/h/'}, {'title': 'HP EliteBook 850 G3', 'link': 'https://acisolutions.ma/product/hp-elitebook-840-g3-core-i5-6eme-generation/'}, {'title': 'HP PROBOOK 640 G5', 'link': 'https://acisolutions.ma/product/hp-probook-640-g5/'}, {'title': 'LENOVO thinkpad 11e', 'link': 'https://acisolutions.ma/product/lenovo-thinkpad-11e/'}, {'title': 'LENOVO thinkpad 260', 'link': 'https://acisolutions.ma/product/lenovo-thinkpad-260/'}, {'title': 'Lenovo ThinkPad L380 YOGA', 'link': 'https://acisolutions.ma/product/lenovo-thinkpad-l380-yoga/'}, {'title': 'LENOVO thinkpad x380 yoga', 'link': 'https://acisolutions.ma/product/lenovo-x380-yoga-tactile-et-convertible-core-i5-8eme-generation-8go-ram-256go-ssd/'}, {'title': 'lenovo thinkpad x390', 'link': 'https://acisolutions.ma/product/lenovo-thinkpad-x390/'}, {'title': 'Lenovo ThinkPad X390', 'link': 'https://acisolutions.ma/product/lenovo-thinkpad-x390-2/'}, {'title': 'Lenovo ThinkPad X390 Yoga', 'link': 'https://acisolutions.ma/product/lenovo-thinkpad-x390-yoga/'}, {'title': 'Lenovo ThinkPad Yoga 370', 'link': 'https://acisolutions.ma/product/lenovo-thinkpad-yoga-370/'}, {'title': 'Lenovo ThinkPad YOGA L390', 'link': 'https://acisolutions.ma/product/lenovo-thinkpad-yoga-l390/'}, {'title': 'Microsoft Surface Laptop 3', 'link': 'https://acisolutions.ma/product/microsoft-surface-laptop-3/'}]
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
