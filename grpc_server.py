import grpc
from concurrent import futures
from google.cloud.firestore_v1 import FieldFilter
from google.protobuf import timestamp_pb2
import firebase_admin
from firebase_admin import credentials, firestore
import traceback
import sys
import real_estate_pb2
import real_estate_pb2_grpc

# Initialize Firebase
try:
    firebase_admin.get_app()
except ValueError:
    try:
        cred = credentials.Certificate("realestate-4b2f6-firebase-adminsdk-fbsvc-70c201f38d.json")
        firebase_admin.initialize_app(cred)
    except Exception as e:
        print("Error initializing Firebase:", e)
        traceback.print_exc()
        sys.exit(1)

db = firestore.client()

def _generate_chat_id(userA, userB):
    # Sort the two usernames alphabetically and join them with an underscore so the same chat doc is used for both directions of conversation
    sorted_users = sorted([userA.lower().strip(), userB.lower().strip()])
    return f"{sorted_users[0]}_{sorted_users[1]}"

class RealEstateServiceServicer(real_estate_pb2_grpc.RealEstateServiceServicer):
    def ListUserChats(self, request, context):
        response = real_estate_pb2.ListUserChatsResponse()
        try:
            username = request.username.lower().strip()
            # Query all chat docs that have this username in participants array
            docs = db.collection("chats").where("participants", "array_contains", username).stream()
            for doc in docs:
                doc_dict = doc.to_dict()
                chat_info = response.chats.add()
                chat_info.chat_id = doc.id  # e.g. "bob_ladygaga"
                if "participants" in doc_dict:
                    for p in doc_dict["participants"]:
                        chat_info.participants.append(p)
        except Exception as e:
            print("Error in ListUserChats:", e)
            traceback.print_exc()
        return response

    def ListChatMessages(self, request, context):
        response = real_estate_pb2.ListChatMessagesResponse()
        try:
            chat_id = request.chat_id.strip()
            msgs_ref = (
                db.collection("chats")
                  .document(chat_id)
                  .collection("messages")
                  .order_by("timestamp")
            )
            msgs = msgs_ref.stream()
            for m in msgs:
                msg_dict = m.to_dict()
                cm = response.messages.add()
                cm.sender = msg_dict.get("sender", "")
                cm.text = msg_dict.get("text", "")
                fs_ts = msg_dict.get("timestamp", None)
                if fs_ts:
                    pb_ts = timestamp_pb2.Timestamp()
                    pb_ts.FromDatetime(fs_ts)
                    cm.timestamp.CopyFrom(pb_ts)
        except Exception as e:
            print("Error in ListChatMessages:", e)
            traceback.print_exc()
        return response

    def SendMessage(self, request, context):
        response = real_estate_pb2.SendMessageResponse(success=False, error_message="")
        try:
            chat_id = request.chat_id.strip()
            sender = request.message.sender.strip()
            text = request.message.text.strip()
            if not chat_id or not sender or not text:
                response.error_message = "Missing chat_id, sender or text"
                return response

            chat_ref = db.collection("chats").document(chat_id)
            chat_doc = chat_ref.get()

            if not chat_doc.exists:
                # If doc doesn't exist create participants from chat_id
                parts = chat_id.split("_")
                data = {
                    "participants": parts,
                }
                chat_ref.set(data)

            msg_data = {
                "sender": sender,
                "text": text,
                "timestamp": firestore.SERVER_TIMESTAMP
            }
            chat_ref.collection("messages").add(msg_data)

            response.success = True
        except Exception as e:
            print("Error in SendMessage:", e)
            traceback.print_exc()
            response.error_message = str(e)
        return response

    def ListProperties(self, request, context):
        response = real_estate_pb2.ListPropertiesResponse()
        try:
            docs = db.collection("properties").stream()
            for doc in docs:
                p = doc.to_dict()
                prop = response.properties.add()
                prop.property_id = str(p.get("propertyId", ""))
                prop.property_name = str(p.get("propertyName", ""))
                prop.property_type = str(p.get("propertyType", ""))
                prop.property_info = str(p.get("propertyInfo", ""))
                price_val = p.get("priceLeaseRent", 0)
                prop.price_lease_rent = str(price_val)
                prop.location = str(p.get("location", ""))
                prop.image_path = str(p.get("imagePath", ""))
                prop.agent_id = str(p.get("agentId", ""))
        except Exception as e:
            print("Error in ListProperties:", e)
            traceback.print_exc()
        return response

    def GetProperty(self, request, context):
        try:
            doc = db.collection("properties").document(request.property_id).get()
            if not doc.exists:
                return real_estate_pb2.GetPropertyResponse()
            p = doc.to_dict()
            prop = real_estate_pb2.Property(
                property_id=str(p.get("propertyId", "")),
                property_name=str(p.get("propertyName", "")),
                property_type=str(p.get("propertyType", "")),
                property_info=str(p.get("propertyInfo", "")),
                price_lease_rent=str(p.get("priceLeaseRent", 0)),
                location=str(p.get("location", "")),
                image_path=str(p.get("imagePath", "")),
                agent_id=str(p.get("agentId", ""))
            )
            return real_estate_pb2.GetPropertyResponse(property=prop)
        except Exception as e:
            print("Error in GetProperty:", e)
            traceback.print_exc()
            return real_estate_pb2.GetPropertyResponse()

    def CreateProperty(self, request, context):
        prop = request.property
        try:
            try:
                numeric_price = float(prop.price_lease_rent)
            except ValueError:
                numeric_price = 0.0

            data = {
                "propertyId": prop.property_id,
                "propertyName": prop.property_name,
                "propertyType": prop.property_type,
                "propertyInfo": prop.property_info,
                "priceLeaseRent": numeric_price,
                "location": prop.location,
                "imagePath": prop.image_path,
                "agentId": prop.agent_id
            }
            db.collection("properties").document(prop.property_id).set(data)
            return real_estate_pb2.CreatePropertyResponse(
                success=True,
                message=f"Property '{prop.property_id}' created/updated"
            )
        except Exception as e:
            print("Error in CreateProperty:", e)
            traceback.print_exc()
            return real_estate_pb2.CreatePropertyResponse(success=False, message=str(e))

    def ListAgents(self, request, context):
        response = real_estate_pb2.ListAgentsResponse()
        try:
            docs = db.collection("agents").stream()
            for doc in docs:
                a = doc.to_dict()
                agent = response.agents.add()
                agent.agent_id = str(a.get("agentId", ""))
                agent.agent_name = str(a.get("agentName", ""))
                agent.agent_info = str(a.get("agentInfo", ""))
                agent.agent_contact_info = str(a.get("agentContactInfo", ""))
                agent.agent_image_path = str(a.get("agentImagePath", ""))
        except Exception as e:
            print("Error in ListAgents:", e)
            traceback.print_exc()
        return response

    def GetAgent(self, request, context):
        try:
            doc = db.collection("agents").document(request.agent_id).get()
            if not doc.exists:
                return real_estate_pb2.GetAgentResponse()  # empty
            a = doc.to_dict()
            agent_msg = real_estate_pb2.Agent(
                agent_id=str(a.get("agentId", "")),
                agent_name=str(a.get("agentName", "")),
                agent_info=str(a.get("agentInfo", "")),
                agent_contact_info=str(a.get("agentContactInfo", "")),
                agent_image_path=str(a.get("agentImagePath", ""))
            )
            return real_estate_pb2.GetAgentResponse(agent=agent_msg)
        except Exception as e:
            print("Error in GetAgent:", e)
            traceback.print_exc()
            return real_estate_pb2.GetAgentResponse()

    def CreateAgent(self, request, context):
        ag = request.agent
        try:
            data = {
                "agentId": ag.agent_id,
                "agentName": ag.agent_name,
                "agentInfo": ag.agent_info,
                "agentContactInfo": ag.agent_contact_info,
                "agentImagePath": ag.agent_image_path
            }
            db.collection("agents").document(ag.agent_id).set(data)
            return real_estate_pb2.CreateAgentResponse(
                success=True,
                message=f"Agent '{ag.agent_id}' created/updated"
            )
        except Exception as e:
            print("Error in CreateAgent:", e)
            traceback.print_exc()
            return real_estate_pb2.CreateAgentResponse(success=False, message=str(e))

    def addUser(self, request, context):
        docs = db.collection("users").where(filter=FieldFilter("username", "==", request.username)).get()
        if docs:
            return real_estate_pb2.addUserResponse(status_message="Username already in use.")
        new_user_data = {
            "username": request.username,
            "password": request.password,
        }
        try:
            db.collection("users").add(new_user_data)
            return real_estate_pb2.addUserResponse(
                status_message="User created successfully",
                username=request.username
            )
        except Exception as e:
            print("Error in addUser:", e)
            traceback.print_exc()
            return real_estate_pb2.addUserResponse(status_message="Error creating user.")

    def getUser(self, request, context):
        # If request.password == 'dummy', we only check existence
        docs = db.collection("users").where(filter=FieldFilter("username", "==", request.username)).get()
        if not docs:
            return real_estate_pb2.getUserResponse(status_message="Invalid credentials.")

        doc = docs[0].to_dict()
        if doc['username'] == request.username:
            # If password is 'dummy', we skip the actual password check
            if request.password == "dummy":
                return real_estate_pb2.getUserResponse(
                    status_message="User exists",
                    username=request.username
                )
            else:
                # normal login check
                if request.password == doc['password']:
                    return real_estate_pb2.getUserResponse(
                        username=request.username,
                        password=request.password,
                        status_message="Login Successful"
                    )
                else:
                    return real_estate_pb2.getUserResponse(status_message="Invalid password.")
        else:
            return real_estate_pb2.getUserResponse(status_message="Invalid credentials.")

def gRPC_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    real_estate_pb2_grpc.add_RealEstateServiceServicer_to_server(RealEstateServiceServicer(), server)
    server.add_insecure_port("localhost:4444")
    server.start()
    print("gRPC server running on port 4444.")
    server.wait_for_termination()

if __name__ == "__main__":
    try:
        gRPC_server()
    except Exception as e:
        print("Server encountered an error:", e)
        traceback.print_exc()
