import customtkinter as ctk
import real_estate_pb2
from functools import partial

def sign_in_window(parent, stub):
    
    for widget in parent.winfo_children():
        widget.destroy()
    parent.pack_propagate(False)
    
    label = ctk.CTkLabel(parent, text="Sign In Window", font=("Arial Black", 20))
    label.pack(pady=20)
    
    global error_label
    error_label = None

    def add_user(parent, stub):

        for widget in parent.winfo_children():
            widget.destroy()

        parent.pack_propagate(False)

        label = ctk.CTkLabel(parent, text="Create Account", font=("Arial Black", 20))
        label.pack(pady=20)

        user_label = ctk.CTkLabel(parent, text="Username:")
        user_label.pack(pady=5)
        user_entry = ctk.CTkEntry(parent, placeholder_text="Enter username", width=200)
        user_entry.pack(pady=5)

        pass_label1 = ctk.CTkLabel(parent, text="Password:")
        pass_label1.pack(pady=5)
        pass_entry1 = ctk.CTkEntry(parent, placeholder_text="Enter password", show='*', width=200)
        pass_entry1.pack(pady=5)

        pass_label2 = ctk.CTkLabel(parent, text="Confirm password:")
        pass_label2.pack(pady=5)
        pass_entry2 = ctk.CTkEntry(parent, placeholder_text="Re-enter password", show='*', width=200)
        pass_entry2.pack(pady=5)
        
        def register():
            global error_label
            username = user_entry.get()
            password1 = pass_entry1.get()
            password2 = pass_entry2.get()
            if password1 != password2:
                if error_label:
                    error_label.configure(text="Passwords do not match.")
                else:
                    error_label = ctk.CTkLabel(parent, text="Passwords do not match.", text_color="red")
                    error_label.pack(pady=10) 
            else:
                if error_label:
                    error_label.configure(text="")
                response = stub.addUser(real_estate_pb2.addUserRequest(username=username, password=password1))
                new_user = response
                if new_user.username: 
                    error_label = ctk.CTkLabel(parent, text="User created successfully.", text_color="green")
                    error_label.pack(pady=10)
                    parent.after(2000, lambda: sign_in_window(parent, stub))
                else:
                    if error_label:
                        error_label.configure(text=new_user.status_message, text_color="red")
                    else:
                        error_label = ctk.CTkLabel(parent, text=new_user.status_message, text_color="red")
                        error_label.pack(pady=10)

        register_button = ctk.CTkButton(parent, text="Register", corner_radius=10, width=100, command=register)
        register_button.pack(pady=10)

    new_user_button = ctk.CTkButton(parent, text="New User", corner_radius=10, width=100, command=partial(add_user, parent, stub))
    new_user_button.pack(pady=10)

    user_label = ctk.CTkLabel(parent, text="Username:")
    user_label.pack(pady=5)
    user_entry = ctk.CTkEntry(parent, placeholder_text="Enter username", width=200)
    user_entry.pack(pady=5)

    pass_label = ctk.CTkLabel(parent, text="Password:")
    pass_label.pack(pady=5)
    pass_entry = ctk.CTkEntry(parent, placeholder_text="Enter password", show='*', width=200)
    pass_entry.pack(pady=5)

    def do_sign_in():
        #from sample import main
        global error_label
        response = stub.getUser(real_estate_pb2.getUserRequest(username=user_entry.get(), password=pass_entry.get()))
        user = response
        if user.username:
            if error_label:
                error_label.configure(text="Log-In Successful.", text_color="green")
            else:
                error_label = ctk.CTkLabel(parent, text="Log-In Successful.", text_color="green")
                error_label.pack(pady=10)
            #parent.after(2000, lambda: main())
        else:
            if error_label:
                error_label.configure(text=user.status_message, text_color="red")
            else:
                error_label = ctk.CTkLabel(parent, text=user.status_message, text_color="red")
                error_label.pack(pady=10)

    sign_button = ctk.CTkButton(parent, text="Sign In", corner_radius=10, width=100, command=do_sign_in)
    sign_button.pack(pady=10)
