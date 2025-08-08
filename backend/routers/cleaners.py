from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any, Optional

from data.cleaners_data import CLEANERS_DATA, get_cleaners_dataframe, get_cleaner_reviews


router = APIRouter()


@router.get("/cleaners", response_model=List[Dict[str, Any]])
def list_cleaners(
    q: Optional[str] = Query(None, description="Free text search by name or skills"),
    min_rating: Optional[float] = Query(None, ge=0, le=5),
    max_rate: Optional[float] = Query(None, gt=0),
):
    df = get_cleaners_dataframe()
    if q:
        q_lower = q.lower()
        df = df[df.apply(lambda r: q_lower in r["name"].lower() or any(q_lower in s.lower() for s in r["skills"]), axis=1)]
    if min_rating is not None:
        df = df[df["rating"] >= min_rating]
    if max_rate is not None:
        df = df[df["hourly_rate"] <= max_rate]
    return df.to_dict(orient="records")


@router.get("/cleaners/{cleaner_id}", response_model=Dict[str, Any])
def get_cleaner(cleaner_id: int):
    for c in CLEANERS_DATA:
        if c["id"] == cleaner_id:
            return c
    raise HTTPException(status_code=404, detail="Cleaner not found")


@router.get("/cleaners/{cleaner_id}/reviews", response_model=List[Dict[str, Any]])
def list_reviews(cleaner_id: int):
    return get_cleaner_reviews(cleaner_id)


