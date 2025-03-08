import customtkinter as ctk

def buy_window(parent):
    """
    Creates the Buy Window, attached to 'parent'.
    Ensures it's in front and responds to user focus.
    """
    win = ctk.CTkToplevel(parent)
    win.title("Buy Property")
    win.geometry("400x300")
    
    # Make sure it's in front
    win.transient(parent)  # Make this window "modal" relative to the parent
    win.grab_set()         # Disallows interaction with parent until closed
    win.lift(parent)       # Lift it above the parent
    win.focus_force()      # Focus on this new window

    buy_label = ctk.CTkLabel(win, text="Buy a Property", font=("Arial Black", 20))
    buy_label.pack(pady=20)

    instructions_label = ctk.CTkLabel(win, text="Enter details to search for a property.")
    instructions_label.pack(pady=10)

    search_entry = ctk.CTkEntry(win, placeholder_text="Property details", width=200)
    search_entry.pack(pady=5)

    def do_search():
        print("Search for:", search_entry.get())

    # Bind Enter key to 'do_search'
    search_entry.bind("<Return>", lambda event: do_search())

    search_button = ctk.CTkButton(win, text="Search", corner_radius=10, width=100, command=do_search)
    search_button.pack(pady=10)
