import customtkinter as ctk

def message_window(parent):
    """
    This window is for entering a username to message.
    Once the username is submitted, it closes this window and opens the chatroom.
    """
    msg_window = ctk.CTkToplevel(parent)
    msg_window.title("Message a User")
    msg_window.geometry("400x300")

    # Make sure it's in front
    msg_window.transient(parent)
    msg_window.grab_set()
    msg_window.lift(parent)
    msg_window.focus_force()

    main_label = ctk.CTkLabel(msg_window, text="Message a User", font=("Arial Black", 20))
    main_label.pack(pady=20)

    instructions_label = ctk.CTkLabel(msg_window, text="Enter the username you want to message:")
    instructions_label.pack(pady=10)

    username_entry = ctk.CTkEntry(msg_window, placeholder_text="Enter username", width=200)
    username_entry.pack(pady=5)

    def open_chatroom():
        username = username_entry.get().strip()
        if username:
            # Close the search window
            msg_window.destroy()
            # Open the full-screen chatroom
            chatroom_window(parent, username)

    # Bind Enter key to open_chatroom
    username_entry.bind("<Return>", lambda event: open_chatroom())

    message_button = ctk.CTkButton(msg_window, text="Message", corner_radius=10, width=100,
                                   command=open_chatroom)
    message_button.pack(pady=10)


def chatroom_window(parent, username, agent_name):
    """
    This window is a full-screen chatroom with the specified user.
    Temporarily stores messages (no DB).
    """

    for widget in parent.winfo_children():
        widget.destroy()

    parent.pack_propagate(False)

    chat_window = parent

    # chat_window = ctk.CTkToplevel(parent)
    # chat_window.title(f"Chatroom with {username}")
    # chat_window.geometry("1200x800")  # Same size as main window

    # # Make sure it's in front
    # chat_window.transient(parent)
    # chat_window.grab_set()
    # chat_window.lift(parent)
    # chat_window.focus_force()

    user_label = ctk.CTkLabel(chat_window, text=f"Chat with: {agent_name} [{username}]", font=("Arial Black", 24))
    user_label.pack(pady=20)

    # Frame for chat messages
    chat_frame = ctk.CTkFrame(chat_window, corner_radius=10)
    chat_frame.pack(expand=True, fill="both", padx=20, pady=10)

    # Textbox to display chat
    chat_text = ctk.CTkTextbox(chat_frame, wrap="word")
    chat_text.pack(expand=True, fill="both", padx=10, pady=10)

    # Frame for message entry
    entry_frame = ctk.CTkFrame(chat_window)
    entry_frame.pack(side="bottom", fill="x", pady=10)

    message_entry = ctk.CTkEntry(entry_frame, placeholder_text="Type a message...")
    message_entry.pack(side="left", padx=5, pady=5, fill="x", expand=True)

    def send_message():
        text = message_entry.get().strip()
        if text:
            # Display the message in the chat_text box
            chat_text.insert("end", f"You: {text}\n")
            chat_text.see("end")  # Auto-scroll
            # Clear the entry
            message_entry.delete(0, "end")

    # Bind Enter key to send message
    message_entry.bind("<Return>", lambda event: send_message())

    send_button = ctk.CTkButton(entry_frame, text="Send", corner_radius=10, width=80, command=send_message)
    send_button.pack(side="left", padx=5)
