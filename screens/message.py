import customtkinter as ctk

# Add messages to DB
def message_window(parent):
    for widget in parent.winfo_children():
        widget.destroy()

    parent.pack_propagate(False)

    label = ctk.CTkLabel(parent, text="Message a User", font=("Arial Black", 20))
    label.pack(pady=20)

    user_label = ctk.CTkLabel(parent, text="Enter username to message:")
    user_label.pack(pady=10)
    user_entry = ctk.CTkEntry(parent, placeholder_text="username", width=200)
    user_entry.pack(pady=5)

    def open_chatroom():
        uname = user_entry.get().strip()
        if uname:
            chatroom_window(parent, uname)

    btn = ctk.CTkButton(parent, text="Open Chat", command=open_chatroom)
    btn.pack(pady=10)


def chatroom_window(parent, username, agent_name="Unknown"):
    for widget in parent.winfo_children():
        widget.destroy()

    parent.pack_propagate(False)

    title_label = ctk.CTkLabel(parent, text=f"Chat with {username}", font=("Arial Black", 24))
    title_label.pack(pady=20)

    chat_frame = ctk.CTkFrame(parent)
    chat_frame.pack(expand=True, fill="both", padx=20, pady=10)

    chat_text = ctk.CTkTextbox(chat_frame, wrap="word")
    chat_text.pack(expand=True, fill="both", padx=10, pady=10)

    entry_frame = ctk.CTkFrame(parent)
    entry_frame.pack(side="bottom", fill="x", pady=10)

    msg_entry = ctk.CTkEntry(entry_frame, placeholder_text="Type a message...")
    msg_entry.pack(side="left", padx=5, pady=5, fill="x", expand=True)

    def send_msg():
        txt = msg_entry.get().strip()
        if txt:
            chat_text.insert("end", f"You: {txt}\n")
            chat_text.see("end")
            msg_entry.delete(0, "end")

    msg_entry.bind("<Return>", lambda e: send_msg())
    send_button = ctk.CTkButton(entry_frame, text="Send", command=send_msg)
    send_button.pack(side="left", padx=5)
