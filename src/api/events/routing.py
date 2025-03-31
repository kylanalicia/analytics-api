import os
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from src.api.db.session import get_session

from .models import (
    EventModel,
    EventListSchema, 
    EventCreateSchema,
    EventUpdateSchema,
    get_utc_now
)

router = APIRouter()
from ..db.config import DATABASE_URL

# Get data here
# List View
# GET /api/events/
@router.get("/", response_model=EventListSchema)
def read_events(session: Session = Depends(get_session)):
    # a bunch of items in a table
    query = select(EventModel).order_by(EventModel.updated_at.asc()).limit(10)
    results = session.exec(query).all()
    return{
        "results": results,
        "count": len(results)
    }

# SEND DATA HERE!
# create view
# POST /api/events/@router.post("/")
@router.post("/", response_model=EventModel)
def create_event(
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
        raise HTTPException(status_code = 404, detail="Event not found")
    return result

# Update this data
# PUT /api/events/12
@router.put("/{event_id}", response_model=EventModel)
def update_event(
    event_id:int, 
    payload:EventUpdateSchema, 
    session: Session = Depends(get_session)): 
    # a single row
    query = select(EventModel).where(EventModel.id == event_id)
    obj = session.exec(query).first()
    if not obj:
        raise HTTPException(status_code = 404, detail="Event not found")
    data = payload.model_dump()
    for k, v in data.items():
        setattr(obj, k, v)

    obj.updated_at = get_utc_now()

    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj

# @router.delete("/{event_id}")
# def get_event(event_id:int) -> EventModel: 
#     # a single row
#     return{"id": event_id}