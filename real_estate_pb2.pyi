from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Property(_message.Message):
    __slots__ = ("property_id", "property_name", "property_type", "property_info", "price_lease_rent", "location", "image_path", "agent_id")
    PROPERTY_ID_FIELD_NUMBER: _ClassVar[int]
    PROPERTY_NAME_FIELD_NUMBER: _ClassVar[int]
    PROPERTY_TYPE_FIELD_NUMBER: _ClassVar[int]
    PROPERTY_INFO_FIELD_NUMBER: _ClassVar[int]
    PRICE_LEASE_RENT_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    IMAGE_PATH_FIELD_NUMBER: _ClassVar[int]
    AGENT_ID_FIELD_NUMBER: _ClassVar[int]
    property_id: str
    property_name: str
    property_type: str
    property_info: str
    price_lease_rent: str
    location: str
    image_path: str
    agent_id: str
    def __init__(self, property_id: _Optional[str] = ..., property_name: _Optional[str] = ..., property_type: _Optional[str] = ..., property_info: _Optional[str] = ..., price_lease_rent: _Optional[str] = ..., location: _Optional[str] = ..., image_path: _Optional[str] = ..., agent_id: _Optional[str] = ...) -> None: ...

class ListPropertiesRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListPropertiesResponse(_message.Message):
    __slots__ = ("properties",)
    PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    properties: _containers.RepeatedCompositeFieldContainer[Property]
    def __init__(self, properties: _Optional[_Iterable[_Union[Property, _Mapping]]] = ...) -> None: ...

class GetPropertyRequest(_message.Message):
    __slots__ = ("property_id",)
    PROPERTY_ID_FIELD_NUMBER: _ClassVar[int]
    property_id: str
    def __init__(self, property_id: _Optional[str] = ...) -> None: ...

class GetPropertyResponse(_message.Message):
    __slots__ = ("property",)
    PROPERTY_FIELD_NUMBER: _ClassVar[int]
    property: Property
    def __init__(self, property: _Optional[_Union[Property, _Mapping]] = ...) -> None: ...

class CreatePropertyRequest(_message.Message):
    __slots__ = ("property",)
    PROPERTY_FIELD_NUMBER: _ClassVar[int]
    property: Property
    def __init__(self, property: _Optional[_Union[Property, _Mapping]] = ...) -> None: ...

class CreatePropertyResponse(_message.Message):
    __slots__ = ("success", "message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    def __init__(self, success: bool = ..., message: _Optional[str] = ...) -> None: ...

class Agent(_message.Message):
    __slots__ = ("agent_id", "agent_name", "agent_info", "agent_contact_info", "agent_image_path")
    AGENT_ID_FIELD_NUMBER: _ClassVar[int]
    AGENT_NAME_FIELD_NUMBER: _ClassVar[int]
    AGENT_INFO_FIELD_NUMBER: _ClassVar[int]
    AGENT_CONTACT_INFO_FIELD_NUMBER: _ClassVar[int]
    AGENT_IMAGE_PATH_FIELD_NUMBER: _ClassVar[int]
    agent_id: str
    agent_name: str
    agent_info: str
    agent_contact_info: str
    agent_image_path: str
    def __init__(self, agent_id: _Optional[str] = ..., agent_name: _Optional[str] = ..., agent_info: _Optional[str] = ..., agent_contact_info: _Optional[str] = ..., agent_image_path: _Optional[str] = ...) -> None: ...

class ListAgentsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListAgentsResponse(_message.Message):
    __slots__ = ("agents",)
    AGENTS_FIELD_NUMBER: _ClassVar[int]
    agents: _containers.RepeatedCompositeFieldContainer[Agent]
    def __init__(self, agents: _Optional[_Iterable[_Union[Agent, _Mapping]]] = ...) -> None: ...

class GetAgentRequest(_message.Message):
    __slots__ = ("agent_id",)
    AGENT_ID_FIELD_NUMBER: _ClassVar[int]
    agent_id: str
    def __init__(self, agent_id: _Optional[str] = ...) -> None: ...

class GetAgentResponse(_message.Message):
    __slots__ = ("agent",)
    AGENT_FIELD_NUMBER: _ClassVar[int]
    agent: Agent
    def __init__(self, agent: _Optional[_Union[Agent, _Mapping]] = ...) -> None: ...

class CreateAgentRequest(_message.Message):
    __slots__ = ("agent",)
    AGENT_FIELD_NUMBER: _ClassVar[int]
    agent: Agent
    def __init__(self, agent: _Optional[_Union[Agent, _Mapping]] = ...) -> None: ...

class CreateAgentResponse(_message.Message):
    __slots__ = ("success", "message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    def __init__(self, success: bool = ..., message: _Optional[str] = ...) -> None: ...

class getUserRequest(_message.Message):
    __slots__ = ("username", "password")
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    username: str
    password: str
    def __init__(self, username: _Optional[str] = ..., password: _Optional[str] = ...) -> None: ...

class getUserResponse(_message.Message):
    __slots__ = ("status_message", "username", "password", "chatMessage")
    STATUS_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    CHATMESSAGE_FIELD_NUMBER: _ClassVar[int]
    status_message: str
    username: str
    password: str
    chatMessage: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, status_message: _Optional[str] = ..., username: _Optional[str] = ..., password: _Optional[str] = ..., chatMessage: _Optional[_Iterable[str]] = ...) -> None: ...
