import uuid
import secrets
from pydantic import BaseModel, Field, validator
from typing import Optional, List

class Attachment(BaseModel):
    url: Optional[str]

class Message(BaseModel):
    message: Optional[str]
    attachments: Optional[List[Attachment]]

class Ticket_Id(BaseModel):
    content: Optional[Message] = Field(alias = secrets.token_hex(6))

class Ticket(BaseModel):
    id: str = Field(default_factory = uuid.uuid4, alias = '_id')
    author: int
    ticket_id: List[Ticket_Id]
    @validator('author')
    def author_valid(cls, value):
        if value < 1000:
            raise ValueError('Invalid author ID')

# saved = Ticket(
#     id = uuid.uuid4(),
#     author = 1234,
#     ticket_id = [
#         Ticket_Id(
#             content = Message(
#                 message = 'This is a message',
#                 attachments = [
#                     Attachment(
#                         url = 'https://cdn.discordapp.com/attachments/897953640365568040/1046193612104413265/Icon-App-29x292x.png'
#                     ),
#                     Attachment(
#                         url = 'https://cdn.discordapp.com/attachments/897953640365568040/1046189898966773870/Icon-App-60x602x.png'
#                     )
#                 ]
#             )
#         ),
#         Ticket_Id(
#             content = Message(
#                 message = 'This is another message!!',
#                 attachments = [
#                     Attachment(
#                         url = 'https://cdn.discordapp.com/attachments/897953640365568040/1046193612104413265/Icon-App-29x292x.png'
#                     ),
#                     Attachment(
#                         url = 'https://cdn.discordapp.com/attachments/897953640365568040/1046189898966773870/Icon-App-60x602x.png'
#                     )
#                 ]
#             )
#         )
#     ]
# )

# print(saved)