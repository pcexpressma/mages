
# ------------------------------------

import os
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import mimetypes

# List of products with title and link
# Example array of objects with title and link
products = [{'title': 'DELL 2412MB', 'link': 'https://acisolutions.ma/product/dell-2412-mb/'},
             {'title': 'DELL E176', 'link': 'https://acisolutions.ma/product/dell-e176/'},
               {'title': 'Dell P2314H', 'link': 'https://acisolutions.ma/product/dell-p2314h/'},
                 {'title': 'DELL P2419H', 'link': 'https://acisolutions.ma/product/dell-p2419h/'},
                   {'title': 'Dell U2415', 'link': 'https://acisolutions.ma/product/aoc-e2475pwj-copy/'},
                     {'title': 'Ecran HP E232', 'link': 'https://acisolutions.ma/product/ecran-hp-elite-display-e232/'},
                       {'title': 'Ecran HP Z23n', 'link': 'https://acisolutions.ma/product/ecran-hp-z23n/'},
                         {'title': 'HP  ELITEDISPLAY Z24n G2', 'link': 'https://acisolutions.ma/product/hp-elitedisplay-z24n-g2/'}, 
                         {'title': 'HP Compaq LE2202', 'link': 'https://acisolutions.ma/product/hp-compaq-le2202/'},
                           {'title': 'HP E23 G4', 'link': 'https://acisolutions.ma/product/11704/'},
                             {'title': 'HP E231', 'link': 'https://acisolutions.ma/product/hp-e231/'},
                               {'title': 'HP E241i', 'link': 'https://acisolutions.ma/product/hp-e241i/'},
                                 {'title': 'HP E242', 'link': 'https://acisolutions.ma/product/hp-e242/'}, 
                                 {'title': 'HP L1706', 'link': 'https://acisolutions.ma/product/hpl1706/'},
                                   {'title': 'HP L1950', 'link': 'https://acisolutions.ma/product/hp-l1950/'}, 
                                   {'title': 'HP LA2205wg', 'link': 'https://acisolutions.ma/product/hp-la2205wg/'},
                                     {'title': 'HP LA2306', 'link': 'https://acisolutions.ma/product/hp-la2306/'},
                                       {'title': 'HP Z23n G2', 'link': 'https://acisolutions.ma/product/ecran-23-full-hd-hp-z23n-g2/'}, 
                                       {'title': 'HP Z24n 24″ IPS Display', 'link': 'https://acisolutions.ma/product/11714/'},
                                         {'title': 'iiyama 17', 'link': 'https://acisolutions.ma/product/iiyama-17/'},
                                           {'title': 'iiyama 19', 'link': 'https://acisolutions.ma/product/iiyama-19/'},
                                             {'title': 'iiyama XB2380HS', 'link': 'https://acisolutions.ma/product/iiyama-xb2380hs/'},
                                               {'title': 'LCD DELL P2317H', 'link': 'https://acisolutions.ma/product/lcd-dell-p2317h/'},
             {'title': 'LCD HP E233', 'link': 'https://acisolutions.ma/product/lcd-hp-e233/'},
             {'title': 'LCD HP S2231', 'link': 'https://acisolutions.ma/product/lcd-hp-s2231/'}, {'title': 'LENOVO ThinkVision P27q', 'link': 'https://acisolutions.ma/product/lenovo-thinkvision-p27q/'}, {'title': 'Lenovo ThinkVision T24d-10', 'link': 'https://acisolutions.ma/product/lenovo-thinkvision-t24d-10/'}, {'title': 'SAMSUNG S24C650', 'link': 'https://acisolutions.ma/product/samsung-s24c650/'}]

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
