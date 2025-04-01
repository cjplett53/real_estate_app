import customtkinter as ctk
import real_estate_pb2
import real_estate_pb2_grpc
from google.protobuf import timestamp_pb2
from functools import partial
from datetime import datetime

def message_window(parent, stub, current_user):
    for widget in parent.winfo_children():
        widget.destroy()

    parent.pack_propagate(False)

    title_label = ctk.CTkLabel(parent, text="Message a User", font=("Arial Black", 20))
    title_label.pack(pady=20)

    user_label = ctk.CTkLabel(parent, text="Enter username or agent ID to message:")
    user_label.pack(pady=10)
    user_entry = ctk.CTkEntry(parent, placeholder_text="e.g. bob or A001", width=200)
    user_entry.pack(pady=5)

    error_label = ctk.CTkLabel(parent, text="", text_color="red")
    error_label.pack(pady=5)
    error_label.pack_forget()

    def verify_account_exists(name):
        name = name.strip()
        if not name:
            return (False, "Empty name")

        # Try agent with uppercase
        agent_resp = stub.GetAgent(real_estate_pb2.GetAgentRequest(agent_id=name.upper()))
        if agent_resp.agent.agent_id:
            return (True, "agent", agent_resp.agent.agent_name)

        # Try user (dummy password)
        user_resp = stub.getUser(real_estate_pb2.getUserRequest(username=name, password="dummy"))
        if user_resp.username:
            return (True, "user", user_resp.username)

        return (False, "Account doesn't exist")

    def open_new_chat():
        error_label.pack_forget()
        target = user_entry.get().strip()
        if not (target and current_user and current_user.username):
            return

        verified = verify_account_exists(target)
        if not verified[0]:
            error_label.configure(text=verified[1], text_color="red")
            error_label.pack(pady=5)
            return

        acctType = verified[1]   # "agent" or "user"
        displayName = verified[2]

        sorted_users = sorted([current_user.username.lower(), target.lower()])
        chat_id = f"{sorted_users[0]}_{sorted_users[1]}"
        chatroom_window(parent, stub, current_user, chat_id, acctType, displayName)

    open_button = ctk.CTkButton(parent, text="Open Chat", command=open_new_chat)
    open_button.pack(pady=10)

    # Row of agents
    agent_frame = ctk.CTkFrame(parent)
    agent_frame.pack(fill="x", padx=10, pady=5)

    agent_list_resp = stub.ListAgents(real_estate_pb2.ListAgentsRequest())
    col_idx = 0

    def open_chat_with_agent(agent_id, agent_name):
        if not current_user or not current_user.username:
            return
        sorted_users = sorted([current_user.username.lower(), agent_id.lower()])
        chat_id = f"{sorted_users[0]}_{sorted_users[1]}"
        chatroom_window(parent, stub, current_user, chat_id, "agent", agent_name)

    for ag in agent_list_resp.agents:
        agent_btn = ctk.CTkButton(
            agent_frame,
            text=ag.agent_name,
            corner_radius=10,
            width=80,
            fg_color="#ff8c69",
            hover_color="#ffa07a",
            command=partial(open_chat_with_agent, ag.agent_id, ag.agent_name)
        )
        agent_btn.grid(row=0, column=col_idx, padx=5, pady=5)
        col_idx += 1

    list_frame = ctk.CTkScrollableFrame(parent, width=400, height=300)
    list_frame.pack(pady=20, fill="both", expand=True)

    if current_user and current_user.username:
        resp = stub.ListUserChats(real_estate_pb2.ListUserChatsRequest(username=current_user.username))
        row_idx = 0
        me_lower = current_user.username.lower()

        for chat_info in resp.chats:
            other_name = None
            # If there are exactly 2 participants then find the other
            if len(chat_info.participants) == 2 and me_lower in [p.lower() for p in chat_info.participants]:
                for p in chat_info.participants:
                    if p.lower() != me_lower:
                        other_name = p
                        break
            else:
                other_name = chat_info.chat_id  # fallback

            # See if other_name is agent or user
            if other_name:
                # check agent, use uppercase to fit with DB agent instances
                agent_resp = stub.GetAgent(real_estate_pb2.GetAgentRequest(agent_id=other_name.upper()))
                if agent_resp.agent.agent_id:
                    display_text = agent_resp.agent.agent_name
                else:
                    # check user
                    user_resp = stub.getUser(real_estate_pb2.getUserRequest(username=other_name, password="dummy"))
                    if user_resp.username:
                        display_text = other_name
                    else:
                        display_text = chat_info.chat_id
            else:
                display_text = chat_info.chat_id

            chat_btn = ctk.CTkButton(
                list_frame,
                text=display_text,
                corner_radius=10,
                width=150,
                fg_color="#1f6aa5",
                hover_color="#498daf",
                text_color="white",
                command=partial(chatroom_window, parent, stub, current_user, chat_info.chat_id, None, None)
            )
            chat_btn.grid(row=row_idx, column=0, padx=10, pady=5, sticky="w")
            row_idx += 1

def chatroom_window(parent, stub, current_user, chat_id, acctType=None, displayName=None):
    for widget in parent.winfo_children():
        widget.destroy()
    parent.pack_propagate(False)

    me = (current_user.username.lower() if current_user else "")
    other = None

    # Find the chat doc
    all_chats = stub.ListUserChats(real_estate_pb2.ListUserChatsRequest(username=me))
    chat_found = None
    for cinfo in all_chats.chats:
        if cinfo.chat_id == chat_id:
            chat_found = cinfo
            break

    if chat_found:
        for p in chat_found.participants:
            if p.lower() != me:
                other = p
                break

    # figure out title
    chat_title = f"Chat: {chat_id}"  # fallback
    if acctType and displayName:
        chat_title = f"Chat with {displayName}"
    else:
        if other:
            # check agent
            agent_resp = stub.GetAgent(real_estate_pb2.GetAgentRequest(agent_id=other.upper()))
            if agent_resp.agent.agent_id:
                chat_title = f"Chat with {agent_resp.agent.agent_name}"
            else:
                # check user
                user_resp = stub.getUser(real_estate_pb2.getUserRequest(username=other, password="dummy"))
                if user_resp.username:
                    chat_title = f"Chat with {other}"

    title_label = ctk.CTkLabel(parent, text=chat_title, font=("Arial Black", 24))
    title_label.pack(pady=10)

    # "Back to Messages" button
    def go_back_to_messages():
        from screens.message import message_window
        # Clear the window
        for w in parent.winfo_children():
            w.destroy()
        # Re-show the messaging screen
        message_window(parent, stub, current_user)

    back_btn = ctk.CTkButton(parent, text="Back to Messages", command=go_back_to_messages)
    back_btn.pack(pady=5)

    chat_frame = ctk.CTkFrame(parent)
    chat_frame.pack(expand=True, fill="both", padx=20, pady=10)

    chat_text = ctk.CTkTextbox(chat_frame, wrap="word")
    chat_text.pack(expand=True, fill="both", padx=10, pady=10)

    # Load existing messages
    try:
        resp = stub.ListChatMessages(real_estate_pb2.ListChatMessagesRequest(chat_id=chat_id))
        for msg in resp.messages:
            dt = msg.timestamp.ToDatetime() if msg.timestamp.seconds != 0 else None
            dt_str = dt.strftime("%Y-%m-%d %H:%M:%S") if dt else ""
            line = f"[{dt_str}] {msg.sender}: {msg.text}\n"
            chat_text.insert("end", line)
        chat_text.see("end")
    except Exception as e:
        chat_text.insert("end", f"Error loading messages: {e}\n")

    entry_frame = ctk.CTkFrame(parent)
    entry_frame.pack(side="bottom", fill="x", pady=10)

    msg_entry = ctk.CTkEntry(entry_frame, placeholder_text="Type a message...")
    msg_entry.pack(side="left", padx=5, pady=5, fill="x", expand=True)

    def send_msg():
        txt = msg_entry.get().strip()
        if not txt or not current_user or not current_user.username:
            return
        new_msg = real_estate_pb2.ChatMessage(sender=current_user.username, text=txt)
        send_req = real_estate_pb2.SendMessageRequest(chat_id=chat_id, message=new_msg)
        send_resp = stub.SendMessage(send_req)
        if send_resp.success:
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            chat_text.insert("end", f"[{now_str}] {current_user.username}: {txt}\n")
            chat_text.see("end")
            msg_entry.delete(0, "end")

    msg_entry.bind("<Return>", lambda e: send_msg())
    send_button = ctk.CTkButton(entry_frame, text="Send", command=send_msg)
    send_button.pack(side="left", padx=5)