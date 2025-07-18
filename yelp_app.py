import requests
import random

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
        print(f"❌ Error: {response.status_code} - {response.text}")
        return

    data = response.json()
    businesses = data.get("businesses", [])

    if not businesses:
        print("😕 No matching restaurants found.")
        return

    # Filter by rating
    filtered = [b for b in businesses if b.get("rating", 0) >= min_rating]

    if not filtered:
        print(f"😕 No restaurants with {min_rating}★ or higher found.")
        return

    chosen = random.choice(filtered)
    name = chosen["name"]
    address = ", ".join(chosen["location"]["display_address"])
    rating = chosen["rating"]
    phone = chosen.get("display_phone", "No phone listed")
    is_closed = chosen.get("is_closed", False)
    yelp_url = chosen["url"]

    print("\n🍽️  Random Restaurant Pick 🍽️")
    print(f"📍 {name}")
    print(f"📌 Address: {address}")
    print(f"📞 Phone: {phone}")
    print(f"⭐ Rating: {rating}")
    print(f"🔗 Yelp: {yelp_url}")

    if is_closed:
        print("⚠️ Yelp reports this place is permanently closed.")
    else:
        print("✅ Yelp shows it as currently operating.")

    google_search = f"https://www.google.com/maps/search/{name.replace(' ', '+')}+{address.replace(' ', '+')}"
    print(f"📍 Google Maps Search: {google_search}")

if __name__ == "__main__":
    zip_code = input("📫 Enter ZIP code (e.g. 87107): ").strip()
    cuisine = input("🍕 Enter cuisine (e.g. sushi, mexican, bbq): ").strip().lower()
    try:
        distance = float(input("📏 Max distance in miles (max 25): "))
    except ValueError:
        distance = 15

    try:
        min_rating = float(input("⭐ Minimum rating (e.g. 4.0): "))
    except ValueError:
        min_rating = 0.0

    get_restaurants(zip_code, cuisine or "restaurants", distance, min_rating)
