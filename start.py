import customtkinter as ctk
from PIL import Image, ImageTk
from buy import buy_window

# Function controls image size as window expands/shrinks
def resize_image(event):
    new_width = event.width
    new_height = event.height
    resized_image = image.resize((new_width, new_height), Image.LANCZOS)
    if new_width > 1.5 * new_height:
        photo = ctk.CTkImage(dark_image=resized_image, size=(new_height*2, new_height))
    else:
        photo = ctk.CTkImage(dark_image=resized_image, size=(new_width, new_width/2))
    image_label.configure(image=photo)
    image_label.image = photo

# Initialize CustomTkinter
ctk.set_appearance_mode("dark")  # Options: "dark", "light", or "system"
ctk.set_default_color_theme("blue")  # Options: "blue", "dark-blue", or "green"

root = ctk.CTk()
root.title("Homeez - Toronto")
root.geometry("1200x800") # initial window size

# Top section for buttons
top_frame = ctk.CTkFrame(root, height=100, fg_color="black") 
top_frame.pack(fill="x")
# Add buttons to the left
buy_button = ctk.CTkButton(top_frame, text="Buy", corner_radius=10, width=80, height=40, fg_color="#ff8c69", hover_color="#ffa07a", text_color="black", command=buy_window)
buy_button.pack(side="left", padx=10, pady=10)
rent_button = ctk.CTkButton(top_frame, text="Rent", corner_radius=10, width=80, height=40, fg_color="#ff8c69", hover_color="#ffa07a", text_color="black")
rent_button.pack(side="left", padx=10, pady=10)
sell_button = ctk.CTkButton(top_frame, text="Sell", corner_radius=10, width=80, height=40, fg_color="#ff8c69", hover_color="#ffa07a", text_color="black")
sell_button.pack(side="left", padx=10, pady=10)
# Add a "Sign In" button to the right
sign_in_button = ctk.CTkButton(top_frame, text="Sign In", corner_radius=10, width=80, height=40, fg_color="#ff8c69", hover_color="#ffa07a", text_color="black")
sign_in_button.pack(side="right", padx=10, pady=10)

# Load the image
image_path = "start_image.jpg" 
image = Image.open(image_path)
image = image.resize((1200, 600))
photo = ctk.CTkImage(dark_image=image, size=(800, 400))
image_label = ctk.CTkLabel(root, image=photo, text="") 
image_label.pack(expand=True, fill="both")
root.bind("<Configure>", resize_image)

# Add a title
title_label = ctk.CTkLabel(root, text="Homeez - Toronto", font=("Arial Black", 30), text_color="#ff8c69")
title_label.pack()

# Bottom frame for search bar
bottom_frame = ctk.CTkFrame(root, height=100, fg_color="black")
bottom_frame.pack(fill="x")
# Search bar
search_frame = ctk.CTkFrame(bottom_frame, corner_radius=10, fg_color="black", height=40)
search_frame.pack(pady=20)
search_entry = ctk.CTkEntry(search_frame, placeholder_text="Enter an address", corner_radius=10, width=400)
search_entry.pack(side="left", padx=10, pady=5)
search_button = ctk.CTkButton(search_frame, text="Search", corner_radius=10, width=80, fg_color="#ff8c69", hover_color="#ffa07a", text_color="black")
search_button.pack(side="left", padx=5)

root.mainloop()
