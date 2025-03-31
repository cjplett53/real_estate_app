import customtkinter as ctk
from PIL import Image, ImageTk
from windows import home_window
from buy import buy_window
from rent import rent_window
from sell import sell_window
from sign_in import sign_in_window  
from message import message_window
from map_window import map_window

import grpc
import real_estate_pb2
import real_estate_pb2_grpc
import subprocess
import sys

# Start the gRPC server as  subprocess so it can also be killed with the application
server_process = subprocess.Popen([sys.executable, "grpc_server.py"])

# Create global variables to track user state
current_user = None
is_user_logged_in = False

def main():
    global current_user, is_user_logged_in
    
    # Create a gRPC channel and stub to connect to the server
    channel = grpc.insecure_channel('localhost:4444')
    stub = real_estate_pb2_grpc.RealEstateServiceStub(channel)

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Homeez - Toronto (gRPC Client)")
    root.geometry("1200x800")
    
    # Create a container frame for all navigation bars
    nav_container = ctk.CTkFrame(root, width=110, fg_color="#000000")
    nav_container.pack(side="left", fill="y", padx=0, pady=0)
    
    # Create main content area
    main_content = ctk.CTkFrame(root)
    main_content.pack(side="right", fill="both", expand=True, padx=5, pady=5)

    # Initially load the home window
    home_window(main_content,current_user)
    
    # Create navigation bars (both initially hidden)
    nav_bar = ctk.CTkFrame(nav_container, width=100, fg_color="black")
    nav_bar_signed_in = ctk.CTkFrame(nav_container, width=100, fg_color="black")    
    
    def create_nav_buttons(nav_frame):
        """Create common navigation buttons for both nav bars"""
        hide_button = ctk.CTkButton(
            nav_frame, text="<<<", corner_radius=10, width=100, height=20,
            fg_color="#ff8c69", hover_color="#ffa07a", text_color="black"
        )
        hide_button.pack(padx=5, pady=5)

        home_button = ctk.CTkButton(
            nav_frame, text="Home", corner_radius=10, width=100, height=40,
            fg_color="#ff8c69", hover_color="#ffa07a", text_color="black",
            command=lambda: home_window(main_content, current_user)
        )
        home_button.pack(padx=5, pady=5)

        buy_button = ctk.CTkButton(
            nav_frame, text="Buy", corner_radius=10, width=100, height=40,
            fg_color="#ff8c69", hover_color="#ffa07a", text_color="black",
            command=lambda: buy_window(main_content, stub)
        )
        buy_button.pack(padx=5, pady=5)

        rent_button = ctk.CTkButton(
            nav_frame, text="Rent", corner_radius=10, width=100, height=40,
            fg_color="#ff8c69", hover_color="#ffa07a", text_color="black",
            command=lambda: rent_window(main_content, stub)
        )
        rent_button.pack(padx=5, pady=5)

        sell_button = ctk.CTkButton(
            nav_frame, text="Sell", corner_radius=10, width=100, height=40,
            fg_color="#ff8c69", hover_color="#ffa07a", text_color="black",
            command=lambda: sell_window(main_content, stub)
        )
        sell_button.pack(padx=5, pady=5)

        map_btn = ctk.CTkButton(
            nav_frame, text="Map", corner_radius=10, width=100, height=40,
            fg_color="#ff8c69", hover_color="#ffa07a", text_color="black",
            command=lambda: map_window(main_content, stub)
        )
        map_btn.pack(padx=5, pady=5)

        msg_button = ctk.CTkButton(
            nav_frame, text="Message", corner_radius=10, width=100, height=40,
            fg_color="#ff8c69", hover_color="#ffa07a", text_color="black",
            command=lambda: message_window(main_content)
        )
        msg_button.pack(padx=5, pady=5)

    # Create regular nav bar (for logged out users)
    create_nav_buttons(nav_bar)
    
    sign_in_button = ctk.CTkButton(
        nav_bar, text="Sign In", corner_radius=10, width=100, height=40,
        fg_color="#ff8c69", hover_color="#ffa07a", text_color="black",
        command=lambda: sign_in_window(main_content, stub, update_user_state)
    )
    sign_in_button.pack(padx=5, pady=5)
    
    # Create logged-in nav bar
    create_nav_buttons(nav_bar_signed_in)
    
    sign_out_button = ctk.CTkButton(
        nav_bar_signed_in, text="Sign Out", corner_radius=10, width=100, height=40,
        fg_color="#ff8c69", hover_color="#ffa07a", text_color="black",
        command=lambda: sign_out(main_content)
    )
    sign_out_button.pack(padx=5, pady=5)

    # Initially show the logged-out nav bar
    nav_bar.pack(fill="both", expand=True)
    
    def sign_out(main_content):
        """Handle sign-out and reset state"""
        global current_user, is_user_logged_in
        # Reset user state
        current_user = None
        is_user_logged_in = False
        
        # Switch navigation bars (carefully managing the UI)
        nav_bar_signed_in.pack_forget()
        nav_bar.pack(fill="both", expand=True)
        
        # Refresh main content
        for widget in main_content.winfo_children():
            widget.destroy()
        home_window(main_content,current_user)
    
    def update_user_state(user):
        """Update the user state and UI based on login status"""
        global current_user, is_user_logged_in
        current_user = user
        is_user_logged_in = True if user and user.username else False
        
        if is_user_logged_in:
            # Switch to signed-in nav bar
            nav_bar.pack_forget()
            nav_bar_signed_in.pack(fill="both", expand=True)
            print(f"User logged in: {current_user.username}")
            
            # Refresh main content to show logged-in state
            for widget in main_content.winfo_children():
                widget.destroy()
            home_window(main_content,current_user)
        else:
            # Switch to regular nav bar
            nav_bar_signed_in.pack_forget()
            nav_bar.pack(fill="both", expand=True)
            print("User logged out")
    

    # When closing the window also terminate the gRPC server subprocess
    def on_close():
        try:
            server_process.terminate()
            server_process.wait(timeout=5)
        except Exception as e:
            print("Error terminating server process:", e)
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()

if __name__ == "__main__":
    main()