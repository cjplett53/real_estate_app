import customtkinter as ctk
from PIL import Image, ImageTk
import tkintermapview
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

def buy_window(parent):
    """
    Creates the Buy Window, attached to 'parent'.
    Ensures it's in front and responds to user focus.
    """

    for widget in parent.winfo_children():
        widget.destroy()

    buy_label = ctk.CTkLabel(parent, text="Buy a Property", font=("Arial Black", 20))
    buy_label.pack(pady=20)

    instructions_label = ctk.CTkLabel(parent, text="Enter details to search for a property.")
    instructions_label.pack(pady=10)

    search_entry = ctk.CTkEntry(parent, placeholder_text="Property details", width=200)
    search_entry.pack(pady=5)

    def do_search():
        print("Search for:", search_entry.get())

    # Bind Enter key to 'do_search'
    search_entry.bind("<Return>", lambda event: do_search())

    search_button = ctk.CTkButton(parent, text="Search", corner_radius=10, width=100, command=do_search)
    search_button.pack(pady=10)


def home_window(parent):
    # Clear the parent frame before adding new content
    for widget in parent.winfo_children():
        widget.destroy()

    # Make sure parent frame doesn't shrink to fit widgets
    parent.pack_propagate(False)

    # Load and display the main background image
    image_path = "start_image.jpg"
    image = Image.open(image_path)
    image = image.resize((1200, 800), resample=Image.Resampling.LANCZOS)
    
    photo = ctk.CTkImage(dark_image=image, size=(1200, 800))
    image_label = ctk.CTkLabel(parent, image=photo, text="")
    image_label.pack(expand=True, fill="both")

    def resize_image(event):
        new_width = parent.winfo_width()
        new_height = parent.winfo_height()
        
        # Resize the image dynamically
        resized_image = image.resize((new_width, new_height), resample=Image.Resampling.LANCZOS)
        photo_resized = ctk.CTkImage(dark_image=resized_image, size=(new_width, new_height))

        image_label.configure(image=photo_resized)
        image_label.image = photo_resized  # Keep reference

    parent.bind("<Configure>", resize_image)

    # Add title label on top of the image
    title_label = ctk.CTkLabel(
        parent, text="Homeez - Toronto", font=("Arial Black", 30), text_color="#ff8c69", bg_color="black"
    )
    title_label.place(relx=0.5, rely=0.05, anchor="center")  # Center at the top

    # Add a search entry and button at the bottom

    search_frame = ctk.CTkFrame(parent, fg_color="transparent", height=40)
    search_frame.place(relx=0.5, rely=0.95, anchor="center", relwidth=0.5)

    search_entry = ctk.CTkEntry(
        search_frame, placeholder_text="Enter an address", corner_radius=10, width=400
    )
    search_entry.pack(side="bottom", padx=10, pady=5)

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
            map_window(parent, lat, lon)
        else:
            print(f"Could not geocode address: {address}")

    search_button = ctk.CTkButton(
        search_frame, text="Search", corner_radius=10, width=80,
        fg_color="#ff8c69", hover_color="#ffa07a", text_color="black",
        command=search_address
    )
    search_button.pack(side="bottom", padx=5,pady=5)


def map_window(parent, lat=None, lon=None):
    """
    Opens a Toplevel window with an interactive map. Defaults to downtown Toronto
    if no lat/lon is provided. Places property markers. If lat/lon is passed in,
    the map is centered there at zoom 15 - but no marker is placed for the searched address.
    """

    for widget in parent.winfo_children():
        widget.destroy()


    # Create the tkintermapview widget
    map_widget = tkintermapview.TkinterMapView(
        parent, 
        width=1200, 
        height=800,
        corner_radius=0
    )
    map_widget.pack(fill="both", expand=True)

    # Use a mostly grayscale tile server (Carto) - comment out if any loading issues
    map_widget.set_tile_server("https://cartodb-basemaps-a.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png")

    # If lat/lon are given, center on them. Otherwise, downtown Toronto.
    if lat is not None and lon is not None:
        map_widget.set_position(lat, lon)
        map_widget.set_zoom(15)
    else:
        map_widget.set_position(43.6532, -79.3832)
        map_widget.set_zoom(15)

    # Initialize geopy's Nominatim geocoder with a rate limiter
    geolocator = Nominatim(user_agent="homeez_map_app")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

    # List of property addresses and their corresponding labels
    properties = [
        ("100 Queen St W, Toronto, ON, Canada", "City Hall - Test"),
        ("1 Yonge Street, Toronto, ON, Canada", "Condo - For Rent"),
        ("350 Victoria St, Toronto, ON, Canada", "Condo - For Sale"),
    ]

    # Place existing property markers
    for address, label in properties:
        location = geocode(address)
        if location:
            marker = map_widget.set_marker(location.latitude, location.longitude, text=label)
            marker.text_font = ("Arial", 14, "bold")
            marker.text_color = "red"
            marker.text_bg_color = "white"
        else:
            print(f"Warning: Geocoding failed for address: {address}")

    # No marker is placed for the new searched address; we only center on it.


##############################################################################
# DETAILS WINDOW FOR A SINGLE PROPERTY
##############################################################################

def open_property_details(parent, property_id,db):
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

    for widget in parent.winfo_children():
        widget.destroy()

    parent.pack_propagate(False)

    # Title
    title_label = ctk.CTkLabel(parent, text=prop_data["propertyName"], font=("Arial", 18, "bold"))
    title_label.pack(pady=10)

    # Load a larger image if available
    image_path = prop_data.get("imagePath", "")
    if image_path:
        try:
            img = Image.open(image_path)
            img = img.resize((400, 300), resample=Image.Resampling.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)
            img_label = ctk.CTkLabel(parent, image=img_tk, text="")
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
    info_label = ctk.CTkLabel(parent, text=info_text, justify="left")
    info_label.pack(pady=5)

##############################################################################
# BROWSE PROPERTIES WINDOW WITH THUMBNAILS & DETAILS BUTTON
##############################################################################

def browse_properties_window(parent,db):
    """
    Opens a Toplevel window listing all documents in the 'properties' collection.
    Each property shows a small thumbnail image, name, short info, and assigned agent name.
    """

    for widget in parent.winfo_children():
        widget.destroy()

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
    scroll_frame = ctk.CTkScrollableFrame(parent, width=(parent.winfo_width()*0.15), height=550)
    scroll_frame.pack(side="left", padx=10, pady=10, fill="y")

    detail_frame = ctk.CTkFrame(parent, height=550, width=(parent.winfo_width()*0.85))
    detail_frame.pack(side="right", padx=10, pady=10, fill="both",ipadx=20,ipady=20)

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
                open_property_details(detail_frame, prop_id,db)
            else:
                print("No propertyId found for this listing.")

        details_button = ctk.CTkButton(info_frame, text="View Details", command=open_details)
        details_button.pack(anchor="w")

        # A separator line
        sep = ctk.CTkLabel(info_frame, text="—" * 20)
        sep.pack(anchor="w", pady=(5, 0))


##############################################################################
# BROWSE AGENTS WINDOW (for "Message" button)
##############################################################################

def open_chat_window(parent, agent_id, agent_name):
    """
    A placeholder function to open a chat window with the specified agent.
    """
    for widget in parent.winfo_children():
        widget.destroy()

    parent.pack_propagate(False)

    # Example UI
    # ctk.CTkLabel(parent, text=f"Chat with Agent {agent_id}", font=("Arial", 16)).pack(pady=10)
    from message import chatroom_window
    chatroom_window(parent, agent_id, agent_name) #temp chat system, doesnt act work...
    

    # You can integrate your existing message.py logic here, or adapt it.

def browse_agents_window(parent,db):
    """
    Opens a Toplevel window listing all agents with their image, info,
    and a 'Message Now' button.
    """

    for widget in parent.winfo_children():
        widget.destroy()

    # Fetch all agents
    docs = db.collection("agents").stream()
    agents = []
    for doc in docs:
        agents.append(doc.to_dict())

    # Create a scrollable frame
    # Create a scrollable frame
    scroll_frame = ctk.CTkScrollableFrame(parent, width=(parent.winfo_width()*0.15), height=550)
    scroll_frame.pack(side="left", padx=10, pady=10, fill="y")

    detail_frame = ctk.CTkFrame(parent, height=550, width=(parent.winfo_width()*0.85))
    detail_frame.pack(side="right", padx=10, pady=10, fill="both",ipadx=20,ipady=20)

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
            open_chat_window(detail_frame, a["agentId"], a["agentName"])

        msg_button = ctk.CTkButton(info_frame, text="Message Now", command=message_now)
        msg_button.pack(anchor="w", pady=5)

        # Separator line
        sep = ctk.CTkLabel(info_frame, text="—" * 20)
        sep.pack(anchor="w", pady=(5, 0))