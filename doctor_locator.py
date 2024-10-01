import requests
import folium
from folium.plugins import MarkerCluster, Fullscreen, MiniMap
import streamlit as st
import os

# Replace with your actual API key
api_key = ""

@st.cache_data(show_spinner=False)
def geocode_address(address, api_key):
    """Geocode the given address to get latitude and longitude."""
    geocode_url = f"https://geocode.search.hereapi.com/v1/geocode"
    geocode_params = {"q": address, "apiKey": api_key}
    geocode_response = requests.get(geocode_url, params=geocode_params)

    if geocode_response.status_code == 200:
        geocode_data = geocode_response.json()
        if geocode_data.get('items'):
            location = geocode_data['items'][0]['position']
            return location['lat'], location['lng']
        else:
            st.error("No results found for the provided address.")
            return None, None
    else:
        st.error(f"Geocoding Error: {geocode_response.status_code} - {geocode_response.text}")
        return None, None

@st.cache_data(show_spinner=False)
def find_doctors_nearby(latitude, longitude, api_key, limit=20):
    """Find doctors near the given latitude and longitude."""
    discover_url = f"https://discover.search.hereapi.com/v1/discover"
    discover_params = {
        "at": f"{latitude},{longitude}",
        "q": "Doctors",
        "limit": limit,
        "apiKey": api_key
    }

    discover_response = requests.get(discover_url, params=discover_params)

    if discover_response.status_code == 200:
        return discover_response.json().get('items', [])
    else:
        st.error(f"Discover Error: {discover_response.status_code} - {discover_response.text}")
        return []

@st.cache_data(show_spinner=False)
def geocode_doctors(doctors, api_key):
    """Geocode the addresses of doctors to get their latitude and longitude."""
    geocoded_doctors = []
    for doctor in doctors:
        name = doctor.get('title')
        address = doctor.get('address', {}).get('label')
        latitude, longitude = geocode_address(address, api_key)
        if latitude and longitude:
            geocoded_doctors.append({
                'name': name,
                'address': address,
                'latitude': latitude,
                'longitude': longitude
            })
    return geocoded_doctors

def create_map(latitude, longitude, geocoded_doctors, file_path="map.html"):
    """Create a Folium map with markers for each geocoded doctor and save as an HTML file."""
    m = folium.Map(location=[latitude, longitude], zoom_start=15, tiles='OpenStreetMap')

    minimap = MiniMap(toggle_display=True)
    m.add_child(minimap)

    Fullscreen().add_to(m)

    marker_cluster = MarkerCluster().add_to(m)

    for doctor in geocoded_doctors:
        popup_content = folium.Html(
            f"<b>{doctor['name']}</b><br>{doctor['address']}", script=True
        )
        popup = folium.Popup(popup_content, max_width=300)
        folium.Marker(
            location=[doctor['latitude'], doctor['longitude']],
            popup=popup,
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(marker_cluster)

    # Save the map to an HTML file
    m.save(file_path)
    return file_path

def doctor_locator():
    st.title("Doctor Locator")

    address = st.text_input("Enter your location:", "Baner, Pune")
    
    if 'map_html_path' not in st.session_state:
        st.session_state.map_html_path = None

    if st.button("Find Doctors"):
        latitude, longitude = geocode_address(address, api_key)
        if latitude and longitude:
            doctors = find_doctors_nearby(latitude, longitude, api_key)
            if doctors:
                geocoded_doctors = geocode_doctors(doctors, api_key)
                # Save the map as an HTML file
                st.session_state.map_html_path = create_map(latitude, longitude, geocoded_doctors)
            else:
                st.warning("No doctors found near the location.")
                st.session_state.map_html_path = None
        else:
            st.error("Could not geocode the address. Please try again.")
            st.session_state.map_html_path = None

    if st.session_state.map_html_path:
        # Read the saved HTML file and display it
        with open(st.session_state.map_html_path, "r") as f:
            map_html = f.read()
        st.components.v1.html(map_html, width=700, height=700)

if __name__ == "__main__":
    doctor_locator()
