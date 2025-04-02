import customtkinter as ctk
import real_estate_pb2
import real_estate_pb2_grpc
from google.protobuf import timestamp_pb2
from functools import partial
from datetime import datetime, timezone

def message_window(parent, stub, current_user):
    # Clear the parent
    for widget in parent.winfo_children():
        widget.destroy()
    parent.pack_propagate(False)

    title_label = ctk.CTkLabel(parent, text="Message a User", font=("Arial Black", 20))
    title_label.pack(pady=20)

    user_label = ctk.CTkLabel(parent, text="Enter username or agent ID to message:")
    user_label.pack(pady=10)
    user_entry = ctk.CTkEntry(parent, placeholder_text="Username to message", width=200)
    user_entry.pack(pady=5)

    error_label = ctk.CTkLabel(parent, text="", text_color="red")
    error_label.pack(pady=5)
    error_label.pack_forget()

    def verify_account_exists(name):
        name_stripped = name.strip()
        if not name_stripped:
            return (False, "Empty name", None)

        # Check agent
        agent_resp = stub.GetAgent(
            real_estate_pb2.GetAgentRequest(agent_id=name_stripped.upper())
        )
        if agent_resp.agent.agent_id:
            return (True, "agent", agent_resp.agent.agent_name)

        # Check user
        user_resp = stub.getUser(
            real_estate_pb2.getUserRequest(username=name_stripped, password="dummy")
        )
        if user_resp.username:
            return (True, "user", user_resp.username)

        # Account doesn't exist
        return (False, "Account doesn't exist", None)

    def open_new_chat():
        error_label.pack_forget()
        target = user_entry.get().strip()
        if not (target and current_user and current_user.username):
            return

        found_ok, acct_type, displayName = verify_account_exists(target)
        if not found_ok:
            error_label.configure(text=acct_type, text_color="red")
            error_label.pack(pady=5)
            return

        me_lower = current_user.username.lower()
        target_lower = target.lower()
        sorted_users = sorted([me_lower, target_lower])
        chat_id = f"{sorted_users[0]}_{sorted_users[1]}"

        chatroom_window(parent, stub, current_user, chat_id, acct_type, displayName)

    open_button = ctk.CTkButton(parent, text="Open Chat", command=open_new_chat)
    open_button.pack(pady=10)

    # Horizontal row of agent buttons
    agent_frame = ctk.CTkFrame(parent)
    agent_frame.pack(fill="x", padx=10, pady=5)

    agent_list_resp = stub.ListAgents(real_estate_pb2.ListAgentsRequest())
    col_idx = 0

    def open_chat_with_agent(agent_id, agent_name):
        if not (current_user and current_user.username):
            return
        me_lower = current_user.username.lower()
        a_lower = agent_id.lower()
        sorted_users = sorted([me_lower, a_lower])
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

    # Scrollable list of existing chats
    list_frame = ctk.CTkScrollableFrame(parent, width=400, height=300)
    list_frame.pack(pady=20, fill="both", expand=True)

    if current_user and current_user.username:
        resp_chats = stub.ListUserChats(
            real_estate_pb2.ListUserChatsRequest(username=current_user.username)
        )
        row_idx = 0
        me_lower = current_user.username.lower()

        for chat_info in resp_chats.chats:
            other_name = None
            if len(chat_info.participants) == 2 and me_lower in [p.lower() for p in chat_info.participants]:
                for p in chat_info.participants:
                    if p.lower() != me_lower:
                        other_name = p
                        break
            else:
                other_name = None

            display_text = None
            if other_name:
                # agent check
                agent_resp = stub.GetAgent(
                    real_estate_pb2.GetAgentRequest(agent_id=other_name.upper())
                )
                if agent_resp.agent.agent_id:
                    display_text = agent_resp.agent.agent_name
                else:
                    user_resp = stub.getUser(
                        real_estate_pb2.getUserRequest(username=other_name, password="dummy")
                    )
                    if user_resp.username:
                        display_text = other_name
                    else:
                        display_text = other_name
            if not display_text:
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

    me_lower = current_user.username.lower()
    other = None

    # Find the relevant chat
    all_chats_resp = stub.ListUserChats(
        real_estate_pb2.ListUserChatsRequest(username=me_lower)
    )
    chat_found = None
    if all_chats_resp.chats:
        for cinfo in all_chats_resp.chats:
            if cinfo.chat_id == chat_id:
                chat_found = cinfo
                break

    if chat_found and len(chat_found.participants) == 2:
        for p in chat_found.participants:
            if p.lower() != me_lower:
                other = p
                break

    # Build title
    chat_title = None
    if acctType and displayName:
        chat_title = f"Chat with {displayName}"
    else:
        if other:
            # agent?
            agent_resp = stub.GetAgent(
                real_estate_pb2.GetAgentRequest(agent_id=other.upper())
            )
            if agent_resp.agent.agent_id:
                chat_title = f"Chat with {agent_resp.agent.agent_name}"
            else:
                user_resp = stub.getUser(
                    real_estate_pb2.getUserRequest(username=other, password="dummy")
                )
                if user_resp.username:
                    chat_title = f"Chat with {other}"
                else:
                    chat_title = f"Chat with {other}"

    if not chat_title:
        chat_title = f"Chat: {chat_id}"

    title_label = ctk.CTkLabel(parent, text=chat_title, font=("Arial Black", 24))
    title_label.pack(pady=10)

    def go_back_to_messages():
        from screens.message import message_window
        for w in parent.winfo_children():
            w.destroy()
        message_window(parent, stub, current_user)

    back_btn = ctk.CTkButton(parent, text="Back to Messages", command=go_back_to_messages)
    back_btn.pack(pady=5)

    chat_frame = ctk.CTkFrame(parent)
    chat_frame.pack(expand=True, fill="both", padx=20, pady=10)

    chat_text = ctk.CTkTextbox(chat_frame, wrap="word")
    chat_text.pack(expand=True, fill="both", padx=10, pady=10)

    # Keep track of displayed messages to avoid duplicates
    displayed_messages = set()  # (seconds, nanos, sender, text)

    def load_new_messages():
        try:
            msgs_resp = stub.ListChatMessages(
                real_estate_pb2.ListChatMessagesRequest(chat_id=chat_id)
            )
            new_count = 0
            for msg in msgs_resp.messages:
                # Build a unique ID for each message
                ts_sec = msg.timestamp.seconds
                ts_nanos = msg.timestamp.nanos
                line_id = (ts_sec, ts_nanos, msg.sender, msg.text)

                if line_id not in displayed_messages:
                    displayed_messages.add(line_id)

                    # Convert server UTC to local
                    dt_utc = msg.timestamp.ToDatetime()
                    if dt_utc.tzinfo is None:
                        dt_utc = dt_utc.replace(tzinfo=timezone.utc)
                    dt_local = dt_utc.astimezone()
                    dt_str = dt_local.strftime("%Y-%m-%d %H:%M:%S")

                    line = f"[{dt_str}] {msg.sender}: {msg.text}\n"
                    chat_text.insert("end", line)
                    new_count += 1

            if new_count > 0:
                chat_text.see("end")
        except Exception as e:
            chat_text.insert("end", f"Error loading messages: {e}\n")

    def poll_for_new_messages():
        if parent.winfo_exists():
            load_new_messages()
            parent.after(250, poll_for_new_messages)

    # Initial load + start polling
    load_new_messages()
    poll_for_new_messages()

    # Bottom input area
    entry_frame = ctk.CTkFrame(parent)
    entry_frame.pack(side="bottom", fill="x", pady=10)

    msg_entry = ctk.CTkEntry(entry_frame, placeholder_text="Type a message...")
    msg_entry.pack(side="left", padx=5, pady=5, fill="x", expand=True)

    def send_msg():
        txt = msg_entry.get().strip()
        if not txt:
            return

        new_msg = real_estate_pb2.ChatMessage(sender=current_user.username, text=txt)
        send_req = real_estate_pb2.SendMessageRequest(chat_id=chat_id, message=new_msg)
        send_resp = stub.SendMessage(send_req)
        if send_resp.success:
            msg_entry.delete(0, "end")

    msg_entry.bind("<Return>", lambda e: send_msg())
    send_button = ctk.CTkButton(entry_frame, text="Send", command=send_msg)
    send_button.pack(side="left", padx=5)