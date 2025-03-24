import customtkinter as ctk
import real_estate_pb2
import real_estate_pb2_grpc

def sell_window(parent, stub):
    """
    Allows a user to list a new property in Firestore via gRPC.
    The user must enter all mandatory fields: Property Name, Price, Location,
    and choose a Property Type ("buy" or "rent") so that the listing appears under the correct screen.
    """

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

    # Location Entry (new field)
    location_entry = ctk.CTkEntry(parent, placeholder_text="Location", width=200)
    location_entry.pack(pady=5)

    # Dropdown for choosing "buy" or "rent"
    property_type_var = ctk.StringVar(value="buy")  # default to "buy"
    type_label = ctk.CTkLabel(parent, text="Property Type:")
    type_label.pack(pady=5)
    type_dropdown = ctk.CTkOptionMenu(parent, variable=property_type_var, values=["buy", "rent"])
    type_dropdown.pack(pady=5)

    def do_list_property():
        # Gather user input
        prop_name = name_entry.get().strip()
        prop_price = price_entry.get().strip()
        location = location_entry.get().strip()
        chosen_type = property_type_var.get().strip()  # "buy" or "rent"

        # Mandatory fields check
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

        # Create a gRPC request to list the property with the provided details
        req = real_estate_pb2.CreatePropertyRequest(
            property=real_estate_pb2.Property(
                property_id=prop_id,
                property_name=prop_name,
                property_type=chosen_type,  # user-selected: "buy" or "rent"
                property_info=f"User-submitted property for {chosen_type}",
                price_lease_rent=prop_price,
                location=location,  # use the user-entered location
                image_path="",      # optional image path
                agent_id=""
            )
        )
        resp = stub.CreateProperty(req)
        print(resp.message)

    # Button to submit the form
    create_button = ctk.CTkButton(parent, text="List Property", corner_radius=10, width=160, command=do_list_property)
    create_button.pack(pady=10)
