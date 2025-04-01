import customtkinter as ctk
from PIL import Image, ImageTk

def home_window(parent,user):
    # Clear old stuff
    for widget in parent.winfo_children():
        widget.destroy()

    parent.pack_propagate(False)

    print("Test: ",user)


    # Load start image
    image_path = "start_image.jpg"
    try:
        image = Image.open(image_path)
    except Exception as e:
        print(f"Could not load home screen image {image_path}: {e}")
        image = None

    if image:
        image = image.resize((1200, 800), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        image_label = ctk.CTkLabel(parent, image=photo, text="")
        image_label.image = photo  # keep reference
        image_label.pack(expand=True, fill="both")

        def resize_image(event):
            new_width = parent.winfo_width()
            new_height = parent.winfo_height()
            resized = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            photo_resized = ImageTk.PhotoImage(resized)
            image_label.configure(image=photo_resized)
            image_label.image = photo_resized

        parent.bind("<Configure>", resize_image)
    else:
        # fallback
        ctk.CTkLabel(parent, text="Homeez - No Background Image", font=("Arial Black", 20)).pack(pady=20)

    if user:
        greeting = ctk.CTkLabel(
            parent, text=f"Welcome back, {user.username}!", font=("Arial Black", 30), text_color="#ff8c69"
        )
        greeting.place(relx=0.5, rely=0.9, anchor="center")

    title_label = ctk.CTkLabel(
        parent, text=f"Homeez - Toronto ", font=("Arial Black", 30), text_color="#ff8c69"
    )
    title_label.place(relx=0.5, rely=0.05, anchor="center")



