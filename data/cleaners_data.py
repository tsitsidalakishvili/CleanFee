import pandas as pd
from datetime import datetime, timedelta
import random

# Sample cleaner data
CLEANERS_DATA = [
    {
        "id": 1,
        "name": "Sarah Johnson",
        "image_url": "https://images.unsplash.com/photo-1494790108755-2616b612b786?w=400&h=400&fit=crop&crop=face",
        "hourly_rate": 25.00,
        "rating": 4.8,
        "total_reviews": 127,
        "bio": "Professional cleaner with 5+ years experience. Specializes in deep cleaning and eco-friendly products.",
        "skills": ["Deep Cleaning", "Eco-friendly", "Pet-friendly", "Move-in/out"],
        "experience_years": 5,
        "verified": True
    },
    {
        "id": 2,
        "name": "Miguel Rodriguez",
        "image_url": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=400&h=400&fit=crop&crop=face",
        "hourly_rate": 22.00,
        "rating": 4.6,
        "total_reviews": 89,
        "bio": "Detail-oriented cleaner who takes pride in making your home spotless. Available evenings and weekends.",
        "skills": ["Detail Cleaning", "Kitchen Deep Clean", "Bathroom Sanitization"],
        "experience_years": 3,
        "verified": True
    },
    {
        "id": 3,
        "name": "Emma Chen",
        "image_url": "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=400&h=400&fit=crop&crop=face",
        "hourly_rate": 28.00,
        "rating": 4.9,
        "total_reviews": 203,
        "bio": "Experienced professional with attention to detail. Brings own supplies and equipment. Flexible scheduling.",
        "skills": ["Premium Service", "Own Equipment", "Flexible Hours", "Post-construction"],
        "experience_years": 7,
        "verified": True
    },
    {
        "id": 4,
        "name": "David Thompson",
        "image_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=400&fit=crop&crop=face",
        "hourly_rate": 20.00,
        "rating": 4.4,
        "total_reviews": 56,
        "bio": "Reliable and efficient cleaner. Great for regular maintenance cleaning. Competitive rates.",
        "skills": ["Regular Maintenance", "Quick Clean", "Budget-friendly"],
        "experience_years": 2,
        "verified": True
    },
    {
        "id": 5,
        "name": "Lisa Park",
        "image_url": "https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=400&h=400&fit=crop&crop=face",
        "hourly_rate": 26.00,
        "rating": 4.7,
        "total_reviews": 142,
        "bio": "Specialized in luxury home cleaning with premium products. Insured and bonded professional.",
        "skills": ["Luxury Cleaning", "Premium Products", "Insured", "Same-day Service"],
        "experience_years": 6,
        "verified": True
    }
]

# Sample reviews for each cleaner
REVIEWS_DATA = {
    1: [
        {"user": "Jennifer M.", "rating": 5, "comment": "Sarah did an amazing job! Very thorough and professional.", "date": "2024-01-15"},
        {"user": "Mike R.", "rating": 5, "comment": "Exceeded expectations. House looked brand new!", "date": "2024-01-10"},
        {"user": "Anna K.", "rating": 4, "comment": "Great service, very reliable. Will book again.", "date": "2024-01-05"},
    ],
    2: [
        {"user": "Tom L.", "rating": 5, "comment": "Miguel is fantastic! Very detail-oriented.", "date": "2024-01-12"},
        {"user": "Sarah W.", "rating": 4, "comment": "Good work, arrived on time and was very polite.", "date": "2024-01-08"},
        {"user": "Chris P.", "rating": 5, "comment": "Excellent deep cleaning of the kitchen. Highly recommend!", "date": "2024-01-03"},
    ],
    3: [
        {"user": "Rachel G.", "rating": 5, "comment": "Emma is the best! Incredible attention to detail.", "date": "2024-01-14"},
        {"user": "David H.", "rating": 5, "comment": "Professional service, brought all equipment. Perfect!", "date": "2024-01-09"},
        {"user": "Maria S.", "rating": 5, "comment": "Outstanding work! House has never been cleaner.", "date": "2024-01-06"},
    ],
    4: [
        {"user": "John D.", "rating": 4, "comment": "Good value for money. Reliable service.", "date": "2024-01-11"},
        {"user": "Lisa T.", "rating": 4, "comment": "David did a good job with regular cleaning.", "date": "2024-01-07"},
        {"user": "Kevin M.", "rating": 5, "comment": "Fast and efficient. Great for weekly maintenance.", "date": "2024-01-02"},
    ],
    5: [
        {"user": "Michelle B.", "rating": 5, "comment": "Lisa provides luxury service! Worth every penny.", "date": "2024-01-13"},
        {"user": "Robert A.", "rating": 5, "comment": "Premium products and exceptional service.", "date": "2024-01-08"},
        {"user": "Amanda C.", "rating": 4, "comment": "High quality cleaning, very professional approach.", "date": "2024-01-04"},
    ]
}

def get_cleaner_availability(cleaner_id, date):
    """Generate random availability for a cleaner on a given date"""
    random.seed(cleaner_id + date.day)  # Consistent availability for same date
    
    available_slots = []
    base_slots = [
        "9:00 AM", "10:00 AM", "11:00 AM", "1:00 PM", 
        "2:00 PM", "3:00 PM", "4:00 PM", "5:00 PM"
    ]
    
    # Randomly select 3-6 available slots
    num_slots = random.randint(3, 6)
    available_slots = random.sample(base_slots, num_slots)
    
    return sorted(available_slots)

def get_cleaners_dataframe():
    """Return cleaners data as pandas DataFrame"""
    return pd.DataFrame(CLEANERS_DATA)

def get_cleaner_reviews(cleaner_id):
    """Get reviews for a specific cleaner"""
    return REVIEWS_DATA.get(cleaner_id, []) 