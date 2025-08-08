from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from datetime import datetime


router = APIRouter()


class BookingCreate(BaseModel):
    cleaner_id: int
    customer_name: str
    customer_phone: str
    address: str
    date: str
    time_slot: str
    notes: str | None = None


class Booking(BaseModel):
    id: str
    created_at: datetime
    status: str = Field(default="pending")
    cleaner_id: int
    customer_name: str
    customer_phone: str
    address: str
    date: str
    time_slot: str
    notes: str | None = None


BOOKINGS: Dict[str, Booking] = {}


@router.get("/bookings", response_model=List[Booking])
def list_bookings() -> List[Booking]:
    return list(BOOKINGS.values())


@router.post("/bookings", response_model=Booking)
def create_booking(payload: BookingCreate) -> Booking:
    booking_id = f"CF-{int(datetime.utcnow().timestamp())}"
    booking = Booking(
        id=booking_id,
        created_at=datetime.utcnow(),
        cleaner_id=payload.cleaner_id,
        customer_name=payload.customer_name.strip(),
        customer_phone=payload.customer_phone.strip(),
        address=payload.address.strip(),
        date=payload.date,
        time_slot=payload.time_slot,
        notes=(payload.notes.strip() if payload.notes else None),
    )
    BOOKINGS[booking_id] = booking
    return booking


@router.get("/bookings/{booking_id}", response_model=Booking)
def get_booking(booking_id: str) -> Booking:
    if booking_id not in BOOKINGS:
        raise HTTPException(status_code=404, detail="Booking not found")
    return BOOKINGS[booking_id]


