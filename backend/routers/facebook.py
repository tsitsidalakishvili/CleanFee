from fastapi import APIRouter
from typing import Dict, Any, List
import os
import requests


router = APIRouter()


FACEBOOK_PAGE_ID = os.getenv("FACEBOOK_PAGE_ID")
FACEBOOK_ACCESS_TOKEN = os.getenv("FACEBOOK_ACCESS_TOKEN")


@router.get("/facebook/page_info", response_model=Dict[str, Any] | None)
def page_info():
    if not FACEBOOK_PAGE_ID or not FACEBOOK_ACCESS_TOKEN:
        return None
    url = f"https://graph.facebook.com/v18.0/{FACEBOOK_PAGE_ID}"
    params = {
        "access_token": FACEBOOK_ACCESS_TOKEN,
        "fields": "name,followers_count,fan_count,picture,about,website,phone,location",
    }
    r = requests.get(url, params=params, timeout=20)
    return r.json()


@router.get("/facebook/insights", response_model=Dict[str, Any] | None)
def insights():
    if not FACEBOOK_PAGE_ID or not FACEBOOK_ACCESS_TOKEN:
        return None
    url = f"https://graph.facebook.com/v18.0/{FACEBOOK_PAGE_ID}/insights"
    params = {
        "access_token": FACEBOOK_ACCESS_TOKEN,
        "metric": "page_impressions,page_engaged_users,page_fans,page_views_total",
        "period": "day",
    }
    r = requests.get(url, params=params, timeout=20)
    return r.json()


@router.post("/facebook/post", response_model=Dict[str, Any])
def create_post(message: str):
    if not FACEBOOK_PAGE_ID or not FACEBOOK_ACCESS_TOKEN:
        return {"error": "Facebook not configured"}
    url = f"https://graph.facebook.com/v18.0/{FACEBOOK_PAGE_ID}/feed"
    params = {"access_token": FACEBOOK_ACCESS_TOKEN, "message": message}
    r = requests.post(url, params=params, timeout=20)
    return r.json()


