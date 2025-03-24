# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: real_estate.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '',
    'real_estate.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11real_estate.proto\x12\nrealestate\"\xb6\x01\n\x08Property\x12\x13\n\x0bproperty_id\x18\x01 \x01(\t\x12\x15\n\rproperty_name\x18\x02 \x01(\t\x12\x15\n\rproperty_type\x18\x03 \x01(\t\x12\x15\n\rproperty_info\x18\x04 \x01(\t\x12\x18\n\x10price_lease_rent\x18\x05 \x01(\t\x12\x10\n\x08location\x18\x06 \x01(\t\x12\x12\n\nimage_path\x18\x07 \x01(\t\x12\x10\n\x08\x61gent_id\x18\x08 \x01(\t\"\x17\n\x15ListPropertiesRequest\"B\n\x16ListPropertiesResponse\x12(\n\nproperties\x18\x01 \x03(\x0b\x32\x14.realestate.Property\")\n\x12GetPropertyRequest\x12\x13\n\x0bproperty_id\x18\x01 \x01(\t\"=\n\x13GetPropertyResponse\x12&\n\x08property\x18\x01 \x01(\x0b\x32\x14.realestate.Property\"?\n\x15\x43reatePropertyRequest\x12&\n\x08property\x18\x01 \x01(\x0b\x32\x14.realestate.Property\":\n\x16\x43reatePropertyResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\"w\n\x05\x41gent\x12\x10\n\x08\x61gent_id\x18\x01 \x01(\t\x12\x12\n\nagent_name\x18\x02 \x01(\t\x12\x12\n\nagent_info\x18\x03 \x01(\t\x12\x1a\n\x12\x61gent_contact_info\x18\x04 \x01(\t\x12\x18\n\x10\x61gent_image_path\x18\x05 \x01(\t\"\x13\n\x11ListAgentsRequest\"7\n\x12ListAgentsResponse\x12!\n\x06\x61gents\x18\x01 \x03(\x0b\x32\x11.realestate.Agent\"#\n\x0fGetAgentRequest\x12\x10\n\x08\x61gent_id\x18\x01 \x01(\t\"4\n\x10GetAgentResponse\x12 \n\x05\x61gent\x18\x01 \x01(\x0b\x32\x11.realestate.Agent\"6\n\x12\x43reateAgentRequest\x12 \n\x05\x61gent\x18\x01 \x01(\x0b\x32\x11.realestate.Agent\"7\n\x13\x43reateAgentResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\"K\n\x11\x41\x64\x64MessageRequest\x12\x13\n\x0b\x63ustomer_id\x18\x01 \x01(\t\x12\x10\n\x08\x61gent_id\x18\x02 \x01(\t\x12\x0f\n\x07message\x18\x03 \x01(\t\"3\n\x12\x41\x64\x64MessageResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0c\n\x04info\x18\x02 \x01(\t2\xf9\x03\n\x11RealEstateService\x12W\n\x0eListProperties\x12!.realestate.ListPropertiesRequest\x1a\".realestate.ListPropertiesResponse\x12N\n\x0bGetProperty\x12\x1e.realestate.GetPropertyRequest\x1a\x1f.realestate.GetPropertyResponse\x12W\n\x0e\x43reateProperty\x12!.realestate.CreatePropertyRequest\x1a\".realestate.CreatePropertyResponse\x12K\n\nListAgents\x12\x1d.realestate.ListAgentsRequest\x1a\x1e.realestate.ListAgentsResponse\x12\x45\n\x08GetAgent\x12\x1b.realestate.GetAgentRequest\x1a\x1c.realestate.GetAgentResponse\x12N\n\x0b\x43reateAgent\x12\x1e.realestate.CreateAgentRequest\x1a\x1f.realestate.CreateAgentResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'real_estate_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_PROPERTY']._serialized_start=34
  _globals['_PROPERTY']._serialized_end=216
  _globals['_LISTPROPERTIESREQUEST']._serialized_start=218
  _globals['_LISTPROPERTIESREQUEST']._serialized_end=241
  _globals['_LISTPROPERTIESRESPONSE']._serialized_start=243
  _globals['_LISTPROPERTIESRESPONSE']._serialized_end=309
  _globals['_GETPROPERTYREQUEST']._serialized_start=311
  _globals['_GETPROPERTYREQUEST']._serialized_end=352
  _globals['_GETPROPERTYRESPONSE']._serialized_start=354
  _globals['_GETPROPERTYRESPONSE']._serialized_end=415
  _globals['_CREATEPROPERTYREQUEST']._serialized_start=417
  _globals['_CREATEPROPERTYREQUEST']._serialized_end=480
  _globals['_CREATEPROPERTYRESPONSE']._serialized_start=482
  _globals['_CREATEPROPERTYRESPONSE']._serialized_end=540
  _globals['_AGENT']._serialized_start=542
  _globals['_AGENT']._serialized_end=661
  _globals['_LISTAGENTSREQUEST']._serialized_start=663
  _globals['_LISTAGENTSREQUEST']._serialized_end=682
  _globals['_LISTAGENTSRESPONSE']._serialized_start=684
  _globals['_LISTAGENTSRESPONSE']._serialized_end=739
  _globals['_GETAGENTREQUEST']._serialized_start=741
  _globals['_GETAGENTREQUEST']._serialized_end=776
  _globals['_GETAGENTRESPONSE']._serialized_start=778
  _globals['_GETAGENTRESPONSE']._serialized_end=830
  _globals['_CREATEAGENTREQUEST']._serialized_start=832
  _globals['_CREATEAGENTREQUEST']._serialized_end=886
  _globals['_CREATEAGENTRESPONSE']._serialized_start=888
  _globals['_CREATEAGENTRESPONSE']._serialized_end=943
  _globals['_ADDMESSAGEREQUEST']._serialized_start=945
  _globals['_ADDMESSAGEREQUEST']._serialized_end=1020
  _globals['_ADDMESSAGERESPONSE']._serialized_start=1022
  _globals['_ADDMESSAGERESPONSE']._serialized_end=1073
  _globals['_REALESTATESERVICE']._serialized_start=1076
  _globals['_REALESTATESERVICE']._serialized_end=1581
# @@protoc_insertion_point(module_scope)
