from typing import List
from pydantic import BaseModel

"""
id
page
description
"""


class EventCreateSchema(BaseModel):
    page:str

class EventUpdateSchema(BaseModel):
    description:int

class EventSchema(BaseModel):
    id:int

# {"id": 12}

class EventListSchema(BaseModel):
    results: list[EventSchema]
    count: int