import customtkinter as ctk
from PIL import Image, ImageTk

def home_window(parent, user):
    # Clear old stuff
    for widget in parent.winfo_children():
        widget.destroy()

    parent.pack_propagate(False)

    image_path = "start_image.jpg"

    try:
        image = Image.open(image_path)
    except Exception as e:
        print(f"Could not load home screen image {image_path}: {e}")
        image = None

    image_label = None
    pil_image_original = image

    if pil_image_original:
        # Create a default size image for the initial screen
        pil_resized = pil_image_original.resize((1200, 800), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(pil_resized)

        image_label = ctk.CTkLabel(parent, image=photo, text="")
        image_label.image = photo  # keep reference alive
        image_label.pack(expand=True, fill="both")

        def resize_image(event):
            # Check if the label still exists to avoid _tkinter.TclError
            if not image_label or not image_label.winfo_exists():
                return

            new_width = parent.winfo_width()
            new_height = parent.winfo_height()

            # Re-create a resized PhotoImage
            resized_img = pil_image_original.resize((new_width, new_height), Image.Resampling.LANCZOS)
            photo_resized = ImageTk.PhotoImage(resized_img)

            # Update the label safely
            image_label.configure(image=photo_resized)
            image_label.image = photo_resized

        # Bind the <Configure> event to dynamically resize the image
        parent.bind("<Configure>", resize_image)
    else:
        # No image fallback
        ctk.CTkLabel(parent, text="Homeez - No Background Image", font=("Arial Black", 20)).pack(pady=20)

    # If the user is logged in, greet them
    if user:
        greeting = ctk.CTkLabel(
            parent, text=f"Welcome back, {user.username}!", 
            font=("Arial Black", 30), 
            text_color="#ff8c69"
        )
        greeting.place(relx=0.5, rely=0.9, anchor="center")

    title_label = ctk.CTkLabel(
        parent, text=f"Homeez - Toronto", 
        font=("Arial Black", 30), 
        text_color="#ff8c69"
    )
    title_label.place(relx=0.5, rely=0.05, anchor="center")
