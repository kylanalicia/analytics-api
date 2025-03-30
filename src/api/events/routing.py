from fastapi import APIRouter
from .schemas import (
    EventSchema,
    EventListSchema, 
    EventCreateSchema,
    EventUpdateSchema
)

router = APIRouter()

# Get data here
# List View
# GET /api/events/
@router.get("/")
def read_events() -> EventListSchema:
    # a bunch of items in a table
    return{
        "results": [
            {"id": 1}, {"id": 2}, {"id": 3}
    ],
    "count": 3
    }

# SEND DATA HERE!
# create view
# POST /api/events/@router.post("/")
@router.post("/")
def create_events(payload: EventCreateSchema) -> EventSchema:
    print(type(payload.page))
    return {"id": 123}


# GET /api/events/12
@router.get("/{event_id}")
def get_event(event_id:int) -> EventSchema: 
    # a single row
    return{"id": event_id}

# Update this data
# PUT /api/events/12
@router.put("/{event_id}")
def update_event(event_id:int, payload:EventUpdateSchema) -> EventSchema: 
    # a single row
    print(payload.description)
    return{"id": event_id}

# @router.delete("/{event_id}")
# def get_event(event_id:int) -> EventSchema: 
#     # a single row
#     return{"id": event_id}