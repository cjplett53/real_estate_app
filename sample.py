# Run this file

import customtkinter as ctk
from PIL import Image, ImageTk

# Import window functions from their respective modules
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

# Start the gRPC server as a subprocess so it can also be killed with the application
server_process = subprocess.Popen([sys.executable, "grpc_server.py"])

def main():
    # Create a gRPC channel and stub to connect to the server
    # Verify matches the one in grpc_server.py
    channel = grpc.insecure_channel('localhost:4444')
    stub = real_estate_pb2_grpc.RealEstateServiceStub(channel)

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Homeez - Toronto (gRPC Client)")
    root.geometry("1200x800")

    nav_bar = ctk.CTkFrame(root, width=80, fg_color="black")
    nav_bar.pack(fill="y", side="left", padx=5, pady=5)

    main_content = ctk.CTkFrame(root)
    main_content.pack(fill="both", expand=True)

    # Initially load the home window
    home_window(main_content)

    hide_button = ctk.CTkButton(
        nav_bar, text="<<<", corner_radius=10, width=100, height=20,
        fg_color="#ff8c69", hover_color="#ffa07a", text_color="black"
    )
    hide_button.pack(padx=5, pady=5)

    home_button = ctk.CTkButton(
        nav_bar, text="Home", corner_radius=10, width=100, height=40,
        fg_color="#ff8c69", hover_color="#ffa07a", text_color="black",
        command=lambda: home_window(main_content)
    )
    home_button.pack(padx=5, pady=5)

    # Buy button (displays properties for purchase via gRPC)
    buy_button = ctk.CTkButton(
        nav_bar, text="Buy", corner_radius=10, width=100, height=40,
        fg_color="#ff8c69", hover_color="#ffa07a", text_color="black",
        command=lambda: buy_window(main_content, stub)
    )
    buy_button.pack(padx=5, pady=5)

    # Rent button (displays properties for rent via gRPC)
    rent_button = ctk.CTkButton(
        nav_bar, text="Rent", corner_radius=10, width=100, height=40,
        fg_color="#ff8c69", hover_color="#ffa07a", text_color="black",
        command=lambda: rent_window(main_content, stub)
    )
    rent_button.pack(padx=5, pady=5)

    # Sell button (Stores to DB through gRPC)
    sell_button = ctk.CTkButton(
        nav_bar, text="Sell", corner_radius=10, width=100, height=40,
        fg_color="#ff8c69", hover_color="#ffa07a", text_color="black",
        command=lambda: sell_window(main_content, stub)
    )
    sell_button.pack(padx=5, pady=5)

    # Map button (utilizes gRPC for showing properties)
    map_btn = ctk.CTkButton(
        nav_bar, text="Map", corner_radius=10, width=100, height=40,
        fg_color="#ff8c69", hover_color="#ffa07a", text_color="black",
        command=lambda: map_window(main_content, stub)
    )
    map_btn.pack(padx=5, pady=5)

    # Message button
    msg_button = ctk.CTkButton(
        nav_bar, text="Message", corner_radius=10, width=100, height=40,
        fg_color="#ff8c69", hover_color="#ffa07a", text_color="black",
        command=lambda: message_window(main_content)
    )
    msg_button.pack(padx=5, pady=5)

    # Sign in button
    sign_in_button = ctk.CTkButton(
        nav_bar, text="Sign In", corner_radius=10, width=100, height=40,
        fg_color="#ff8c69", hover_color="#ffa07a", text_color="black",
        command=lambda: sign_in_window(main_content)
    )
    sign_in_button.pack(padx=5, pady=5)

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
