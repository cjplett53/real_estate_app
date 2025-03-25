import grpc
from concurrent import futures
from google.cloud.firestore_v1 import FieldFilter
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

class RealEstateServiceServicer(real_estate_pb2_grpc.RealEstateServiceServicer):
    # Retrieves all property documents from DB
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
                
                # Convert price to string
                price_val = p.get("priceLeaseRent", 0)
                prop.price_lease_rent = str(price_val)
                prop.location = str(p.get("location", ""))
                prop.image_path = str(p.get("imagePath", ""))
                prop.agent_id = str(p.get("agentId", ""))
        except Exception as e:
            print("Error in ListProperties:", e)
            traceback.print_exc()
        return response

    # Retrieves a single property by ID
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

    # Creates properties and adds to DB (Need to add proper images and agent IDs)
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

    # Retrieve agents from DB
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

    # Retrieve a single agent based on ID
    def GetAgent(self, request, context):
        try:
            doc = db.collection("agents").document(request.agent_id).get()
            if not doc.exists:
                return real_estate_pb2.GetAgentResponse()
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
                username=request.username,
            )
        except Exception as e:
            return real_estate_pb2.addUserResponse(status_message="Error creating user.")

    # return valid user upon login
    def getUser(self, request, context):
        docs = db.collection("users").where(filter=FieldFilter("username", "==", request.username)).get()

        if not docs:
            return real_estate_pb2.getUserResponse(status_message="Invalid credentials.")

        doc = docs[0].to_dict()
        
        if doc['username'] == request.username and request.password == doc['password']:
            # Successful login
            response = real_estate_pb2.getUserResponse(
                username=request.username,
                password=request.password,
                chatMessage="",
                status_message="Login Successful"
            )
        else:
            # Failed login
            response = real_estate_pb2.getUserResponse(
                status_message="Invalid password." 
            )
        return response

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
