import streamlit as st
import flickrapi
import requests
from PIL import Image
from io import BytesIO

FLICKR_PUBLIC = st.secrets["flickr"]["api_key"]
FLICKR_SECRET = st.secrets["flickr"]["api_secret"]
flickr = flickrapi.FlickrAPI(FLICKR_PUBLIC, FLICKR_SECRET, format='parsed-json')

def resize_image(image_data, width, height):
    img = Image.open(BytesIO(image_data))
    # Correct usage of the resampling filter
    img_resized = img.resize((width, height), Image.Resampling.LANCZOS)
    return img_resized

def fetch_flickr_images(search_term, width, height):
    photos = flickr.photos.search(text=search_term, per_page=50, media='photos')
    images = []
    for photo in photos['photos']['photo']:
        url = f"https://live.staticflickr.com/{photo['server']}/{photo['id']}_{photo['secret']}_w.jpg"
        response = requests.get(url)
        img_resized = resize_image(response.content, width, height)
        images.append(img_resized)
    return images

def fetch_wikimedia_images(search_term, width, height):
    SEARCH_URL = "https://commons.wikimedia.org/w/api.php"
    params = {
        'action': 'query',
        'format': 'json',
        'generator': 'search',
        'gsrnamespace': 6,
        'gsrsearch': search_term,
        'gsrlimit': 50,
        'prop': 'imageinfo',
        'iiprop': 'url',
        'iiurlwidth': width,
    }
    response = requests.get(SEARCH_URL, params=params).json()
    images = []
    if 'query' in response:
        for page_id in response['query']['pages']:
            image_info = response['query']['pages'][page_id]['imageinfo'][0]
            url = image_info['url']
            response = requests.get(url)
            img_resized = resize_image(response.content, width, height)
            images.append(img_resized)
    return images

st.title("Image Search App")

width = st.sidebar.number_input("Width", min_value=50, max_value=1000, value=300)
height = st.sidebar.number_input("Height", min_value=50, max_value=1000, value=300)

search_term = st.text_input("Enter a search term:")

if search_term:
    flickr_images = fetch_flickr_images(search_term, width, height)
    wikimedia_images = fetch_wikimedia_images(search_term, width, height)
    
    if flickr_images:
        st.subheader("Flickr Images:")
        for img in flickr_images:
            st.image(img, use_column_width=True)
            
    if wikimedia_images:
        st.subheader("Wikimedia Commons Images:")
        for img in wikimedia_images:
            st.image(img, use_column_width=True)
