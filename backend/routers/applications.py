from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, EmailStr
from typing import List, Dict, Any, Optional
from datetime import datetime


router = APIRouter()


class CleanerApplicationCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    dob: str
    experience_years: int = Field(ge=0, le=50)
    skills: List[str] = []
    bio: Optional[str] = None
    facebook_profile: Optional[str] = None


class CleanerApplication(CleanerApplicationCreate):
    id: str
    status: str = Field(default="submitted")
    created_at: datetime


APPLICATIONS: Dict[str, CleanerApplication] = {}


@router.post("/applications", response_model=CleanerApplication)
def create_application(payload: CleanerApplicationCreate) -> CleanerApplication:
    app_id = f"APP-{int(datetime.utcnow().timestamp())}"
    app = CleanerApplication(id=app_id, created_at=datetime.utcnow(), **payload.dict())
    APPLICATIONS[app_id] = app
    return app


@router.get("/applications", response_model=List[CleanerApplication])
def list_applications() -> List[CleanerApplication]:
    return list(APPLICATIONS.values())


@router.get("/applications/{application_id}", response_model=CleanerApplication)
def get_application(application_id: str) -> CleanerApplication:
    if application_id not in APPLICATIONS:
        raise HTTPException(status_code=404, detail="Application not found")
    return APPLICATIONS[application_id]


