import streamlit as st
import flickrapi
import requests

FLICKR_PUBLIC = st.secrets["flickr"]["api_key"]
FLICKR_SECRET = st.secrets["flickr"]["api_secret"]
flickr = flickrapi.FlickrAPI(FLICKR_PUBLIC, FLICKR_SECRET, format='parsed-json')

def fetch_flickr_images(search_term):
    photos = flickr.photos.search(text=search_term, per_page=5, media='photos')
    urls = []
    for photo in photos['photos']['photo']:
        url = f"https://live.staticflickr.com/{photo['server']}/{photo['id']}_{photo['secret']}_w.jpg"
        urls.append(url)
    return urls

def fetch_wikimedia_images(search_term):
    SEARCH_URL = "https://commons.wikimedia.org/w/api.php"
    params = {
        'action': 'query',
        'format': 'json',
        'generator': 'search',
        'gsrnamespace': 6,
        'gsrsearch': search_term,
        'gsrlimit': 5,
        'prop': 'imageinfo',
        'iiprop': 'url',
        'iiurlwidth': 200,
    }
    response = requests.get(SEARCH_URL, params=params).json()
    images = []
    if 'query' in response:
        for page_id in response['query']['pages']:
            image_info = response['query']['pages'][page_id]['imageinfo'][0]
            images.append(image_info['url'])
    return images

st.title("Image Search App")
search_term = st.text_input("Enter a search term:")

if search_term:
    flickr_images = fetch_flickr_images(search_term)
    wikimedia_images = fetch_wikimedia_images(search_term)
    
    if flickr_images:
        st.subheader("Flickr Images:")
        for image_url in flickr_images:
            st.image(image_url, use_column_width=True)
    else:
        st.write("No Flickr images found.")
        
    if wikimedia_images:
        st.subheader("Wikimedia Commons Images:")
        for image_url in wikimedia_images:
            st.image(image_url, use_column_width=True)
    else:
        st.write("No Wikimedia Commons images found.")
else:
    st.write("Please enter a search term.")
