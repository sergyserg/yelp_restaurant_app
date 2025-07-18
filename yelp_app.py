import requests
import random
import streamlit as st

st.set_page_config(
    page_title="🍽️ Random Restaurant Picker",
    page_icon="🍠",
    layout="centered"
)

st.markdown("""
    <style>
        .stButton>button {
            background-color: #f63366;
            color: white;
            border-radius: 10px;
            height: 3em;
            width: 100%;
        }
    </style>
""", unsafe_allow_html=True)

API_KEY = "dKXO-AEkZkU9RjENAWLRWyMODGQQdfDtOHq4ZWLTh2oxDfMWGpjTenYDltwgoAUI7S8QpA07mDLGQs-xgXWU1NluJOKFzN6ZTS5R-c6RKLqI2helamG-A5AJffR3aHYx"

def get_restaurants(zip_code, cuisine="restaurants", radius_miles=15, min_rating=0.0):
    RADIUS_METERS = min(int(radius_miles * 1609.34), 40000)

    url = "https://api.yelp.com/v3/businesses/search"
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    params = {
        "term": cuisine,
        "location": zip_code,
        "limit": 50,
        "radius": RADIUS_METERS,
        "sort_by": "best_match"
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        st.error(f"Error: {response.status_code} - {response.text}")
        return None

    data = response.json()
    businesses = data.get("businesses", [])
    filtered = [b for b in businesses if b.get("rating", 0) >= min_rating and not b.get("is_closed", False)]

    return filtered if filtered else None

# Streamlit UI
st.title(":sushi: Random Restaurant Picker")
st.caption("Powered by Yelp Fusion API")

zip_code = st.text_input("\ud83d\udce7 Enter ZIP code", value="87107")
cuisine = st.text_input("\ud83c\udf55 Preferred cuisine (e.g. sushi, mexican)", value="restaurants")
distance = st.slider("\ud83d\udccd Max distance (miles)", 1, 25, 15)
rating = st.slider("\u2b50 Minimum Yelp rating", 1.0, 5.0, 4.0, step=0.1)

if st.button("\ud83c\udf72 Pick a Place"):
    result_list = get_restaurants(zip_code, cuisine, distance, rating)
    if result_list:
        result = random.choice(result_list)
        name = result['name']
        address = ", ".join(result['location']['display_address'])
        phone = result.get('display_phone', 'No phone')
        rating = result['rating']
        url = result['url']
        google_url = f"https://www.google.com/maps/search/{name.replace(' ', '+')}+{address.replace(' ', '+')}"

        st.success(f"\ud83c\udf1f {name}")
        st.write(f"\ud83d\udccd {address}")
        st.write(f"\ud83d\udcf1 {phone}")
        st.write(f"\u2b50 Rating: {rating}")
        st.markdown(f"[View on Yelp]({url}) | [Google Maps]({google_url})")

        if st.button("\ud83d\udd04 Pick Again"):
            st.rerun()
    else:
        st.warning("No matching restaurants found.")
