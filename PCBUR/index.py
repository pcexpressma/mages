
# ------------------------------------

import os
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import mimetypes

# List of products with title and link
# Example array of objects with title and link
products = [{'title': 'DELL Optiplex 7020 SFF', 'link': 'https://acisolutions.ma/product/dell-optiplex-7020-sff/'}, {'title': 'DELL Optiplex 7040 MINI', 'link': 'https://acisolutions.ma/product/dell-optiplex-7040-mini/'}, {'title': 'Dell OptiPlex 7040 SFF I5 7050', 'link': 'https://acisolutions.ma/product/dell-optiplex-7040-sff-i5-7050/'}, {'title': 'Dell OptiPlex 7040 SFF i7-6700', 'link': 'https://acisolutions.ma/product/dell-optiplex-7040-sff-i7-6700/'}, {'title': 'DELL OPTIPLEX 7050 SFF', 'link': 'https://acisolutions.ma/product/dell-optiplex-7050-sff/'}, {'title': 'Dell Optiplex 9020 Mini-Tower', 'link': 'https://acisolutions.ma/product/dell-optiplex-9020-mini-tower/'}, {'title': 'Dell OptiPlex 9020 SFF', 'link': 'https://acisolutions.ma/product/dell-optiplex-9020-sff/'}, {'title': 'HP 600 G2 SFF', 'link': 'https://acisolutions.ma/product/hp-prodesk-600-g2-sff-core-i5-6eme-gen-8go-ddr4-256gb-ssd-win-10-pro/'}, {'title': 'HP 6000 SFF', 'link': 'https://acisolutions.ma/product/hp-6000-sff/'}, {'title': 'HP 6200 SFF', 'link': 'https://acisolutions.ma/product/hp-6200-sff/'}, {'title': 'HP 6300 SFF', 'link': 'https://acisolutions.ma/product/hp-6300-sff/'}, {'title': 'HP 800 G1 SFF', 'link': 'https://acisolutions.ma/product/hp-800-g1-sff/'}, {'title': 'HP 800 G3 SFF', 'link': 'https://acisolutions.ma/product/hp-elitedesk-800-g3-sff-intel-core-i5-6500-ram-8-go/'}, {'title': 'HP Elitedesk 705 G4 MINI', 'link': 'https://acisolutions.ma/product/hp-elitedesk-705-g4-mini/'}, {'title': 'HP Elitedesk 800 G1 TOWER Core i5-4590', 'link': 'https://acisolutions.ma/product/hp-elitedesk-800-g1-tower-core-i5-4590/'}, {'title': 'HP Elitedesk 800 G1 TOWER Core i7-4590', 'link': 'https://acisolutions.ma/product/hp-elitedesk-800-g1-core-i5-4590/'}, {'title': 'HP EliteDesk 800 G2', 'link': 'https://acisolutions.ma/product/hp-elitedesk-800-g2/'}, {'title': 'HP Elitedesk 800 g2 mini', 'link': 'https://acisolutions.ma/product/hp-elitedesk-800-g2-mini/'}, {'title': 'HP elitedesk 800 G4 mini', 'link': 'https://acisolutions.ma/product/hp-elitedesk-800-g4-mini/'}, {'title': 'HP EliteDesk 800 G5', 'link': 'https://acisolutions.ma/product/hp-elitedesk-800-g5/'}, {'title': 'HP ProDesk 400 G3 SFF', 'link': 'https://acisolutions.ma/product/hp-prodesk-400-g3-sff/'}, {'title': 'HP prodesk 400 G4 sff', 'link': 'https://acisolutions.ma/product/hp-prodesk-400-g4-sff/'}, {'title': 'HP ProDesk 400 G5 Desktop Mini', 'link': 'https://acisolutions.ma/product/hp-prodesk-400-g5-desktop-mini/'}, {'title': 'Lenovo ThinkCentre M630e MINI', 'link': 'https://acisolutions.ma/product/11841/'}, {'title': 'Lenovo ThinkCentre M700 MINI', 'link': 'https://acisolutions.ma/product/lenovo-thinkcentre-m700-mini/'}, {'title': 'Lenovo ThinkCentre M710q MINI', 'link': 'https://acisolutions.ma/product/lenovo-thinkcentre-m710q-mini/'}, {'title': 'Lenovo ThinkCentre M715q MINI', 'link': 'https://acisolutions.ma/product/lenovo-thinkcentre-m715q-mini/'}, {'title': 'Lenovo ThinkCentre M720q MINI', 'link': 'https://acisolutions.ma/product/lenovo-thinkcentre-m720q-mini/'}, {'title': 'LENOVO thinkcentre M72e', 'link': 'https://acisolutions.ma/product/lenovo-thinkcentre-m72e/'}, {'title': 'LENOVO thinkcentre M72e', 'link': 'https://acisolutions.ma/product/lenovo-thinkcentre-m72e-2/'}, {'title': 'Lenovo ThinkCentre M83 Mini', 'link': 'https://acisolutions.ma/product/lenovo-thinkcentre-m83-mini/'}, {'title': 'Lenovo ThinkCentre M900 MINI', 'link': 'https://acisolutions.ma/product/lenovo-thinkcentre-m900-mini/'}, {'title': 'LENOVO THINKCENTRE M910T TOWER', 'link': 'https://acisolutions.ma/product/lenovo-thinkcentre-m910t-tower/'}]
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
