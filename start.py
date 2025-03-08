import customtkinter as ctk
from PIL import Image, ImageTk
from buy import buy_window
from message import message_window
from map_window import map_window

# geopy imports for address search
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

def resize_image(event):
    new_width = event.width
    new_height = event.height
    resized_image = image.resize((new_width, new_height), Image.LANCZOS)
    if new_width > 1.5 * new_height:
        photo = ctk.CTkImage(dark_image=resized_image, size=(int(new_height*2), int(new_height)))
    else:
        photo = ctk.CTkImage(dark_image=resized_image, size=(new_width, new_width / 2))
    image_label.configure(image=photo)
    image_label.image = photo

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Homeez - Toronto")
root.geometry("1200x800")

top_frame = ctk.CTkFrame(root, height=100, fg_color="black")
top_frame.pack(fill="x")

buy_button = ctk.CTkButton(
    top_frame, text="Buy", corner_radius=10, width=80, height=40,
    fg_color="#ff8c69", hover_color="#ffa07a", text_color="black",
    command=lambda: buy_window(root)
)
buy_button.pack(side="left", padx=10, pady=10)

rent_button = ctk.CTkButton(
    top_frame, text="Rent", corner_radius=10, width=80, height=40,
    fg_color="#ff8c69", hover_color="#ffa07a", text_color="black"
)
rent_button.pack(side="left", padx=10, pady=10)

sell_button = ctk.CTkButton(
    top_frame, text="Sell", corner_radius=10, width=80, height=40,
    fg_color="#ff8c69", hover_color="#ffa07a", text_color="black"
)
sell_button.pack(side="left", padx=10, pady=10)

map_button = ctk.CTkButton(
    top_frame, text="Map", corner_radius=10, width=80, height=40,
    fg_color="#ff8c69", hover_color="#ffa07a", text_color="black",
    command=lambda: map_window(root)  # no lat/lon => goes to default
)
map_button.pack(side="left", padx=10, pady=10)

message_button = ctk.CTkButton(
    top_frame, text="Message", corner_radius=10, width=80, height=40,
    fg_color="#ff8c69", hover_color="#ffa07a", text_color="black",
    command=lambda: message_window(root)
)
message_button.pack(side="left", padx=10, pady=10)

sign_in_button = ctk.CTkButton(
    top_frame, text="Sign In", corner_radius=10, width=80, height=40,
    fg_color="#ff8c69", hover_color="#ffa07a", text_color="black"
)
sign_in_button.pack(side="right", padx=10, pady=10)

image_path = "start_image.jpg"
image = Image.open(image_path)
image = image.resize((1200, 600))
photo = ctk.CTkImage(dark_image=image, size=(800, 400))
image_label = ctk.CTkLabel(root, image=photo, text="")
image_label.pack(expand=True, fill="both")
root.bind("<Configure>", resize_image)

title_label = ctk.CTkLabel(
    root, text="Homeez - Toronto", font=("Arial Black", 30), text_color="#ff8c69"
)
title_label.pack()

bottom_frame = ctk.CTkFrame(root, height=100, fg_color="black")
bottom_frame.pack(fill="x")

search_frame = ctk.CTkFrame(bottom_frame, corner_radius=10, fg_color="black", height=40)
search_frame.pack(pady=20)

search_entry = ctk.CTkEntry(
    search_frame, placeholder_text="Enter an address", corner_radius=10, width=400
)
search_entry.pack(side="left", padx=10, pady=5)

geolocator = Nominatim(user_agent="homeez_map_app_search")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=0.1)

def search_address():
    address = search_entry.get().strip()
    if not address:
        print("No address entered.")
        return

    location = geocode(address)
    if location:
        lat, lon = location.latitude, location.longitude
        map_window(root, lat, lon)
    else:
        print(f"Could not geocode address: {address}")

search_button = ctk.CTkButton(
    search_frame, text="Search", corner_radius=10, width=80,
    fg_color="#ff8c69", hover_color="#ffa07a", text_color="black",
    command=search_address
)
search_button.pack(side="left", padx=5)

root.mainloop()
