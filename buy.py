import customtkinter as ctk
import real_estate_pb2
import real_estate_pb2_grpc
from PIL import Image, ImageTk

def buy_window(parent, stub):
    # Clear any existing widgets in the parent
    for widget in parent.winfo_children():
        widget.destroy()

    # Make sure the parent doesn't shrink
    parent.pack_propagate(False)

    title_label = ctk.CTkLabel(parent, text="Buy a Property", font=("Arial Black", 20))
    title_label.pack(pady=20)

    # Call gRPC to list all properties
    response = stub.ListProperties(real_estate_pb2.ListPropertiesRequest())
    all_properties = response.properties

    # Filter for property_type == "buy" cap insensitive
    buy_props = [p for p in all_properties if (p.property_type or "").lower() == "buy"]

    # Create a scrollable frame to hold the results
    scroll_frame = ctk.CTkScrollableFrame(parent, width=800, height=600)
    scroll_frame.pack(expand=True, fill="both", padx=10, pady=10)

    # Property frame
    row_index = 0
    for prop in buy_props:
        frame = ctk.CTkFrame(scroll_frame)
        frame.grid(row=row_index, column=0, padx=10, pady=10, sticky="w")
        row_index += 1

        # Attempt to load the property's image
        if prop.image_path:
            try:
                img = Image.open(prop.image_path)
                img = img.resize((120, 80))
                tk_img = ImageTk.PhotoImage(img)
                img_label = ctk.CTkLabel(frame, image=tk_img, text="")
                img_label.image = tk_img
                img_label.pack(side="left", padx=5, pady=5)
            except Exception as e:
                print(f"Could not load image {prop.image_path}: {e}")

        price_str = prop.price_lease_rent or "0"

        info_str = (
            f"Name: {prop.property_name}\n"
            f"Info: {prop.property_info}\n"
            f"Price: {price_str}\n"
            f"Location: {prop.location}\n"
            f"Agent: {prop.agent_id}"
        )
        info_label = ctk.CTkLabel(frame, text=info_str, justify="left")
        info_label.pack(side="left", padx=10, pady=5)
