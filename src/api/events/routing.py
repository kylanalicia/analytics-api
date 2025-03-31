import os
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from src.api.db.session import get_session

from .models import (
    EventModel,
    EventListSchema, 
    EventCreateSchema,
    EventUpdateSchema
)

router = APIRouter()
from ..db.config import DATABASE_URL

# Get data here
# List View
# GET /api/events/
@router.get("/", response_model=EventListSchema)
def read_events(session: Session = Depends(get_session)):
    # a bunch of items in a table
    query = select(EventModel).order_by(EventModel.id.desc()).limit(10)
    results = session.exec(query).all()
    return{
        "results": results,
        "count": len(results)
    }

# SEND DATA HERE!
# create view
# POST /api/events/@router.post("/")
@router.post("/", response_model=EventModel)
def create_events(
    payload: EventCreateSchema, 
    session: Session = Depends(get_session)):
    print(payload.page)
    data = payload.model_dump() # payload -> dict -> pydantic
    obj = EventModel.model_validate(data)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return {"id": 123, **data}


# GET /api/events/12
@router.get("/{event_id}", response_model=EventModel)
def get_event(event_id:int, session: Session = Depends(get_session)): 
    # a single row
    query = select(EventModel).where(EventModel.id == event_id)
    result = session.exec(query).first()
    if not result:
        raise HTTPException(status_code = 404, detail="Eventt not found")
    return result

# Update this data
# PUT /api/events/12
@router.put("/{event_id}")
def update_event(event_id:int, payload:EventUpdateSchema) -> EventModel: 
    # a single row
    data = payload.model_dump()
    return{"id": event_id, **data}

# @router.delete("/{event_id}")
# def get_event(event_id:int) -> EventModel: 
#     # a single row
#     return{"id": event_id}