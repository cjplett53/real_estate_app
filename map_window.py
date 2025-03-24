# map_window.py
import customtkinter as ctk
import tkintermapview
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

def map_window(parent, lat=None, lon=None):
    """
    Opens a Toplevel window with an interactive map.
    """
    win = ctk.CTkToplevel(parent)
    win.title("Map - Toronto")
    win.geometry("1200x800")

    # In front
    win.transient(parent)
    win.grab_set()
    win.lift(parent)
    win.focus_force()

    map_widget = tkintermapview.TkinterMapView(
        win,
        width=1200,
        height=800,
        corner_radius=0
    )
    map_widget.pack(fill="both", expand=True)

    map_widget.set_tile_server("https://cartodb-basemaps-a.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png")

    if lat is not None and lon is not None:
        map_widget.set_position(lat, lon)
        map_widget.set_zoom(15)
    else:
        map_widget.set_position(43.6532, -79.3832)
        map_widget.set_zoom(15)

    geolocator = Nominatim(user_agent="homeez_map_app")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

    # We are just displaying 3 sample addresses
    properties = [
        ("100 Queen St W, Toronto, ON, Canada", "City Hall - Test"),
        ("1 Yonge Street, Toronto, ON, Canada", "Condo - For Rent"),
        ("350 Victoria St, Toronto, ON, Canada", "Condo - For Sale"),
    ]

    for address, label in properties:
        location = geocode(address)
        if location:
            marker = map_widget.set_marker(location.latitude, location.longitude, text=label)
            marker.text_font = ("Arial", 14, "bold")
            marker.text_color = "red"
            marker.text_bg_color = "white"
        else:
            print(f"Warning: Geocoding failed for address: {address}")