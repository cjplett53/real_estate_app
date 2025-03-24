import customtkinter as ctk
import real_estate_pb2

def sign_in_window(parent, stub):
    for widget in parent.winfo_children():
        widget.destroy()

    parent.pack_propagate(False)

    label = ctk.CTkLabel(parent, text="Sign In Window", font=("Arial Black", 20))
    label.pack(pady=20)

    user_label = ctk.CTkLabel(parent, text="Username:")
    user_label.pack(pady=5)
    user_entry = ctk.CTkEntry(parent, placeholder_text="Enter username", width=200)
    user_entry.pack(pady=5)

    pass_label = ctk.CTkLabel(parent, text="Password:")
    pass_label.pack(pady=5)
    pass_entry = ctk.CTkEntry(parent, placeholder_text="Enter password", show='*', width=200)
    pass_entry.pack(pady=5)

    def do_sign_in():
        # purely local until firebase login is implemented
        # print("Username:", user_entry.get())
        # print("Password:", pass_entry.get())

        #verify and reterive user data
        response = stub.getUser(real_estate_pb2.getUserRequest(username=user_entry.get(), password=pass_entry.get()))
        user = response
        print(user)

    sign_button = ctk.CTkButton(parent, text="Sign In", corner_radius=10, width=100, command=do_sign_in)
    sign_button.pack(pady=10)
