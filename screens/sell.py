import customtkinter as ctk
import real_estate_pb2
import real_estate_pb2_grpc
import random

def sell_window(parent, stub):
    # Clear old content
    for widget in parent.winfo_children():
        widget.destroy()

    parent.pack_propagate(False)

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

    # Dropdown for choosing "buy" or "rent"
    property_type_var = ctk.StringVar(value="buy")  # default to "buy"
    type_label = ctk.CTkLabel(parent, text="Property Type:")
    type_label.pack(pady=5)
    type_dropdown = ctk.CTkOptionMenu(parent, variable=property_type_var, values=["buy", "rent"])
    type_dropdown.pack(pady=5)

    def do_list_property():
        prop_name = name_entry.get().strip()
        prop_price = price_entry.get().strip()
        location = location_entry.get().strip()
        chosen_type = property_type_var.get().strip()  # "buy" or "rent"

        if not prop_name:
            print("Error: Property name is required.")
            return
        if not prop_price:
            print("Error: Price is required.")
            return
        if not location:
            print("Error: Location is required.")
            return
        if not chosen_type:
            print("Error: Property type is required.")
            return

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
                property_info="",   # Need to add this
                price_lease_rent=prop_price,
                location=location,
                image_path="",      # image path - check how DB stores images
                agent_id=random_agent_id
            )
        )
        resp = stub.CreateProperty(req)
        print(resp.message)

    create_button = ctk.CTkButton(parent, text="List Property", corner_radius=10, width=160, command=do_list_property)
    create_button.pack(pady=10)
