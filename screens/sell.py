import customtkinter as ctk
import real_estate_pb2
import real_estate_pb2_grpc
import random
from PIL import Image, ImageTk
import os
import shutil

def sell_window(parent, stub):
    global save_path
    save_path = None  # Initialize save_path variable
    def upload_and_save_image():
        global save_path
        # Create a folder to store the uploaded images (if it doesn't exist)
        upload_folder = "images"
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        # Open a file dialog to choose an image
        file_path = ctk.filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")])
        
        if file_path:
            # Open the selected image
            image = Image.open(file_path)
            image = image.resize((250, 250))  # Resize the image to fit the window

            # Convert the image to a format Tkinter can display
            photo = ImageTk.PhotoImage(image)

            # Display the image in the label
            image_label.configure(image=photo)
            image_label.image = photo  # Keep a reference to avoid garbage collection

            image_name = os.path.splitext(os.path.basename(file_path))[0]  # Get the base name without extension
            save_path = os.path.join(upload_folder, image_name + ".png")  # Save as PNG

            # Save the image (preserving the format)
            image.save(save_path, "PNG")
            print(f"Image saved to {save_path}")

    # Clear old content
    for widget in parent.winfo_children():
        widget.destroy()
    parent.pack_propagate(False)

    # Create error label to display messages
    error_label = ctk.CTkLabel(parent, text="", text_color="red")
    error_label.pack(pady=10)
    error_label.pack_forget()  # Hide initially

    title_label = ctk.CTkLabel(parent, text="List a New Property", font=("Arial Black", 20))
    title_label.pack(pady=20)

    instructions_label = ctk.CTkLabel(parent, text="Enter property details below:")
    instructions_label.pack(pady=10)

    # Property Name Entry
    name_entry = ctk.CTkEntry(parent, placeholder_text="Property Name", width=200)
    name_entry.pack(pady=5)

    # Price Entry
    price_entry = ctk.CTkEntry(parent, placeholder_text="Price or Monthly Rent", width=200)
    price_entry.pack(pady=5)

    # Location Entry
    location_entry = ctk.CTkEntry(parent, placeholder_text="Location", width=200)
    location_entry.pack(pady=5)

    #info txtbox
    info_label = ctk.CTkLabel(parent, text="List any information about the property\n(# of rooms, # of washrooms, etc.)")
    info_label.pack(pady=5)
    info_entry = ctk.CTkTextbox(parent, width=400, height=100)
    info_entry.pack(pady=5)

    # Dropdown for choosing "buy" or "rent"
    property_type_var = ctk.StringVar(value="buy")  # default to "buy"
    type_label = ctk.CTkLabel(parent, text="Property Type:")
    type_label.pack(pady=5)
    type_dropdown = ctk.CTkOptionMenu(parent, variable=property_type_var, values=["buy", "rent"])
    type_dropdown.pack(pady=5)

    # Button to upload and save the image
    upload_button = ctk.CTkButton(parent, text="Upload Image", command=upload_and_save_image)
    upload_button.pack(pady=10)

    # Label to display the uploaded image
    image_label = ctk.CTkLabel(parent,text="")
    image_label.pack(pady=10)

    def do_list_property():
        prop_name = name_entry.get().strip()
        prop_price = price_entry.get().strip()
        location = location_entry.get().strip()
        info = info_entry.get("1.0", ctk.END).strip()
        chosen_type = property_type_var.get().strip()  # "buy" or "rent"

        error_label.pack(pady=10)
        if not prop_name:
            error_label.configure(text="Property name is required.", text_color="red")
            print("Error: Property name is required.")
            return
        if not prop_price:
            error_label.configure(text="Price is required.", text_color="red")
            print("Error: Price is required.")
            return
        if not location:
            error_label.configure(text="Location is required.", text_color="red")
            print("Error: Location is required.")
            return
        if not chosen_type:
            error_label.configure(text="Property type is required..", text_color="red")
            print("Error: Property type is required.")
            return
        
        #if gotten here, successful input
        error_label.configure(text="Sucessfully Added", text_color="green")

        #Reset the entry fields
        name_entry.delete(0, ctk.END)
        price_entry.delete(0, ctk.END)
        location_entry.delete(0, ctk.END)
        image_label.configure(image="")

        # Derive a property_id from the property name
        prop_id = prop_name.lower().replace(" ", "_")

        # Select a random agent from the DB (may crash sell if no agents in DB)
        agent_response = stub.ListAgents(real_estate_pb2.ListAgentsRequest())
        agents = agent_response.agents
        random_agent = random.choice(agents)
        random_agent_id = random_agent.agent_id

        # Create a gRPC request to sell the property with the provided details
        req = real_estate_pb2.CreatePropertyRequest(
            property=real_estate_pb2.Property(
                property_id=prop_id,
                property_name=prop_name,
                property_type=chosen_type,
                property_info=f"{info}",   # Need to add this
                price_lease_rent=prop_price,
                location=location,
                image_path=f"{save_path}",      # image path - check how DB stores images
                agent_id=random_agent_id
            )
        )
        resp = stub.CreateProperty(req)
        print(resp.message)

    create_button = ctk.CTkButton(parent, text="List Property", corner_radius=10, width=160, command=do_list_property)
    create_button.pack(pady=10)

    