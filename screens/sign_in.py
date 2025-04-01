import customtkinter as ctk
import real_estate_pb2
from functools import partial

def sign_in_window(parent, stub, update_user_callback):

    # Clear parent frame
    for widget in parent.winfo_children():
        widget.destroy()
    
    # Create a centered container for the sign-in content
    container = ctk.CTkFrame(parent, fg_color="transparent")
    container.pack(expand=True, fill="both")
    
    # Use a fixed-width inner frame for the actual login controls
    inner_frame = ctk.CTkFrame(container, width=400, height=500, fg_color="transparent")
    inner_frame.place(relx=0.5, rely=0.4, anchor="center")
    inner_frame.pack_propagate(False)
    
    # Set up the sign-in UI
    label = ctk.CTkLabel(inner_frame, text="Sign In Window", font=("Arial Black", 20))
    label.pack(pady=20)
    
    # Create error label to display messages
    error_label = ctk.CTkLabel(inner_frame, text="", text_color="red")
    error_label.pack(pady=10)
    error_label.pack_forget()  # Hide initially

    def add_user(parent, stub):
        """Create new user account page"""
        for widget in parent.winfo_children():
            widget.destroy()
            
        # Create centered container for registration
        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.pack(expand=True, fill="both")
        
        # Use a fixed-width inner frame
        inner_frame = ctk.CTkFrame(container, width=400, height=500, fg_color="transparent")
        inner_frame.place(relx=0.5, rely=0.4, anchor="center")
        inner_frame.pack_propagate(False)

        label = ctk.CTkLabel(inner_frame, text="Create Account", font=("Arial Black", 20))
        label.pack(pady=20)

        user_label = ctk.CTkLabel(inner_frame, text="Username:")
        user_label.pack(pady=5)
        user_entry = ctk.CTkEntry(inner_frame, placeholder_text="Enter username", width=200)
        user_entry.pack(pady=5)

        pass_label1 = ctk.CTkLabel(inner_frame, text="Password:")
        pass_label1.pack(pady=5)
        pass_entry1 = ctk.CTkEntry(inner_frame, placeholder_text="Enter password", show='*', width=200)
        pass_entry1.pack(pady=5)

        pass_label2 = ctk.CTkLabel(inner_frame, text="Confirm password:")
        pass_label2.pack(pady=5)
        pass_entry2 = ctk.CTkEntry(inner_frame, placeholder_text="Re-enter password", show='*', width=200)
        pass_entry2.pack(pady=5)
        
        # Error message label
        error_register_label = ctk.CTkLabel(inner_frame, text="", text_color="red")
        error_register_label.pack(pady=10)
        error_register_label.pack_forget()  # Hide initially
        
        def register():
            username = user_entry.get()
            password1 = pass_entry1.get()
            password2 = pass_entry2.get()
            
            # Show error label if needed
            error_register_label.pack(pady=10)
            
            if password1 != password2:
                error_register_label.configure(text="Passwords do not match.")
            else:
                # Try to create the user
                response = stub.addUser(real_estate_pb2.addUserRequest(username=username, password=password1))
                if response.username: 
                    error_register_label.configure(text="User created successfully.", text_color="green")
                    parent.after(2000, lambda: sign_in_window(parent, stub, update_user_callback))
                else:
                    error_register_label.configure(text=response.status_message, text_color="red")

        register_button = ctk.CTkButton(inner_frame, text="Register", corner_radius=10, width=100, command=register)
        register_button.pack(pady=10)
        
        # Back button
        back_button = ctk.CTkButton(
            inner_frame, 
            text="Back to Sign In", 
            corner_radius=10, 
            width=100, 
            command=lambda: sign_in_window(parent, stub, update_user_callback)
        )
        back_button.pack(pady=10)

    # New user button
    new_user_button = ctk.CTkButton(
        inner_frame, 
        text="New User", 
        corner_radius=10, 
        width=100, 
        command=partial(add_user, parent, stub)
    )
    new_user_button.pack(pady=10)

    # Username and password fields
    user_label = ctk.CTkLabel(inner_frame, text="Username:")
    user_label.pack(pady=5)
    user_entry = ctk.CTkEntry(inner_frame, placeholder_text="Enter username", width=200)
    user_entry.pack(pady=5)

    pass_label = ctk.CTkLabel(inner_frame, text="Password:")
    pass_label.pack(pady=5)
    pass_entry = ctk.CTkEntry(inner_frame, placeholder_text="Enter password", show='*', width=200)
    pass_entry.pack(pady=5)

    def do_sign_in():
        """Handle sign-in button click"""
        # Show error label
        error_label.pack(pady=10)
        
        # Call the gRPC service to authenticate
        response = stub.getUser(real_estate_pb2.getUserRequest(
            username=user_entry.get(), 
            password=pass_entry.get()
        ))
        
        if response.username:
            error_label.pack(pady=10)
            error_label.configure(text="Log-In Successful.", text_color="green")
            parent.after(500, lambda: update_user_callback(response))
        else:
            error_label.configure(text=response.status_message, text_color="red")

    # Sign in button
    sign_button = ctk.CTkButton(
        inner_frame, 
        text="Sign In", 
        corner_radius=10, 
        width=100, 
        command=do_sign_in
    )
    sign_button.pack(pady=10)