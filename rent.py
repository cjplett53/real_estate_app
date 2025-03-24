import customtkinter as ctk
import real_estate_pb2
import real_estate_pb2_grpc
from PIL import Image, ImageTk

def rent_window(parent, stub):
    """
    Shows all 'rent' properties from Firestore via gRPC.
    """

    # Clear any existing widgets
    for widget in parent.winfo_children():
        widget.destroy()

    parent.pack_propagate(False)

    title_label = ctk.CTkLabel(parent, text="Rent a Property", font=("Arial Black", 20))
    title_label.pack(pady=20)

    # gRPC: List all properties
    response = stub.ListProperties(real_estate_pb2.ListPropertiesRequest())
    all_properties = response.properties

    # Filter for property_type == "rent"
    rent_props = [p for p in all_properties if (p.property_type or "").lower() == "rent"]

    scroll_frame = ctk.CTkScrollableFrame(parent, width=800, height=600)
    scroll_frame.pack(expand=True, fill="both", padx=10, pady=10)

    row_index = 0
    for prop in rent_props:
        frame = ctk.CTkFrame(scroll_frame)
        frame.grid(row=row_index, column=0, padx=10, pady=10, sticky="w")
        row_index += 1

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

        # Convert numeric Firestore field (sent as string) safely
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
