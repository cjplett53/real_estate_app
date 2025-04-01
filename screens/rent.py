import customtkinter as ctk
import real_estate_pb2
import real_estate_pb2_grpc
from PIL import Image, ImageTk

import app_globals

def rent_window(parent, stub):
    for widget in parent.winfo_children():
        widget.destroy()

    parent.pack_propagate(False)

    title_label = ctk.CTkLabel(parent, text="Rent a Property", font=("Arial Black", 20))
    title_label.pack(pady=20)

    response = stub.ListProperties(real_estate_pb2.ListPropertiesRequest())
    all_properties = response.properties

    rent_props = [p for p in all_properties if (p.property_type or "").lower() == "rent"]

    scroll_frame = ctk.CTkScrollableFrame(parent, width=800, height=600)
    scroll_frame.pack(expand=True, fill="both", padx=10, pady=10)

    row_index = 0
    for prop in rent_props:
        frame = ctk.CTkFrame(scroll_frame)
        frame.grid(row=row_index, column=0, padx=10, pady=10, sticky="w")
        row_index += 1

        if prop.image_path:
            try:
                img = Image.open(prop.image_path)
                img = img.resize((120, 80))
                tk_img = ImageTk.PhotoImage(img)
                img_label = ctk.CTkLabel(frame, image=tk_img, text="")
                img_label.image = tk_img
                img_label.pack(side="left", padx=5, pady=5)
            except Exception as e:
                print(f"Could not load image {prop.image_path}: {e}")

        price_str = prop.price_lease_rent or "0"

        info_str = (
            f"Name: {prop.property_name}\n"
            f"Info: {prop.property_info}\n"
            f"Price: {price_str}\n"
            f"Location: {prop.location}\n"
            f"Agent ID: {prop.agent_id}"
        )
        info_label = ctk.CTkLabel(frame, text=info_str, justify="left")
        info_label.pack(side="left", padx=10, pady=5)

        agent_id = prop.agent_id.strip()
        if agent_id:
            get_agent_req = real_estate_pb2.GetAgentRequest(agent_id=agent_id)
            agent_resp = stub.GetAgent(get_agent_req)
            agent_name = agent_resp.agent.agent_name if agent_resp.agent.agent_id else agent_id

            def open_chat_with_agent(aid, aname):
                if not app_globals.is_user_logged_in or not app_globals.current_user or not app_globals.current_user.username:
                    return
                sorted_users = sorted([app_globals.current_user.username.lower(), aid.lower()])
                chat_id = f"{sorted_users[0]}_{sorted_users[1]}"
                from screens.message import message_window, chatroom_window

                parent.pack_forget()
                parent.destroy()

                # open message window
                message_window(parent.master, stub, app_globals.current_user)
                # forcibly open the chat
                chatroom_window(parent.master, stub, app_globals.current_user, chat_id, "agent", aname)

            msg_btn_text = f"Message {agent_name}"
            msg_btn = ctk.CTkButton(
                frame,
                text=msg_btn_text,
                corner_radius=10,
                width=140,
                fg_color="#ff8c69",
                hover_color="#ffa07a",
                text_color="black",
                command=lambda agid=agent_id, aname=agent_name: open_chat_with_agent(agid, aname),
                state="normal" if (app_globals.is_user_logged_in and app_globals.current_user and app_globals.current_user.username) else "disabled"
            )
            msg_btn.pack(side="left", padx=10, pady=5)
