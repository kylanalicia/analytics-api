from typing import List, Optional
from pydantic import BaseModel, Field

"""
id
page
description
"""


class EventCreateSchema(BaseModel):
    page:str
    description:Optional[str] = Field(default = "")

class EventUpdateSchema(BaseModel):
    description:str

class EventSchema(BaseModel):
    id:int
    page: Optional[str] = ""
    description: Optional[str] = ""

# {"id": 12}

class EventListSchema(BaseModel):
    results: List[EventSchema]
    count: int