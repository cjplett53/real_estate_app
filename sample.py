import customtkinter as ctk
from PIL import Image, ImageTk
# We do NOT do "from PIL import ImageResampling" to avoid the ImportError.
# We can still call "Image.Resampling.LANCZOS" if Pillow is 9.1.0 or newer.

# Existing module imports
from windows import *

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
# MAIN WINDOW CODE
##############################################################################

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Homeez - Toronto")
root.geometry("1200x800")

nav_bar = ctk.CTkFrame(root, width=80, fg_color="black")
nav_bar.pack(fill="y", side="left", padx=5, pady=5)

# background = ctk.CTkFrame(root)
# background.pack(fill="both",expand=True)

main_content = ctk.CTkFrame(root) 
main_content.pack(fill="both",expand=True)

# Initial window focusd on howe window
home_window(main_content)

hide_button = ctk.CTkButton(
    nav_bar, text="<<<", corner_radius=10, width=100, height=20,
    fg_color="#ff8c69", hover_color="#ffa07a", text_color="black",
    # command=lambda: buy_window(nav_bar)
)
hide_button.pack( padx=5, pady=5)

home_button = ctk.CTkButton(
    nav_bar, text="Home", corner_radius=10, width=100, height=40,
    fg_color="#ff8c69", hover_color="#ffa07a", text_color="black",
    command=lambda: home_window(main_content)
)
home_button.pack( padx=5, pady=5)

buy_button = ctk.CTkButton(
    nav_bar, text="Buy", corner_radius=10, width=100, height=40,
    fg_color="#ff8c69", hover_color="#ffa07a", text_color="black",
    command=lambda: buy_window(main_content)
)
buy_button.pack(padx=5, pady=5)

rent_button = ctk.CTkButton(
    nav_bar, text="Rent", corner_radius=10, width=100, height=40,
    fg_color="#ff8c69", hover_color="#ffa07a", text_color="black"
)
rent_button.pack(padx=5, pady=5)

sell_button = ctk.CTkButton(
    nav_bar, text="Sell", corner_radius=10, width=100, height=40,
    fg_color="#ff8c69", hover_color="#ffa07a", text_color="black"
)
sell_button.pack(padx=5, pady=5)

map_button = ctk.CTkButton(
    nav_bar, text="Map", corner_radius=10, width=100, height=40,
    fg_color="#ff8c69", hover_color="#ffa07a", text_color="black",
    command=lambda: map_window(main_content)  # no lat/lon => goes to default
)
map_button.pack(padx=5, pady=5)

# REPLACE old message button with agent catalog
message_button = ctk.CTkButton(
    nav_bar, text="Message", corner_radius=10, width=100, height=40,
    fg_color="#ff8c69", hover_color="#ffa07a", text_color="black",
    command=lambda: browse_agents_window(main_content,db)  # Show all agents
)
message_button.pack(padx=5, pady=5)

browse_button = ctk.CTkButton(
    nav_bar, text="Browse", corner_radius=10, width=100, height=40,
    fg_color="#ff8c69", hover_color="#ffa07a", text_color="black",
    command=lambda: browse_properties_window(main_content,db)  # Show all properties
)
browse_button.pack(padx=5, pady=5)

sign_in_button = ctk.CTkButton(
    nav_bar, text="Sign In", corner_radius=10, width=100, height=40,
    fg_color="#ff8c69", hover_color="#ffa07a", text_color="black"
)
sign_in_button.pack(padx=5, pady=5)

root.mainloop()