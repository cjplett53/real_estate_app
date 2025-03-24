import customtkinter as ctk
import tkintermapview
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import real_estate_pb2
import math
from PIL import Image, ImageTk

def map_window(parent, stub, lat=None, lon=None):
    
    # Create window
    win = ctk.CTkToplevel(parent)
    win.title("Map - Toronto")
    win.geometry("1200x800")

    # Ensure the window appears on top and gets focus
    win.transient(parent)
    win.grab_set()
    win.lift(parent)
    win.focus_force()

    # Create the tkintermapview widget
    map_widget = tkintermapview.TkinterMapView(
        win, width=1200, height=800, corner_radius=0
    )
    map_widget.pack(fill="both", expand=True)

    # Set the tile server (using Carto's light basemap).
    map_widget.set_tile_server("https://cartodb-basemaps-a.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png")

    # Center the map, default to downtown Toronto.
    if lat is not None and lon is not None:
        map_widget.set_position(lat, lon)
        map_widget.set_zoom(15)
    else:
        map_widget.set_position(43.6532, -79.3832)
        map_widget.set_zoom(15)

    # Initialize geocoder
    geolocator = Nominatim(user_agent="homeez_map_app")
    geocode = RateLimiter(lambda address: geolocator.geocode(address, timeout=5), 
                          min_delay_seconds=0.5, 
                          max_retries=3, 
                          error_wait_seconds=2)

    # Retrieve all properties from the database via gRPC
    response = stub.ListProperties(real_estate_pb2.ListPropertiesRequest())
    
    # TEMPORARY: only include properties with IDs P001 and P006 as tests
    test_ids = {"P001", "P006"}
    filtered_properties = [p for p in response.properties if p.property_id in test_ids]

    # List to store marker objects along with their property info
    markers_list = []

    # create an info pop-up (set to when a marker is hovered)
    def open_info_popup(prop):
        info_win = ctk.CTkToplevel(win)
        info_win.title("Property Info")
        info_win.geometry("300x150")
        info_frame = ctk.CTkFrame(info_win)
        info_frame.pack(fill="both", expand=True, padx=5, pady=5)
        info_text = (
            f"Name: {prop.property_name}\n"
            f"Info: {prop.property_info}\n"
            f"Price: {prop.price_lease_rent}\n"
            f"Location: {prop.location}\n"
            f"Agent: {prop.agent_id}"
        )
        info_label = ctk.CTkLabel(info_frame, text=info_text, justify="left")
        info_label.pack(padx=5, pady=5)

    hover_popup = None

    def on_marker_enter(event, prop):
        nonlocal hover_popup
        if hover_popup is not None:
            hover_popup.destroy()

        hover_popup = ctk.CTkToplevel(win)
        hover_popup.overrideredirect(True)

        x = event.x_root + 10
        y = event.y_root + 10
        hover_popup.geometry(f"+{x}+{y}")

        info_frame = ctk.CTkFrame(hover_popup)
        info_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        if hasattr(prop, "image_path") and prop.image_path:
            try:
                img = Image.open(prop.image_path)
                img = img.resize((100, 100), Image.LANCZOS)  # Resize for display
                photo = ImageTk.PhotoImage(img)
                hover_popup.property_photo = photo  
                image_label = ctk.CTkLabel(info_frame, image=photo, text="")  
                image_label.image = photo
                image_label.pack(padx=5, pady=5)
            except Exception as e:
                print("Error loading property image:", e)
        
        # Build the property info
        info_text = (
            f"Name: {prop.property_name}\n"
            f"Info: {prop.property_info}\n"
            f"Price: {prop.price_lease_rent}\n"
            f"Location: {prop.location}\n"
            f"Agent: {prop.agent_id}"
        )
        info_label = ctk.CTkLabel(info_frame, text=info_text, justify="left")
        info_label.pack(padx=5, pady=5)


    def on_marker_leave(event):
        nonlocal hover_popup
        if hover_popup:
            hover_popup.destroy()
            hover_popup = None

    # place a marker on the map
    for prop in filtered_properties:
        address_full = prop.location
        # Simplify the address by splitting by comma and joining first two parts (street address and city) (lazy solution)
        parts = address_full.split(',')
        if len(parts) >= 2:
            simple_address = parts[0].strip() + ", " + parts[1].strip()
        else:
            simple_address = address_full.strip()

        # Marker label set to address
        label = simple_address

        location_obj = geocode(address_full)
        if location_obj:
            marker = map_widget.set_marker(location_obj.latitude, location_obj.longitude, text=label)
            # print(marker.__dict__)
            marker.text_font = ("Arial", 14, "bold")
            marker.text_color = "red"
            marker.text_bg_color = "white"

            map_widget.canvas.tag_bind(
                marker.big_circle,
                "<Enter>",
                lambda event, p=prop: on_marker_enter(event, p)
            )
            map_widget.canvas.tag_bind(
                marker.big_circle,
                "<Leave>",
                on_marker_leave
            )
            # Bind hover events to the marker text to increase hover range
            if hasattr(marker, "canvas_text"):
                map_widget.canvas.tag_bind(
                    marker.canvas_text,
                    "<Enter>",
                    lambda event, p=prop: on_marker_enter(event, p)
                )
                map_widget.canvas.tag_bind(
                    marker.canvas_text,
                    "<Leave>",
                    on_marker_leave
                )

            markers_list.append((marker, prop))
        else:
            print(f"Warning: Geocoding failed for address: {address_full}")
