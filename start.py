import customtkinter as ctk
from PIL import Image, ImageTk
# We do NOT do "from PIL import ImageResampling" to avoid the ImportError.
# We can still call "Image.Resampling.LANCZOS" if Pillow is 9.1.0 or newer.

# Existing module imports
from buy import buy_window
from message import message_window  # You can adapt or remove if not needed
from map_window import map_window

import firebase_admin
from firebase_admin import credentials, firestore

# 1) Load your service account key JSON
cred = credentials.Certificate("realestate-4b2f6-firebase-adminsdk-fbsvc-70c201f38d.json")
firebase_admin.initialize_app(cred)

# 2) Get a Firestore client
db = firestore.client()

##############################################################################
# DATABASE HELPER FUNCTIONS
##############################################################################

def create_agent(agent_id, agent_name, agent_info, agent_contact_info, agent_image_path=None):
    """
    Inserts/Updates an Agent document in the 'agents' collection.
    agent_id is used as the Firestore document ID.
    agent_image_path: local path (e.g., "Agents/Agent1.png") if you want agent images.
    """
    data = {
        "agentId": agent_id,
        "agentName": agent_name,
        "agentInfo": agent_info,
        "agentContactInfo": agent_contact_info
    }
    if agent_image_path:
        data["agentImagePath"] = agent_image_path

    db.collection("agents").document(agent_id).set(data)
    print(f"Agent '{agent_id}' created/updated in Firestore.")

def create_property(property_id, property_name, property_type, property_info,
                    price_lease_rent, location, image_path, agent_id):
    """
    Inserts/Updates a Property document in the 'properties' collection.
    property_id is used as the Firestore document ID.
    property_type can be 'buy' or 'rent'.
    """
    data = {
        "propertyId": property_id,
        "propertyName": property_name,
        "propertyType": property_type,  # 'buy' or 'rent'
        "propertyInfo": property_info,
        "priceLeaseRent": price_lease_rent,
        "location": location,
        "imagePath": image_path,  # local path or could be a URL
        "agentId": agent_id
    }
    db.collection("properties").document(property_id).set(data)
    print(f"Property '{property_id}' created/updated in Firestore.")

def create_customer(customer_id, customer_name, customer_phone,
                    customer_address, customer_preferences):
    """
    Inserts/Updates a Customer document in the 'customers' collection.
    customer_id is used as the Firestore document ID.
    """
    data = {
        "customerId": customer_id,
        "customerName": customer_name,
        "customerPhone": customer_phone,
        "customerAddress": customer_address,
        "customerPreferences": customer_preferences
    }
    db.collection("customers").document(customer_id).set(data)
    print(f"Customer '{customer_id}' created/updated in Firestore.")

def save_property_for_customer(customer_id, property_id):
    """
    Inserts a record in 'customer_saved_properties' linking a customer to a property.
    Uses a composite doc ID for uniqueness: "customerId_propertyId".
    """
    doc_id = f"{customer_id}_{property_id}"
    data = {
        "customerId": customer_id,
        "propertyId": property_id
    }
    db.collection("customer_saved_properties").document(doc_id).set(data)
    print(f"Customer '{customer_id}' saved property '{property_id}' in Firestore.")

def add_customer_agent_message(customer_id, agent_id, message):
    """
    Inserts a message document in 'customer_agent_messaging_history'.
    Each message is a separate doc (auto ID).
    If you need a single doc per (customer, agent), adapt accordingly.
    """
    data = {
        "customerId": customer_id,
        "agentId": agent_id,
        "message": message
        # Optionally add a timestamp: "timestamp": firestore.SERVER_TIMESTAMP
    }
    doc_ref = db.collection("customer_agent_messaging_history").document()
    doc_ref.set(data)
    print(f"Message added for customer '{customer_id}' and agent '{agent_id}' in Firestore.")

##############################################################################
# SEED SAMPLE DATA (10 Agents, 10 Properties: 5 buy, 5 rent)
##############################################################################

def seed_sample_data():
    """
    Creates 10 agents and 10 properties (5 buy, 5 rent) in Firestore.
    You can run this once, then comment out the call at the bottom.
    """
    # 10 Agents
    agents_data = [
        # agent_id, agent_name, agent_info, agent_contact_info, (optional) agent_image_path
        ("A001", "Agent Fred", "5 years experience, specialized in condos", "Fred@example.com", "Agents/Agent1.png"),
        ("A002", "Agent Sarah",   "Family homes in suburbs",                  "Sarah@example.com",    "Agents/Agent2.png"),
        ("A003", "Agent Carol", "Luxury property expert",                   "Carol@example.com",  "Agents/Agent3.png"),
        ("A004", "Agent Davinder",  "Downtown rental specialist",               "Davinder@example.com",   "Agents/Agent4.png"),
        ("A005", "Agent Steve",   "Commercial and residential",               "Steve@example.com",    "Agents/Agent5.png"),
        ("A006", "Agent Frank", "High-end mansions",                        "Frank@example.com",  "Agents/Agent6.png"),
        ("A007", "Agent John", "Investment properties",                    "John@example.com",  "Agents/Agent7.png"),
        ("A008", "Agent Henry", "First-time home buyers",                   "Henry@example.com",  "Agents/Agent8.png"),
        ("A009", "Agent Irene", "Suburban family homes",                    "Irene@example.com",  "Agents/Agent9.png"),
        ("A010", "Agent Jack",  "Condos and apartments",                    "Jack@example.com",   "Agents/Agent10.png"),
    ]
    for a in agents_data:
        # if you changed create_agent(...) to accept agent_image_path, do:
        create_agent(a[0], a[1], a[2], a[3], a[4])

    # 10 Properties (5 buy, 5 rent)
    # property_id, property_name, property_type, property_info, price_lease_rent, location, image_path, agent_id
    properties_data = [
        ("P001", "House #1", "buy",  "3 bed, 2 bath", 500000,  "Toronto",    "images/house1.png", "A001"),
        ("P002", "House #2", "buy",  "4 bed, 3 bath", 600000,  "Brampton",   "images/house2.png", "A002"),
        ("P003", "House #3", "buy",  "2 bed, 1 bath", 400000,  "Markham",    "images/house3.png", "A003"),
        ("P004", "House #4", "buy",  "3 bed, 2 bath", 550000,  "Mississauga","images/house4.png", "A004"),
        ("P005", "House #5", "buy",  "5 bed, 4 bath", 900000,  "Toronto",    "images/house5.png", "A005"),

        ("P006", "House #6", "rent", "2 bed, 1 bath", 2000,    "Toronto",    "images/house6.png", "A006"),
        ("P007", "House #7", "rent", "3 bed, 2 bath", 2500,    "Brampton",   "images/house7.png", "A007"),
        ("P008", "House #8", "rent", "1 bed, 1 bath", 1500,    "Markham",    "images/house8.png", "A008"),
        ("P009", "House #9", "rent", "2 bed, 1 bath", 2200,    "Toronto",    "images/house9.png", "A009"),
        ("P010", "House #10","rent", "4 bed, 3 bath", 3500,    "Mississauga","images/house10.png","A010"),
    ]
    for p in properties_data:
        create_property(*p)

    print("Seeding complete! 10 agents + 10 properties (5 buy, 5 rent) added to Firestore.")

##############################################################################
# DETAILS WINDOW FOR A SINGLE PROPERTY
##############################################################################

def open_property_details(parent, property_id):
    """
    Opens a new window showing the full details of a single property,
    plus optional assigned agent info.
    """
    # Fetch the property doc from Firestore
    doc = db.collection("properties").document(property_id).get()
    if not doc.exists:
        print(f"Property {property_id} not found in Firestore.")
        return
    prop_data = doc.to_dict()

    detail_win = ctk.CTkToplevel(parent)
    detail_win.title(prop_data.get("propertyName", "No Name"))
    detail_win.geometry("600x500")

    # Title
    title_label = ctk.CTkLabel(detail_win, text=prop_data["propertyName"], font=("Arial", 18, "bold"))
    title_label.pack(pady=10)

    # Load a larger image if available
    image_path = prop_data.get("imagePath", "")
    if image_path:
        try:
            img = Image.open(image_path)
            img = img.resize((400, 300), resample=Image.Resampling.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)
            img_label = ctk.CTkLabel(detail_win, image=img_tk, text="")
            img_label.image = img_tk
            img_label.pack(pady=10)
        except Exception as e:
            print(f"Error loading image {image_path}: {e}")

    # Show property info
    # Optionally fetch the agent's name here
    agent_id = prop_data.get("agentId", "")
    agent_name = agent_id
    if agent_id:
        agent_doc = db.collection("agents").document(agent_id).get()
        if agent_doc.exists:
            agent_data = agent_doc.to_dict()
            agent_name = agent_data.get("agentName", agent_id)

    info_text = (
        f"Info: {prop_data.get('propertyInfo', 'N/A')}\n"
        f"Price/Lease/Rent: {prop_data.get('priceLeaseRent', 'N/A')}\n"
        f"Location: {prop_data.get('location', 'N/A')}\n"
        f"Type: {prop_data.get('propertyType', 'N/A')}\n"
        f"Agent: {agent_name}"
    )
    info_label = ctk.CTkLabel(detail_win, text=info_text, justify="left")
    info_label.pack(pady=5)

##############################################################################
# BROWSE PROPERTIES WINDOW WITH THUMBNAILS & DETAILS BUTTON
##############################################################################

def browse_properties_window(parent):
    """
    Opens a Toplevel window listing all documents in the 'properties' collection.
    Each property shows a small thumbnail image, name, short info, and assigned agent name.
    """
    win = ctk.CTkToplevel(parent)
    win.title("Browse Properties")
    win.geometry("800x600")

    win.transient(parent)
    win.grab_set()
    win.lift(parent)
    win.focus_force()

    # Fetch all properties
    docs = db.collection("properties").stream()
    properties = []
    for doc in docs:
        prop_data = doc.to_dict()

        # Also fetch the agent name to display in the listing
        agent_id = prop_data.get("agentId", "")
        agent_name = agent_id
        if agent_id:
            agent_doc = db.collection("agents").document(agent_id).get()
            if agent_doc.exists:
                agent_data = agent_doc.to_dict()
                agent_name = agent_data.get("agentName", agent_id)

        prop_data["agentName"] = agent_name
        properties.append(prop_data)

    # Create a scrollable frame
    scroll_frame = ctk.CTkScrollableFrame(win, width=780, height=550)
    scroll_frame.pack(padx=10, pady=10, fill="both", expand=True)

    row_index = 0
    for prop in properties:
        # Outer frame for each property listing
        prop_frame = ctk.CTkFrame(scroll_frame, corner_radius=10)
        prop_frame.grid(row=row_index, column=0, padx=10, pady=10, sticky="w")
        row_index += 1

        # Attempt to load a small/thumbnail image
        image_path = prop.get("imagePath", "")
        if image_path:
            try:
                img = Image.open(image_path)
                img = img.resize((120, 80), resample=Image.Resampling.LANCZOS)
                img_tk = ImageTk.PhotoImage(img)
                thumb_label = ctk.CTkLabel(prop_frame, image=img_tk, text="")
                thumb_label.image = img_tk  # keep a reference
                thumb_label.pack(side="left", padx=5, pady=5)
            except Exception as e:
                print(f"Error loading image {image_path}: {e}")

        # Info frame (to the right of the thumbnail)
        info_frame = ctk.CTkFrame(prop_frame, corner_radius=0, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True, padx=10, pady=5)

        # Property Title
        title_label = ctk.CTkLabel(
            info_frame,
            text=prop.get("propertyName", "No Name"),
            font=("Arial", 16, "bold")
        )
        title_label.pack(anchor="w")

        info_str = (
            f"Info: {prop.get('propertyInfo', 'N/A')}\n"
            f"Price/Lease/Rent: {prop.get('priceLeaseRent', 'N/A')}\n"
            f"Location: {prop.get('location', 'N/A')}\n"
            f"Type: {prop.get('propertyType', 'N/A')}\n"
            f"Agent: {prop.get('agentName', 'N/A')}"
        )
        info_label = ctk.CTkLabel(info_frame, text=info_str, justify="left")
        info_label.pack(anchor="w", pady=(2, 5))

        # "View Details" button
        def open_details(p=prop):
            prop_id = p.get("propertyId")
            if prop_id:
                open_property_details(win, prop_id)
            else:
                print("No propertyId found for this listing.")

        details_button = ctk.CTkButton(info_frame, text="View Details", command=open_details)
        details_button.pack(anchor="w")

        # A separator line
        sep = ctk.CTkLabel(info_frame, text="—" * 60)
        sep.pack(anchor="w", pady=(5, 0))

##############################################################################
# BROWSE AGENTS WINDOW (for "Message" button)
##############################################################################

def open_chat_window(parent, agent_id):
    """
    A placeholder function to open a chat window with the specified agent.
    """
    chat_win = ctk.CTkToplevel(parent)
    chat_win.title(f"Chat with {agent_id}")
    chat_win.geometry("400x300")

    # Example UI
    ctk.CTkLabel(chat_win, text=f"Chat with Agent {agent_id}", font=("Arial", 16)).pack(pady=10)

    # You can integrate your existing message.py logic here, or adapt it.

def browse_agents_window(parent):
    """
    Opens a Toplevel window listing all agents with their image, info,
    and a 'Message Now' button.
    """
    win = ctk.CTkToplevel(parent)
    win.title("Agents")
    win.geometry("800x600")

    win.transient(parent)
    win.grab_set()
    win.lift(parent)
    win.focus_force()

    # Fetch all agents
    docs = db.collection("agents").stream()
    agents = []
    for doc in docs:
        agents.append(doc.to_dict())

    # Create a scrollable frame
    scroll_frame = ctk.CTkScrollableFrame(win, width=780, height=550)
    scroll_frame.pack(padx=10, pady=10, fill="both", expand=True)

    row_index = 0
    for agent in agents:
        agent_frame = ctk.CTkFrame(scroll_frame, corner_radius=10)
        agent_frame.grid(row=row_index, column=0, padx=10, pady=10, sticky="w")
        row_index += 1

        # Attempt to load the agent's image if "agentImagePath" is stored
        agent_image_path = agent.get("agentImagePath", "")
        if agent_image_path:
            try:
                img = Image.open(agent_image_path)
                img = img.resize((100, 100), resample=Image.Resampling.LANCZOS)
                img_tk = ImageTk.PhotoImage(img)
                img_label = ctk.CTkLabel(agent_frame, image=img_tk, text="")
                img_label.image = img_tk
                img_label.pack(side="left", padx=5, pady=5)
            except Exception as e:
                print(f"Error loading agent image {agent_image_path}: {e}")

        # Info frame
        info_frame = ctk.CTkFrame(agent_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True, padx=10)

        title_label = ctk.CTkLabel(info_frame, text=agent.get("agentName", "Unknown"), font=("Arial", 16, "bold"))
        title_label.pack(anchor="w")

        info_str = (
            f"Info: {agent.get('agentInfo', 'N/A')}\n"
            f"Contact: {agent.get('agentContactInfo', 'N/A')}"
        )
        info_label = ctk.CTkLabel(info_frame, text=info_str, justify="left")
        info_label.pack(anchor="w")

        # "Message Now" button
        def message_now(a=agent):
            open_chat_window(win, a["agentId"])

        msg_button = ctk.CTkButton(info_frame, text="Message Now", command=message_now)
        msg_button.pack(anchor="w", pady=5)

        # Separator line
        sep = ctk.CTkLabel(info_frame, text="—" * 60)
        sep.pack(anchor="w", pady=(5, 0))

##############################################################################
# MAIN WINDOW CODE
##############################################################################

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

# REPLACE old message button with agent catalog
message_button = ctk.CTkButton(
    top_frame, text="Message", corner_radius=10, width=80, height=40,
    fg_color="#ff8c69", hover_color="#ffa07a", text_color="black",
    command=lambda: browse_agents_window(root)  # Show all agents
)
message_button.pack(side="left", padx=10, pady=10)

browse_button = ctk.CTkButton(
    top_frame, text="Browse", corner_radius=10, width=80, height=40,
    fg_color="#ff8c69", hover_color="#ffa07a", text_color="black",
    command=lambda: browse_properties_window(root)  # Show all properties
)
browse_button.pack(side="left", padx=10, pady=10)

sign_in_button = ctk.CTkButton(
    top_frame, text="Sign In", corner_radius=10, width=80, height=40,
    fg_color="#ff8c69", hover_color="#ffa07a", text_color="black"
)
sign_in_button.pack(side="right", padx=10, pady=10)

# Load and display the main background image
image_path = "start_image.jpg"
image = Image.open(image_path)
# Use LANCZOS for high-quality resizing
image = image.resize((1200, 600), resample=Image.Resampling.LANCZOS)
photo = ctk.CTkImage(dark_image=image, size=(800, 400))
image_label = ctk.CTkLabel(root, image=photo, text="")
image_label.pack(expand=True, fill="both")

def resize_image(event):
    new_width = event.width
    new_height = event.height
    resized_image = image.resize((new_width, new_height), resample=Image.Resampling.LANCZOS)
    if new_width > 1.5 * new_height:
        photo_resized = ctk.CTkImage(dark_image=resized_image, size=(int(new_height*2), int(new_height)))
    else:
        photo_resized = ctk.CTkImage(dark_image=resized_image, size=(new_width, new_width / 2))
    image_label.configure(image=photo_resized)
    image_label.image = photo_resized

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

from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

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

##############################################################################
# CALL SEED FUNCTION (OPTIONAL) - RUN ONCE, THEN COMMENT OUT
##############################################################################

#seed_sample_data()  # <-- Uncomment to insert 10 agents & 10 properties
# Then run: python start.py
# After seeing "Seeding complete!" in the console, comment out again.

root.mainloop()
