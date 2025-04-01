import customtkinter as ctk
import tkintermapview
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import real_estate_pb2
import math
from PIL import Image, ImageTk

def map_window(parent, stub, lat=None, lon=None):
    # Clear existing widgets
    for widget in parent.winfo_children():
        widget.destroy()

    # Create the map widget
    map_widget = tkintermapview.TkinterMapView(parent, width=1200, height=800, corner_radius=0)
    map_widget.pack(fill="both", expand=True)

    # Configure tile server
    map_widget.set_tile_server("https://cartodb-basemaps-a.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png")

    # Center/zoom
    if lat is not None and lon is not None:
        map_widget.set_position(lat, lon)
        map_widget.set_zoom(15)
    else:
        map_widget.set_position(43.6532, -79.3832)
        map_widget.set_zoom(15)

    # Setup geocoder
    geolocator = Nominatim(user_agent="homeez_map_app")
    geocode = RateLimiter(lambda address: geolocator.geocode(address, timeout=5),
                          min_delay_seconds=0.5, max_retries=3, error_wait_seconds=2)

    # Retrieve all properties
    response = stub.ListProperties(real_estate_pb2.ListPropertiesRequest())
    filtered_properties = response.properties

    # Hover popup logic
    hover_popup = None
    def show_popup(prop, x_root, y_root):
        nonlocal hover_popup
        if hover_popup is not None:
            hover_popup.destroy()

        hover_popup = ctk.CTkToplevel(parent)
        hover_popup.overrideredirect(True)
        hover_popup.geometry(f"+{x_root + 10}+{y_root + 10}")

        info_frame = ctk.CTkFrame(hover_popup)
        info_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Image if available
        if prop.image_path:
            try:
                img = Image.open(prop.image_path)
                img = img.resize((100, 100), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                hover_popup.property_photo = photo
                image_label = ctk.CTkLabel(info_frame, image=photo, text="")
                image_label.pack(padx=5, pady=5)
            except Exception as e:
                print("Error loading property image:", e)

        info_text = (
            f"Name: {prop.property_name}\n"
            f"Info: {prop.property_info}\n"
            f"Price: {prop.price_lease_rent}\n"
            f"Location: {prop.location}\n"
            f"Agent: {prop.agent_id}"
        )
        info_label = ctk.CTkLabel(info_frame, text=info_text, justify="left")
        info_label.pack(padx=5, pady=5)

    def on_enter_canvas_item(event, prop):
        # Triggered on <Enter> for a marker item
        show_popup(prop, event.x_root, event.y_root)

    def on_leave_canvas_item(event):
        # Triggered on <Leave> for a marker item
        nonlocal hover_popup
        if hover_popup:
            hover_popup.destroy()
            hover_popup = None

    def bind_canvas_item(item_id, prop):
        # Helper to safely bind <Enter>/<Leave> to a single canvas ID
        map_widget.canvas.tag_bind(
            item_id,
            "<Enter>",
            lambda e: on_enter_canvas_item(e, prop)
        )
        map_widget.canvas.tag_bind(
            item_id,
            "<Leave>",
            on_leave_canvas_item
        )

    markers_list = []

    for prop in filtered_properties:
        address_full = prop.location
        parts = address_full.split(',')
        if len(parts) >= 2:
            simple_address = parts[0].strip() + ", " + parts[1].strip()
        else:
            simple_address = address_full.strip()

        location_obj = geocode(address_full)
        if location_obj:
            marker = map_widget.set_marker(location_obj.latitude, location_obj.longitude, text=simple_address)
            marker.text_font = ("Arial", 14, "bold")
            marker.text_bg_color = "white"
            marker.text_color = "black"
            marker.set_text(marker.text)

            # Color based on property type
            prop_type = (prop.property_type or "").lower().strip()
            if prop_type == "buy":
                marker.marker_color_circle = "#FF0000"
                marker.marker_color_outside = "#FF0000"
                if hasattr(marker, "polygon"):
                    map_widget.canvas.itemconfig(marker.polygon, fill="#FF0000", outline="#FF0000")
                if hasattr(marker, "big_circle"):
                    map_widget.canvas.itemconfig(marker.big_circle, fill="#FF0000", outline="#FF0000")
            elif prop_type == "rent":
                marker.marker_color_circle = "#0000FF"
                marker.marker_color_outside = "#0000FF"
                if hasattr(marker, "polygon"):
                    map_widget.canvas.itemconfig(marker.polygon, fill="#0000FF", outline="#0000FF")
                if hasattr(marker, "big_circle"):
                    map_widget.canvas.itemconfig(marker.big_circle, fill="#0000FF", outline="#0000FF")

            # Safely bind big_circle
            if hasattr(marker, "big_circle") and marker.big_circle:
                if isinstance(marker.big_circle, (list, tuple)):
                    for circle_id in marker.big_circle:
                        bind_canvas_item(circle_id, prop)
                else:
                    bind_canvas_item(marker.big_circle, prop)

            # Safely bind canvas_text
            if hasattr(marker, "canvas_text") and marker.canvas_text:
                if isinstance(marker.canvas_text, (list, tuple)):
                    for text_id in marker.canvas_text:
                        bind_canvas_item(text_id, prop)
                else:
                    bind_canvas_item(marker.canvas_text, prop)

            markers_list.append((marker, prop))
        else:
            print(f"Warning: Geocoding failed for address: {address_full}")

    # Raise text after creation
    def raise_all_text():
        for (marker, _) in markers_list:
            if hasattr(marker, "canvas_text") and marker.canvas_text:
                if isinstance(marker.canvas_text, (list, tuple)):
                    for txt_id in marker.canvas_text:
                        try:
                            map_widget.canvas.tag_raise(txt_id)
                        except Exception as ex:
                            print("tag_raise error (list item):", ex)
                else:
                    try:
                        map_widget.canvas.tag_raise(marker.canvas_text)
                    except Exception as ex:
                        print("tag_raise error (single text):", ex)

    map_widget.canvas.after(200, raise_all_text)