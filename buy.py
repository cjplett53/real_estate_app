import customtkinter as ctk

def buy_window():
    buy_window = ctk.CTkToplevel()
    buy_window.title("Buy Property")
    buy_window.geometry("400x300")
    
    # Add content to the new window
    buy_label = ctk.CTkLabel(buy_window, text="Buy a Property", font=("Arial Black", 20))
    buy_label.pack(pady=20)

    # Example of additional widgets in the new window
    instructions_label = ctk.CTkLabel(buy_window, text="Enter details to search for a property.")
    instructions_label.pack(pady=10)

    search_entry = ctk.CTkEntry(buy_window, placeholder_text="Property details", width=200)
    search_entry.pack(pady=5)
    
    search_button = ctk.CTkButton(buy_window, text="Search", corner_radius=10, width=100)
    search_button.pack(pady=10)