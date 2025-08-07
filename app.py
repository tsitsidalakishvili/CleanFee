import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, date
import requests
import json
import os
from data.cleaners_data import (
    get_cleaners_dataframe, 
    get_cleaner_reviews, 
    get_cleaner_availability,
    CLEANERS_DATA
)

# Facebook OAuth configuration
FACEBOOK_APP_ID = st.secrets.get("FACEBOOK_APP_ID", "your_facebook_app_id")
FACEBOOK_APP_SECRET = st.secrets.get("FACEBOOK_APP_SECRET", "your_facebook_app_secret")
REDIRECT_URI = st.secrets.get("REDIRECT_URI", "https://your-app-url.streamlit.app")

# Facebook OAuth functions
def get_facebook_login_url():
    """Generate Facebook OAuth login URL"""
    base_url = "https://www.facebook.com/v18.0/dialog/oauth"
    params = {
        "client_id": FACEBOOK_APP_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": "email,public_profile",
        "response_type": "code",
        "state": "cleanfee_auth"
    }
    
    param_string = "&".join([f"{k}={v}" for k, v in params.items()])
    return f"{base_url}?{param_string}"

def exchange_code_for_token(code):
    """Exchange authorization code for access token"""
    token_url = "https://graph.facebook.com/v18.0/oauth/access_token"
    params = {
        "client_id": FACEBOOK_APP_ID,
        "client_secret": FACEBOOK_APP_SECRET,
        "redirect_uri": REDIRECT_URI,
        "code": code
    }
    
    try:
        response = requests.get(token_url, params=params)
        return response.json()
    except Exception as e:
        st.error(f"Error exchanging code for token: {e}")
        return None

def get_facebook_user_info(access_token):
    """Get user information from Facebook"""
    user_url = "https://graph.facebook.com/v18.0/me"
    params = {
        "access_token": access_token,
        "fields": "id,name,email,picture.type(large),first_name,last_name"
    }
    
    try:
        response = requests.get(user_url, params=params)
        return response.json()
    except Exception as e:
        st.error(f"Error getting user info: {e}")
        return None

def render_facebook_login_button():
    """Render Facebook login button"""
    login_url = get_facebook_login_url()
    
    st.markdown(f"""
    <div style="text-align: center; margin: 1rem 0;">
        <a href="{login_url}" target="_self" style="text-decoration: none;">
            <div style="
                background: linear-gradient(135deg, #1877f2, #42a5f5);
                color: white;
                padding: 0.8rem 2rem;
                border-radius: 25px;
                font-weight: 600;
                font-size: 1rem;
                border: none;
                cursor: pointer;
                transition: all 0.2s ease;
                box-shadow: 0 4px 15px rgba(24, 119, 242, 0.3);
                display: inline-flex;
                align-items: center;
                gap: 0.5rem;
            ">
                <span style="font-size: 1.2rem;">📘</span>
                Continue with Facebook
            </div>
        </a>
    </div>
    """, unsafe_allow_html=True)

# Page configuration
st.set_page_config(
    page_title="CleanFee - Home Cleaning App",
    page_icon="🧹",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Mobile-first CSS for app-like experience
st.markdown("""
<style>
    /* Hide Streamlit branding and menu */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Mobile app container */
    .main {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
    }
    
    .block-container {
        padding: 0.5rem 0.5rem 5rem 0.5rem !important;
        max-width: 100% !important;
    }
    
    /* App header */
    .app-header {
        background: linear-gradient(135deg, #f8f4f0 0%, #e8ddd4 100%);
        color: #5d4e37;
        padding: 1rem 0.5rem;
        margin: -0.5rem -0.5rem 0.5rem -0.5rem;
        text-align: center;
        box-shadow: 0 2px 10px rgba(93, 78, 55, 0.1);
    }
    
    .app-title {
        font-size: 1.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }
    
    .app-subtitle {
        font-size: 0.8rem;
        opacity: 0.9;
        margin: 0.2rem 0 0 0;
    }
    
    /* Mobile cleaner cards */
    .mobile-cleaner-card {
        background: white;
        border-radius: 12px;
        padding: 0.8rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 15px rgba(0,0,0,0.08);
        border: none;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .mobile-cleaner-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.12);
    }
    
    .cleaner-avatar {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        object-fit: cover;
        border: 2px solid #f0f0f0;
    }
    
    .cleaner-info {
        flex: 1;
        margin-left: 0.8rem;
    }
    
    .cleaner-name {
        font-size: 1rem;
        font-weight: 600;
        color: #2c3e50;
        margin: 0 0 0.2rem 0;
    }
    
    .cleaner-rating {
        display: flex;
        align-items: center;
        margin: 0.2rem 0;
    }
    
    .rating-text {
        font-size: 0.75rem;
        color: #666;
        margin-left: 0.3rem;
    }
    
    .cleaner-price {
        font-size: 1.1rem;
        font-weight: 700;
        color: #7a9b76;
        margin: 0.2rem 0;
    }
    
    .cleaner-experience {
        font-size: 0.7rem;
        color: #8a7968;
        background: #f7f5f3;
        padding: 0.2rem 0.5rem;
        border-radius: 10px;
        display: inline-block;
        margin: 0.2rem 0;
    }
    
    /* Mobile skill tags */
    .mobile-skill-tag {
        background: linear-gradient(135deg, #d4c5b9, #c7b299);
        color: #5d4e37;
        padding: 0.2rem 0.5rem;
        border-radius: 12px;
        font-size: 0.65rem;
        margin: 0.1rem 0.2rem 0.1rem 0;
        display: inline-block;
        font-weight: 500;
    }
    
    /* Mobile buttons */
    .mobile-btn {
        background: linear-gradient(135deg, #a8998a, #8f7a67);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.7rem 1.5rem;
        font-weight: 600;
        font-size: 0.9rem;
        width: 100%;
        margin: 0.3rem 0;
        cursor: pointer;
        transition: all 0.2s ease;
        box-shadow: 0 2px 10px rgba(168, 153, 138, 0.3);
    }
    
    .mobile-btn:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 15px rgba(168, 153, 138, 0.4);
    }
    
    .mobile-btn-secondary {
        background: transparent;
        color: #8f7a67;
        border: 2px solid #8f7a67;
        box-shadow: none;
    }
    
    .mobile-btn-secondary:hover {
        background: #8f7a67;
        color: white;
    }
    
    /* Bottom navigation */
    .bottom-nav {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: white;
        border-top: 1px solid #e0e0e0;
        padding: 0.8rem 0 0.5rem 0;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
        z-index: 1000;
    }
    
    .nav-items {
        display: flex;
        justify-content: space-around;
        align-items: center;
        max-width: 600px;
        margin: 0 auto;
        flex-wrap: nowrap;
    }
    
    .nav-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-decoration: none;
        color: #95a5a6;
        transition: color 0.2s ease;
        cursor: pointer;
        padding: 0.2rem 0.1rem;
        min-width: 0;
        flex: 1;
    }
    
    .nav-item.active {
        color: #8f7a67;
    }
    
    .nav-icon {
        font-size: 1.1rem;
        margin-bottom: 0.1rem;
    }
    
    .nav-label {
        font-size: 0.6rem;
        font-weight: 500;
        white-space: nowrap;
    }
    
    /* Mobile forms */
    .mobile-form-group {
        margin: 1rem 0;
    }
    
    .mobile-form-label {
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 0.5rem;
        display: block;
        font-size: 0.9rem;
    }
    
    /* Filter section */
    .filter-section {
        background: white;
        border-radius: 16px;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.06);
    }
    
    .filter-title {
        font-size: 1rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    /* Success messages */
    .mobile-success {
        background: linear-gradient(135deg, #9bb99d, #7a9b76);
        color: white;
        padding: 1rem;
        border-radius: 16px;
        margin: 1rem 0;
        text-align: center;
        font-weight: 500;
        box-shadow: 0 4px 15px rgba(122, 155, 118, 0.3);
    }
    
    /* Review cards */
    .mobile-review-card {
        background: #fdfcfb;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.8rem 0;
        box-shadow: 0 2px 8px rgba(93, 78, 55, 0.06);
        border-left: 4px solid #a8998a;
    }
    
    .review-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
    }
    
    .review-user {
        font-weight: 600;
        color: #2c3e50;
        font-size: 0.9rem;
    }
    
    .review-stars {
        color: #f39c12;
        font-size: 0.9rem;
    }
    
    .review-comment {
        color: #555;
        font-style: italic;
        line-height: 1.4;
        margin: 0.5rem 0;
        font-size: 0.85rem;
    }
    
    .review-date {
        color: #95a5a6;
        font-size: 0.75rem;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .block-container {
            padding: 0.3rem 0.3rem 5rem 0.3rem !important;
        }
        
        .app-header {
            margin: -0.3rem -0.3rem 0.3rem -0.3rem;
            padding: 0.8rem 0.3rem;
        }
        
        .app-title {
            font-size: 1.3rem;
        }
        
        .app-subtitle {
            font-size: 0.75rem;
        }
        
        .mobile-cleaner-card {
            margin: 0.3rem 0;
            padding: 0.6rem;
            border-radius: 10px;
        }
        
        .cleaner-avatar {
            width: 50px;
            height: 50px;
        }
        
        .cleaner-info {
            margin-left: 0.6rem;
        }
        
        .cleaner-name {
            font-size: 0.9rem;
            margin: 0 0 0.1rem 0;
        }
        
        .cleaner-price {
            font-size: 1rem;
            margin: 0.1rem 0;
        }
        
        .rating-text {
            font-size: 0.7rem;
        }
        
        .cleaner-experience {
            font-size: 0.65rem;
            padding: 0.15rem 0.4rem;
            margin: 0.1rem 0;
        }
        
        .mobile-skill-tag {
            font-size: 0.6rem;
            padding: 0.15rem 0.4rem;
            margin: 0.1rem 0.15rem 0.1rem 0;
        }
        
        .stats-card {
            margin: 0.2rem;
            padding: 0.8rem;
        }
        
        .stats-number {
            font-size: 1.5rem;
        }
        
        .stats-label {
            font-size: 0.7rem;
        }
        
        .application-step {
            padding: 1rem;
            margin: 0.5rem 0;
        }
        
        .form-section {
            padding: 1rem;
            margin: 0.5rem 0;
        }
        
        .earning-estimate {
            margin: 0.5rem 0;
            padding: 0.8rem;
        }
        
        .earning-amount {
            font-size: 1.6rem;
        }
        
        .requirement-list {
            margin: 0.5rem 0;
            padding: 0.8rem;
        }
        
        .mobile-review-card {
            margin: 0.5rem 0;
            padding: 0.8rem;
        }
    }
    
    /* Extra small devices (phones in portrait) */
    @media (max-width: 480px) {
        .block-container {
            padding: 0.2rem 0.2rem 5rem 0.2rem !important;
        }
        
        .app-header {
            margin: -0.2rem -0.2rem 0.2rem -0.2rem;
            padding: 0.6rem 0.2rem;
        }
        
        .mobile-cleaner-card {
            margin: 0.2rem 0;
            padding: 0.5rem;
        }
        
        .cleaner-avatar {
            width: 45px;
            height: 45px;
        }
        
        .cleaner-info {
            margin-left: 0.5rem;
        }
        
        .application-step {
            padding: 0.8rem;
            margin: 0.3rem 0;
        }
        
        .bottom-nav {
            padding: 0.5rem 0 0.3rem 0;
        }
        
        .nav-item {
            padding: 0.1rem 0.05rem;
        }
        
        .nav-icon {
            font-size: 1rem;
            margin-bottom: 0.05rem;
        }
        
        .nav-label {
            font-size: 0.55rem;
        }
    }
    
    /* Hide sidebar toggle */
    .css-1d391kg {
        display: none;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #c1c1c1;
        border-radius: 3px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #a8a8a8;
    }
    
    /* Advanced animations and effects */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    @keyframes slideIn {
        from { transform: translateX(-100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    .fade-in {
        animation: fadeInUp 0.6s ease-out;
    }
    
    .pulse-animation {
        animation: pulse 2s infinite;
    }
    
    /* Search and filter enhancements */
    .search-container {
        position: relative;
        margin: 1rem 0;
    }
    
    .search-input {
        width: 100%;
        padding: 0.8rem 2.5rem 0.8rem 1rem;
        border: 2px solid #e0e0e0;
        border-radius: 25px;
        font-size: 1rem;
        background: white;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }
    
    .search-input:focus {
        border-color: #a8998a;
        box-shadow: 0 4px 15px rgba(168, 153, 138, 0.2);
        outline: none;
    }
    
    .search-icon {
        position: absolute;
        right: 1rem;
        top: 50%;
        transform: translateY(-50%);
        color: #a8998a;
        font-size: 1.2rem;
    }
    
    /* Favorite heart animation */
    .heart-icon {
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .heart-icon:hover {
        transform: scale(1.2);
    }
    
    .heart-filled {
        color: #e74c3c;
        animation: pulse 0.5s ease-in-out;
    }
    
    .heart-empty {
        color: #bdc3c7;
    }
    
    /* Notification badge */
    .notification-badge {
        background: linear-gradient(135deg, #d4a574, #c8956d);
        color: white;
        border-radius: 50%;
        width: 20px;
        height: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.7rem;
        font-weight: bold;
        position: absolute;
        top: -5px;
        right: -5px;
        animation: pulse 2s infinite;
    }
    
    /* Advanced card hover effects */
    .mobile-cleaner-card {
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    }
    
    .mobile-cleaner-card:hover {
        transform: translateY(-4px) scale(1.02);
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    }
    
    /* Loading spinner */
    .loading-spinner {
        border: 3px solid #f7f5f3;
        border-top: 3px solid #a8998a;
        border-radius: 50%;
        width: 30px;
        height: 30px;
        animation: spin 1s linear infinite;
        margin: 1rem auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Success checkmark animation */
    .success-checkmark {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: #7a9b76;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 1rem auto;
        animation: scaleIn 0.5s ease-out;
    }
    
    @keyframes scaleIn {
        from { transform: scale(0); }
        to { transform: scale(1); }
    }
    
    /* Enhanced form styling */
    .form-section {
        background: #fdfcfb;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(93, 78, 55, 0.08);
        border-left: 4px solid #a8998a;
    }
    
    .form-section-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Stats cards */
    .stats-card {
        background: linear-gradient(135deg, #d4c5b9, #a8998a);
        color: white;
        border-radius: 16px;
        padding: 1rem;
        text-align: center;
        margin: 0.5rem;
        box-shadow: 0 4px 15px rgba(168, 153, 138, 0.3);
    }
    
    .stats-number {
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
    }
    
    .stats-label {
        font-size: 0.8rem;
        opacity: 0.9;
    }
    
    /* Improved sorting pills */
    .sort-pill {
        background: #f8f9fa;
        border: 2px solid #e9ecef;
        color: #495057;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-size: 0.85rem;
        font-weight: 500;
        margin: 0.2rem;
        cursor: pointer;
        transition: all 0.3s ease;
        display: inline-block;
    }
    
    .sort-pill.active {
        background: linear-gradient(135deg, #a8998a, #8f7a67);
        color: white;
        border-color: #a8998a;
        transform: scale(1.05);
    }
    
    .sort-pill:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    
    /* Cleaner application specific styles */
    .application-step {
        background: #fdfcfb;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(93, 78, 55, 0.08);
        border-left: 4px solid #7a9b76;
    }
    
    .step-header {
        display: flex;
        align-items: center;
        margin-bottom: 1rem;
        font-size: 1.2rem;
        font-weight: 600;
        color: #2c3e50;
    }
    
    .step-number {
        background: linear-gradient(135deg, #7a9b76, #9bb99d);
        color: white;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 1rem;
        font-weight: bold;
    }
    
    .verification-item {
        background: #f8f9fa;
        border: 2px solid #e9ecef;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        display: flex;
        align-items: center;
        justify-content: space-between;
        transition: all 0.3s ease;
    }
    
    .verification-item.verified {
        border-color: #7a9b76;
        background: #e8f5e8;
    }
    
    .verification-item.pending {
        border-color: #d4a574;
        background: #fdf6e8;
    }
    
    .verification-item.failed {
        border-color: #d49999;
        background: #f5e8e8;
    }
    
    .upload-area {
        border: 2px dashed #bdc3c7;
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
        background: #f8f9fa;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .upload-area:hover {
        border-color: #667eea;
        background: #f0f4ff;
    }
    
    .upload-area.dragover {
        border-color: #27ae60;
        background: #d4edda;
    }
    
    .progress-bar {
        width: 100%;
        height: 20px;
        background: #e9ecef;
        border-radius: 10px;
        overflow: hidden;
        margin: 1rem 0;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(135deg, #27ae60, #2ecc71);
        transition: width 0.3s ease;
    }
    
    .requirement-list {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .requirement-item {
        display: flex;
        align-items: center;
        padding: 0.5rem 0;
        font-size: 0.9rem;
    }
    
    .requirement-icon {
        margin-right: 0.5rem;
        font-size: 1rem;
    }
    
    .application-summary {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        text-align: center;
    }
    
    .earning-estimate {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        text-align: center;
    }
    
    .earning-amount {
        font-size: 2rem;
        font-weight: 700;
        color: #27ae60;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'selected_cleaner' not in st.session_state:
    st.session_state.selected_cleaner = None
if 'bookings' not in st.session_state:
    st.session_state.bookings = []
if 'completed_bookings' not in st.session_state:
    st.session_state.completed_bookings = []
if 'favorites' not in st.session_state:
    st.session_state.favorites = []
if 'search_query' not in st.session_state:
    st.session_state.search_query = ""
if 'sort_by' not in st.session_state:
    st.session_state.sort_by = "rating"
if 'notifications' not in st.session_state:
    st.session_state.notifications = []
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {
        'name': '',
        'phone': '',
        'address': '',
        'preferred_time': 'Morning (8AM-12PM)',
        'total_spent': 0,
        'total_bookings': 0
    }
if 'cleaner_applications' not in st.session_state:
    st.session_state.cleaner_applications = []
if 'application_status' not in st.session_state:
    st.session_state.application_status = None  # None, 'pending', 'approved', 'rejected'
if 'current_application' not in st.session_state:
    st.session_state.current_application = {}
if 'application_step' not in st.session_state:
    st.session_state.application_step = 1
if 'facebook_user' not in st.session_state:
    st.session_state.facebook_user = None
if 'facebook_authenticated' not in st.session_state:
    st.session_state.facebook_authenticated = False

# Handle Facebook OAuth callback
def handle_facebook_callback():
    """Handle Facebook OAuth callback"""
    query_params = st.query_params
    
    if "code" in query_params and "state" in query_params:
        code = query_params["code"]
        state = query_params["state"]
        
        if state == "cleanfee_auth":
            # Exchange code for token
            token_data = exchange_code_for_token(code)
            
            if token_data and "access_token" in token_data:
                # Get user info
                user_info = get_facebook_user_info(token_data["access_token"])
                
                if user_info:
                    st.session_state.facebook_user = user_info
                    st.session_state.facebook_authenticated = True
                    
                    # Pre-fill application with Facebook data
                    st.session_state.current_application.update({
                        'first_name': user_info.get('first_name', ''),
                        'last_name': user_info.get('last_name', ''),
                        'email': user_info.get('email', ''),
                        'facebook_id': user_info.get('id', ''),
                        'profile_picture': user_info.get('picture', {}).get('data', {}).get('url', '')
                    })
                    
                    # Clear query params and redirect to cleaner application
                    st.query_params.clear()
                    st.session_state.page = "become_cleaner"
                    st.rerun()

# Call callback handler
handle_facebook_callback()

def display_star_rating(rating):
    """Display star rating"""
    full_stars = int(rating)
    half_star = 1 if rating - full_stars >= 0.5 else 0
    empty_stars = 5 - full_stars - half_star
    
    stars = "⭐" * full_stars + "⭐" * half_star + "☆" * empty_stars
    return f"{stars} ({rating:.1f})"

def display_mobile_cleaner_card(cleaner):
    """Display an enhanced mobile-optimized cleaner card"""
    # Check if cleaner is in favorites
    is_favorite = cleaner['id'] in st.session_state.favorites
    heart_icon = "❤️" if is_favorite else "🤍"
    heart_class = "heart-filled" if is_favorite else "heart-empty"
    
    # Availability status
    availability_status = "🟢 Available Today" if cleaner['id'] % 2 == 0 else "🟡 Busy Today"
    
    stars = "⭐" * int(cleaner['rating'])
    skills_html = " ".join([f'<span class="mobile-skill-tag">{skill}</span>' for skill in cleaner['skills']])
    
    card_html = f"""
    <div class="mobile-cleaner-card fade-in">
        <div style="display: flex; align-items: flex-start; position: relative;">
            <img src="{cleaner['image_url']}" class="cleaner-avatar" alt="{cleaner['name']}">
            <div class="cleaner-info" style="flex: 1;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div class="cleaner-name">{cleaner['name']}</div>
                    <div class="heart-icon {heart_class}" onclick="toggleFavorite({cleaner['id']})" style="font-size: 1.5rem; cursor: pointer;">
                        {heart_icon}
                    </div>
                </div>
                <div class="cleaner-rating">
                    <span class="review-stars">{stars}</span>
                    <span class="rating-text">({cleaner['rating']:.1f}) • {cleaner['total_reviews']} reviews</span>
                </div>
                <div class="cleaner-price">${cleaner['hourly_rate']:.2f}/hour</div>
                <div class="cleaner-experience">{cleaner['experience_years']} years experience</div>
                <div style="font-size: 0.75rem; color: #27ae60; font-weight: 500; margin-top: 0.3rem;">
                    {availability_status}
                </div>
            </div>
        </div>
        <div style="margin-top: 0.8rem;">
            <div style="font-size: 0.85rem; color: #555; margin-bottom: 0.5rem;">{cleaner['bio']}</div>
            <div>{skills_html}</div>
        </div>
    </div>
    """
    
    st.markdown(card_html, unsafe_allow_html=True)
    
    # Enhanced mobile buttons with icons
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        if st.button(f"📅 Book Now", key=f"select_{cleaner['id']}", help="Book this cleaner", use_container_width=True):
            st.session_state.selected_cleaner = cleaner.to_dict()
            st.session_state.page = 'booking'
            st.rerun()
    
    with col2:
        if st.button(f"⭐ Reviews", key=f"reviews_{cleaner['id']}", help="View reviews", use_container_width=True):
            st.session_state.selected_cleaner = cleaner.to_dict()
            st.session_state.page = 'reviews'
            st.rerun()
    
    with col3:
        # Favorite toggle button
        fav_label = "💖" if is_favorite else "🤍"
        if st.button(fav_label, key=f"fav_{cleaner['id']}", help="Add to favorites"):
            if is_favorite:
                st.session_state.favorites.remove(cleaner['id'])
                st.success("Removed from favorites!")
            else:
                st.session_state.favorites.append(cleaner['id'])
                st.success("Added to favorites!")
            st.rerun()

def home_page():
    """Display the enhanced mobile-optimized home page"""
    # Mobile app header with notifications
    notification_count = len(st.session_state.notifications)
    notification_badge = f'<div class="notification-badge">{notification_count}</div>' if notification_count > 0 else ''
    
    st.markdown(f"""
    <div class="app-header">
        <div class="app-title">🧹 CleanFee</div>
        <div class="app-subtitle">Professional Home Cleaning</div>
        <div style="position: absolute; top: 1rem; right: 1rem;">
            <span style="position: relative; font-size: 1.5rem;">🔔{notification_badge}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # User stats dashboard (compact on mobile)
    total_spent = st.session_state.user_profile['total_spent']
    total_bookings = len(st.session_state.bookings) + len(st.session_state.completed_bookings)
    favorite_count = len(st.session_state.favorites)
    
    if total_bookings > 0 or favorite_count > 0:
        col1, col2, col3 = st.columns(3, gap="small")
        with col1:
            st.markdown(f"""
            <div class="stats-card">
                <div class="stats-number">{total_bookings}</div>
                <div class="stats-label">Total Bookings</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="stats-card">
                <div class="stats-number">${total_spent:.0f}</div>
                <div class="stats-label">Total Spent</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="stats-card">
                <div class="stats-number">{favorite_count}</div>
                <div class="stats-label">Favorites</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Advanced search bar (compact)
    search_query = st.text_input("🔍 Search cleaners", 
                                placeholder="Search by name, skills, or experience...", 
                                key="search_cleaners")
    
    # Sort options with pills
    st.markdown("**Sort by:**")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("⭐ Rating", key="sort_rating", use_container_width=True):
            st.session_state.sort_by = "rating"
    with col2:
        if st.button("💰 Price", key="sort_price", use_container_width=True):
            st.session_state.sort_by = "price"
    with col3:
        if st.button("🎯 Experience", key="sort_exp", use_container_width=True):
            st.session_state.sort_by = "experience"
    with col4:
        if st.button("📝 Reviews", key="sort_reviews", use_container_width=True):
            st.session_state.sort_by = "reviews"
    
    # Advanced filters section
    with st.expander("🔧 Advanced Filters", expanded=False):
        st.markdown('<div class="filter-title">Customize Your Search</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            price_range = st.slider("💰 Hourly Rate", 15, 35, (15, 35), 1, help="Set your budget range")
            min_rating = st.slider("⭐ Minimum Rating", 1.0, 5.0, 4.0, 0.1, help="Filter by rating")
        
        with col2:
            experience_filter = st.selectbox("🎯 Experience Level", [0, 2, 5, 7], index=0, 
                                            format_func=lambda x: f"{x}+ years" if x > 0 else "Any experience")
            
            skill_filter = st.multiselect("🛠️ Required Skills", 
                                        ["Deep Cleaning", "Eco-friendly", "Pet-friendly", "Move-in/out", 
                                         "Kitchen Deep Clean", "Premium Service", "Same-day Service"])
        
        availability_filter = st.selectbox("📅 Availability", 
                                         ["Any time", "Available Today", "Available This Week"])
        
        # Favorites only toggle
        favorites_only = st.checkbox("💖 Show Favorites Only")
    
    # Get and filter cleaners
    cleaners_df = get_cleaners_dataframe()
    
    # Apply search filter
    if search_query:
        mask = (
            cleaners_df['name'].str.contains(search_query, case=False, na=False) |
            cleaners_df['bio'].str.contains(search_query, case=False, na=False) |
            cleaners_df['skills'].astype(str).str.contains(search_query, case=False, na=False)
        )
        cleaners_df = cleaners_df[mask]
    
    # Apply other filters
    filtered_cleaners = cleaners_df[
        (cleaners_df['hourly_rate'] >= price_range[0]) &
        (cleaners_df['hourly_rate'] <= price_range[1]) &
        (cleaners_df['rating'] >= min_rating) &
        (cleaners_df['experience_years'] >= experience_filter)
    ]
    
    # Apply skill filter
    if skill_filter:
        skill_mask = filtered_cleaners['skills'].apply(
            lambda skills: any(skill in skills for skill in skill_filter)
        )
        filtered_cleaners = filtered_cleaners[skill_mask]
    
    # Apply favorites filter
    if favorites_only:
        filtered_cleaners = filtered_cleaners[filtered_cleaners['id'].isin(st.session_state.favorites)]
    
    # Apply sorting
    if st.session_state.sort_by == "rating":
        filtered_cleaners = filtered_cleaners.sort_values('rating', ascending=False)
    elif st.session_state.sort_by == "price":
        filtered_cleaners = filtered_cleaners.sort_values('hourly_rate', ascending=True)
    elif st.session_state.sort_by == "experience":
        filtered_cleaners = filtered_cleaners.sort_values('experience_years', ascending=False)
    elif st.session_state.sort_by == "reviews":
        filtered_cleaners = filtered_cleaners.sort_values('total_reviews', ascending=False)
    
    # Results count with emoji and filters applied
    filter_info = []
    if search_query:
        filter_info.append(f"matching '{search_query}'")
    if favorites_only:
        filter_info.append("favorites")
    if skill_filter:
        filter_info.append(f"with {', '.join(skill_filter)}")
    
    filter_text = f" ({', '.join(filter_info)})" if filter_info else ""
    
    st.markdown(f"""
    <div style="text-align: center; padding: 1rem 0; font-size: 1.1rem; font-weight: 600; color: #2c3e50;">
        👥 {len(filtered_cleaners)} Professional Cleaners Available{filter_text}
    </div>
    """, unsafe_allow_html=True)
    
    # No results message
    if len(filtered_cleaners) == 0:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; color: #7f8c8d;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🔍</div>
            <div style="font-size: 1.2rem; font-weight: 600; margin-bottom: 0.5rem;">No cleaners found</div>
            <div>Try adjusting your filters or search terms</div>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Display mobile cleaner cards with loading animation
    for i, (_, cleaner) in enumerate(filtered_cleaners.iterrows()):
        # Add small delay effect for animation
        if i < 3:  # Only animate first 3 cards
            st.markdown(f'<div class="fade-in" style="animation-delay: {i*0.1}s;"></div>', unsafe_allow_html=True)
        display_mobile_cleaner_card(cleaner)

def booking_page():
    """Display mobile-optimized booking page"""
    if st.session_state.selected_cleaner is None:
        st.error("No cleaner selected. Please go back to home page.")
        return
    
    cleaner = st.session_state.selected_cleaner
    
    # Mobile header
    st.markdown(f"""
    <div class="app-header">
        <div class="app-title">📅 Book Service</div>
        <div class="app-subtitle">{cleaner['name']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Back button
    if st.button("← Back to Cleaners", key="back_to_home"):
        st.session_state.page = 'home'
        st.rerun()
    
    # Cleaner summary card
    st.markdown(f"""
    <div style="background: white; border-radius: 16px; padding: 1rem; margin: 1rem 0; box-shadow: 0 2px 8px rgba(0,0,0,0.06);">
        <div style="display: flex; align-items: center;">
            <img src="{cleaner['image_url']}" style="width: 60px; height: 60px; border-radius: 50%; object-fit: cover; margin-right: 1rem;">
            <div>
                <div style="font-weight: 600; color: #2c3e50; font-size: 1.1rem;">{cleaner['name']}</div>
                <div style="color: #f39c12;">{'⭐' * int(cleaner['rating'])} ({cleaner['rating']:.1f})</div>
                <div style="color: #27ae60; font-weight: 600; font-size: 1.2rem;">${cleaner['hourly_rate']:.2f}/hour</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Mobile booking form
    st.markdown('<div class="mobile-form-label">📅 Select Date</div>', unsafe_allow_html=True)
    selected_date = st.date_input(
        "",
        min_value=date.today(),
        max_value=date.today() + timedelta(days=30)
    )
    
    # Get availability for selected date
    available_slots = get_cleaner_availability(cleaner['id'], selected_date)
    
    if available_slots:
        st.markdown('<div class="mobile-form-label">⏰ Available Time Slots</div>', unsafe_allow_html=True)
        selected_time = st.selectbox("", available_slots)
        
        st.markdown('<div class="mobile-form-label">⏱️ Cleaning Duration</div>', unsafe_allow_html=True)
        duration = st.selectbox("", [1, 2, 3, 4, 5], index=1, format_func=lambda x: f"{x} hour{'s' if x != 1 else ''}")
        
        st.markdown('<div class="mobile-form-label">➕ Additional Services (optional)</div>', unsafe_allow_html=True)
        services = st.multiselect(
            "",
            ["Deep Cleaning (+$10/hr)", "Inside Oven (+$15)", "Inside Fridge (+$15)", 
             "Window Cleaning (+$20)", "Garage Cleaning (+$25)"]
        )
        
        # Calculate total cost
        base_cost = cleaner['hourly_rate'] * duration
        additional_cost = len(services) * 15  # Simplified additional cost
        total_cost = base_cost + additional_cost
        
        # Cost breakdown
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; border-radius: 16px; padding: 1rem; margin: 1rem 0; text-align: center;">
            <div style="font-size: 1.1rem; margin-bottom: 0.5rem;">Total Cost</div>
            <div style="font-size: 2rem; font-weight: 700;">${total_cost:.2f}</div>
            <div style="font-size: 0.85rem; opacity: 0.9;">Base: ${base_cost:.2f} + Add-ons: ${additional_cost:.2f}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Customer details
        st.markdown('<div class="mobile-form-label">👤 Contact Information</div>', unsafe_allow_html=True)
        customer_name = st.text_input("Your Name", placeholder="Enter your full name")
        customer_phone = st.text_input("Phone Number", placeholder="Your phone number")
        customer_address = st.text_area("Address", placeholder="Your complete address")
        special_instructions = st.text_area("Special Instructions (optional)", placeholder="Any special requests or instructions...")
        
        # Mobile booking button
        if st.button("🎉 Confirm Booking", type="primary", use_container_width=True):
            # Validate required fields
            missing_fields = []
            if not customer_name.strip():
                missing_fields.append("Name")
            if not customer_phone.strip():
                missing_fields.append("Phone Number")
            if not customer_address.strip():
                missing_fields.append("Address")
            
            if not missing_fields:
                booking = {
                    'id': len(st.session_state.bookings) + len(st.session_state.completed_bookings) + 1,
                    'cleaner_id': cleaner['id'],
                    'cleaner_name': cleaner['name'],
                    'cleaner_image': cleaner['image_url'],
                    'date': selected_date.strftime('%Y-%m-%d'),
                    'time': selected_time,
                    'duration': duration,
                    'services': services,
                    'total_cost': total_cost,
                    'customer_name': customer_name.strip(),
                    'customer_phone': customer_phone.strip(),
                    'customer_address': customer_address.strip(),
                    'special_instructions': special_instructions.strip(),
                    'status': 'confirmed',
                    'booking_date': datetime.now().strftime('%Y-%m-%d %H:%M'),
                    'estimated_completion': (datetime.now() + timedelta(hours=duration)).strftime('%H:%M')
                }
                
                st.session_state.bookings.append(booking)
                
                # Update user profile
                st.session_state.user_profile['total_spent'] += total_cost
                st.session_state.user_profile['total_bookings'] += 1
                if not st.session_state.user_profile['name']:
                    st.session_state.user_profile.update({
                        'name': customer_name.strip(),
                        'phone': customer_phone.strip(),
                        'address': customer_address.strip()
                    })
                
                # Add notification
                notification = {
                    'id': len(st.session_state.notifications) + 1,
                    'type': 'booking_confirmed',
                    'title': 'Booking Confirmed! 🎉',
                    'message': f'Your cleaning with {cleaner["name"]} is scheduled for {selected_date.strftime("%B %d")} at {selected_time}',
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M'),
                    'read': False
                }
                st.session_state.notifications.append(notification)
                
                # Mobile success message
                st.markdown(f"""
                <div class="mobile-success">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">🎉</div>
                    <div style="font-size: 1.2rem; font-weight: 600; margin-bottom: 1rem;">Booking Confirmed!</div>
                    <div style="text-align: left; background: rgba(255,255,255,0.2); border-radius: 12px; padding: 1rem;">
                        <div><strong>Cleaner:</strong> {cleaner['name']}</div>
                        <div><strong>Date:</strong> {selected_date.strftime('%B %d, %Y')}</div>
                        <div><strong>Time:</strong> {selected_time}</div>
                        <div><strong>Duration:</strong> {duration} hour{'s' if duration != 1 else ''}</div>
                        <div><strong>Total:</strong> ${total_cost:.2f}</div>
                        <div><strong>Booking ID:</strong> #{booking['id']:03d}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            else:
                st.error(f"Please fill in: {', '.join(missing_fields)}")
    else:
        st.warning("⚠️ No available slots for this date. Please select another date.")

def reviews_page():
    """Display mobile-optimized reviews page"""
    if st.session_state.selected_cleaner is None:
        st.error("No cleaner selected.")
        return
    
    cleaner = st.session_state.selected_cleaner
    
    # Mobile header with back button
    st.markdown(f"""
    <div class="app-header">
        <div class="app-title">⭐ Reviews</div>
        <div class="app-subtitle">{cleaner['name']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Back button
    if st.button("← Back to Cleaners", key="back_to_cleaners"):
        st.session_state.page = 'home'
        st.rerun()
    
    reviews = get_cleaner_reviews(cleaner['id'])
    
    # Overall rating summary
    stars = "⭐" * int(cleaner['rating'])
    st.markdown(f"""
    <div style="text-align: center; padding: 1rem; background: white; border-radius: 16px; margin: 1rem 0; box-shadow: 0 2px 8px rgba(0,0,0,0.06);">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">{stars}</div>
        <div style="font-size: 1.2rem; font-weight: 600; color: #2c3e50;">{cleaner['rating']:.1f} out of 5</div>
        <div style="color: #666; font-size: 0.9rem;">Based on {len(reviews)} reviews</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Mobile review cards
    for review in reviews:
        st.markdown(f"""
        <div class="mobile-review-card">
            <div class="review-header">
                <span class="review-user">{review['user']}</span>
                <span class="review-stars">{'⭐' * review['rating']}</span>
            </div>
            <div class="review-comment">"{review['comment']}"</div>
            <div class="review-date">{review['date']}</div>
        </div>
        """, unsafe_allow_html=True)

def my_bookings_page():
    """Display mobile-optimized bookings page"""
    # Mobile header
    st.markdown("""
    <div class="app-header">
        <div class="app-title">📅 My Bookings</div>
        <div class="app-subtitle">Track your cleaning services</div>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.bookings and not st.session_state.completed_bookings:
        st.info("No bookings yet. Book a cleaner from the home page!")
        return
    
    # Tabs for different booking statuses
    tab1, tab2 = st.tabs(["📅 Upcoming Bookings", "✅ Completed Bookings"])
    
    with tab1:
        if st.session_state.bookings:
            for booking in st.session_state.bookings:
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.markdown(f"**#{booking['id']:03d} - {booking['cleaner_name']}**")
                    st.markdown(f"📅 {booking['date']} at {booking['time']}")
                    st.markdown(f"⏱️ {booking['duration']} hour(s)")
                    st.markdown(f"💰 ${booking['total_cost']:.2f}")
                
                with col2:
                    st.markdown(f"**Status:** {booking['status'].title()}")
                    st.markdown(f"**Booked:** {booking['booking_date']}")
                
                with col3:
                    if st.button(f"Mark as Completed", key=f"complete_{booking['id']}"):
                        booking['status'] = 'completed'
                        st.session_state.completed_bookings.append(booking)
                        st.session_state.bookings.remove(booking)
                        st.rerun()
                
                st.markdown("---")
        else:
            st.info("No upcoming bookings.")
    
    with tab2:
        if st.session_state.completed_bookings:
            for booking in st.session_state.completed_bookings:
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**#{booking['id']:03d} - {booking['cleaner_name']}**")
                    st.markdown(f"📅 {booking['date']} at {booking['time']}")
                    st.markdown(f"💰 ${booking['total_cost']:.2f}")
                
                with col2:
                    if 'user_rating' not in booking:
                        st.markdown("**Rate this service:**")
                        rating = st.selectbox(
                            "Rating", 
                            options=[1, 2, 3, 4, 5],
                            key=f"rating_{booking['id']}",
                            format_func=lambda x: f"{x} Star{'s' if x != 1 else ''}"
                        )
                        comment = st.text_area(
                            "Comment (optional)", 
                            key=f"comment_{booking['id']}",
                            height=100
                        )
                        
                        if st.button(f"Submit Rating", key=f"submit_rating_{booking['id']}"):
                            booking['user_rating'] = rating
                            booking['user_comment'] = comment
                            st.success("Thank you for your feedback!")
                            st.rerun()
                    else:
                        st.markdown(f"**Your Rating:** {'⭐' * booking['user_rating']}")
                        if booking.get('user_comment'):
                            st.markdown(f"**Your Comment:** {booking['user_comment']}")
                
                st.markdown("---")
        else:
            st.info("No completed bookings yet.")

# Mobile bottom navigation
def render_bottom_nav():
    """Render mobile bottom navigation"""
    current_page = st.session_state.page
    
    nav_html = f"""
    <div class="bottom-nav">
        <div class="nav-items">
            <div class="nav-item {'active' if current_page == 'home' else ''}" onclick="setPage('home')">
                <div class="nav-icon">🏠</div>
                <div class="nav-label">Home</div>
            </div>
            <div class="nav-item {'active' if current_page == 'bookings' else ''}" onclick="setPage('bookings')">
                <div class="nav-icon">📅</div>
                <div class="nav-label">Bookings</div>
            </div>
            <div class="nav-item">
                <div class="nav-icon">💬</div>
                <div class="nav-label">Support</div>
            </div>
            <div class="nav-item">
                <div class="nav-icon">👤</div>
                <div class="nav-label">Profile</div>
            </div>
        </div>
    </div>
    
    <script>
    function setPage(page) {{
        window.parent.postMessage({{type: 'setPage', page: page}}, '*');
    }}
    </script>
    """
    
    st.markdown(nav_html, unsafe_allow_html=True)

# Enhanced Navigation with new features
col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1:
    if st.button("🏠", key="nav_home", help="Home", use_container_width=True):
        st.session_state.page = "home"
        st.rerun()
with col2:
    if st.button("📋", key="nav_bookings", help="My Bookings", use_container_width=True):
        st.session_state.page = "bookings"
        st.rerun()
with col3:
    # Notifications with badge
    notification_count = len([n for n in st.session_state.notifications if not n['read']])
    notif_label = f"🔔" if notification_count > 0 else "🔔"
    if st.button(notif_label, key="nav_notifications", help="Notifications", use_container_width=True):
        st.session_state.page = "notifications"
        st.rerun()
with col4:
    # Favorites
    if st.button("⭐", key="nav_favorites", help="Favorites", use_container_width=True):
        st.session_state.page = "favorites"
        st.rerun()
with col5:
    # Become a Cleaner
    if st.button("🧹", key="nav_become_cleaner", help="Become a Cleaner", use_container_width=True):
        st.session_state.page = "become_cleaner"
        st.rerun()
with col6:
    if st.button("👤", key="nav_profile", help="Profile", use_container_width=True):
        st.session_state.page = "profile"
        st.rerun()

# Style the navigation buttons for mobile
st.markdown("""
<style>
    /* Navigation button styling */
    .stButton > button {
        height: 2.5rem !important;
        width: 100% !important;
        font-size: 1rem !important;
        padding: 0.2rem !important;
        border-radius: 8px !important;
        border: none !important;
        background-color: transparent !important;
        color: #95a5a6 !important;
        transition: all 0.2s ease !important;
    }
    
    .stButton > button:hover {
        background-color: rgba(143, 122, 103, 0.1) !important;
        color: #8f7a67 !important;
        transform: scale(1.05) !important;
    }
    
    .stButton > button:focus {
        background-color: rgba(143, 122, 103, 0.15) !important;
        color: #8f7a67 !important;
        box-shadow: 0 0 0 2px rgba(143, 122, 103, 0.3) !important;
    }
    
    /* Mobile responsive navigation */
    @media (max-width: 768px) {
        .stButton > button {
            height: 2.2rem !important;
            font-size: 0.9rem !important;
            padding: 0.1rem !important;
        }
    }
    
    @media (max-width: 480px) {
        .stButton > button {
            height: 2rem !important;
            font-size: 0.8rem !important;
            padding: 0.05rem !important;
        }
    }
    
    .row-widget.stHorizontal > div {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

def notifications_page():
    """Display notifications page"""
    st.markdown("""
    <div class="app-header">
        <div class="app-title">🔔 Notifications</div>
        <div class="app-subtitle">Stay updated with your bookings</div>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.notifications:
        st.markdown("""
        <div style="text-align: center; padding: 3rem; color: #7f8c8d;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">🔔</div>
            <div style="font-size: 1.2rem; font-weight: 600; margin-bottom: 0.5rem;">No notifications yet</div>
            <div>We'll notify you about booking updates and special offers</div>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Mark all as read button
    if st.button("✅ Mark All as Read", use_container_width=True):
        for notification in st.session_state.notifications:
            notification['read'] = True
        st.rerun()
    
    # Display notifications
    for notification in reversed(st.session_state.notifications):
        read_style = "opacity: 0.6;" if notification['read'] else ""
        icon = "📖" if notification['read'] else "🆕"
        
        st.markdown(f"""
        <div class="mobile-review-card" style="{read_style}">
            <div class="review-header">
                <span class="review-user">{icon} {notification['title']}</span>
                <span class="review-date">{notification['timestamp']}</span>
            </div>
            <div class="review-comment">{notification['message']}</div>
        </div>
        """, unsafe_allow_html=True)

def favorites_page():
    """Display favorites page"""
    st.markdown("""
    <div class="app-header">
        <div class="app-title">💖 Favorites</div>
        <div class="app-subtitle">Your preferred cleaners</div>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.favorites:
        st.markdown("""
        <div style="text-align: center; padding: 3rem; color: #7f8c8d;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">💔</div>
            <div style="font-size: 1.2rem; font-weight: 600; margin-bottom: 0.5rem;">No favorites yet</div>
            <div>Tap the heart icon on cleaner cards to add them to favorites</div>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Get favorite cleaners
    cleaners_df = get_cleaners_dataframe()
    favorite_cleaners = cleaners_df[cleaners_df['id'].isin(st.session_state.favorites)]
    
    st.markdown(f"""
    <div style="text-align: center; padding: 1rem 0; font-size: 1.1rem; font-weight: 600; color: #2c3e50;">
        💖 {len(favorite_cleaners)} Favorite Cleaners
    </div>
    """, unsafe_allow_html=True)
    
    # Clear all favorites button
    if st.button("🗑️ Clear All Favorites", use_container_width=True):
        st.session_state.favorites = []
        st.rerun()
    
    # Display favorite cleaners
    for _, cleaner in favorite_cleaners.iterrows():
        display_mobile_cleaner_card(cleaner)

def profile_page():
    """Display user profile page"""
    st.markdown("""
    <div class="app-header">
        <div class="app-title">👤 Profile</div>
        <div class="app-subtitle">Manage your account</div>
    </div>
    """, unsafe_allow_html=True)
    
    # User stats
    profile = st.session_state.user_profile
    total_bookings = len(st.session_state.bookings) + len(st.session_state.completed_bookings)
    
    # Stats overview
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="stats-card">
            <div class="stats-number">{total_bookings}</div>
            <div class="stats-label">Total Bookings</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stats-card">
            <div class="stats-number">${profile['total_spent']:.0f}</div>
            <div class="stats-label">Total Spent</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stats-card">
            <div class="stats-number">{len(st.session_state.favorites)}</div>
            <div class="stats-label">Favorites</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Profile form
    st.markdown("""
    <div class="form-section">
        <div class="form-section-title">👤 Personal Information</div>
    </div>
    """, unsafe_allow_html=True)
    
    name = st.text_input("Full Name", value=profile['name'], placeholder="Enter your full name")
    phone = st.text_input("Phone Number", value=profile['phone'], placeholder="Your phone number")
    address = st.text_area("Address", value=profile['address'], placeholder="Your complete address")
    
    st.markdown("""
    <div class="form-section">
        <div class="form-section-title">⚙️ Preferences</div>
    </div>
    """, unsafe_allow_html=True)
    
    preferred_time = st.selectbox("Preferred Cleaning Time", 
                                 ["Morning (8AM-12PM)", "Afternoon (12PM-5PM)", "Evening (5PM-8PM)"],
                                 index=["Morning (8AM-12PM)", "Afternoon (12PM-5PM)", "Evening (5PM-8PM)"].index(profile.get('preferred_time', 'Morning (8AM-12PM)')))
    
    # Notification preferences
    email_notifications = st.checkbox("📧 Email Notifications", value=True)
    sms_notifications = st.checkbox("📱 SMS Notifications", value=True)
    
    # Save profile
    if st.button("💾 Save Profile", type="primary", use_container_width=True):
        st.session_state.user_profile.update({
            'name': name,
            'phone': phone,
            'address': address,
            'preferred_time': preferred_time
        })
        st.success("✅ Profile updated successfully!")
        st.rerun()
    
    # Account actions
    st.markdown("""
    <div class="form-section">
        <div class="form-section-title">🔧 Account Actions</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Clear Bookings", use_container_width=True):
            st.session_state.bookings = []
            st.session_state.completed_bookings = []
            st.session_state.user_profile['total_spent'] = 0
            st.success("Bookings cleared!")
            st.rerun()
    
    with col2:
        if st.button("🔄 Reset App", use_container_width=True):
            for key in ['bookings', 'completed_bookings', 'favorites', 'notifications']:
                st.session_state[key] = []
            st.session_state.user_profile = {
                'name': '', 'phone': '', 'address': '', 'preferred_time': 'Morning (8AM-12PM)',
                'total_spent': 0, 'total_bookings': 0
            }
            st.success("App reset successfully!")
            st.rerun()

def become_cleaner_page():
    """Comprehensive cleaner application system"""
    st.markdown("""
    <div class="app-header">
        <div class="app-title">🧹✨ Become a Cleaner</div>
        <div class="app-subtitle">Join our trusted cleaning professionals</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Check application status
    if st.session_state.application_status == 'pending':
        show_application_status()
        return
    elif st.session_state.application_status == 'approved':
        show_cleaner_dashboard()
        return
    elif st.session_state.application_status == 'rejected':
        show_reapplication_option()
        return
    
    # Show application intro and earnings
    if st.session_state.application_step == 1:
        show_application_intro()
    elif st.session_state.application_step == 2:
        show_personal_info_form()
    elif st.session_state.application_step == 3:
        show_professional_info_form()
    elif st.session_state.application_step == 4:
        show_documents_upload()
    elif st.session_state.application_step == 5:
        show_references_form()
    elif st.session_state.application_step == 6:
        show_background_check()
    elif st.session_state.application_step == 7:
        show_application_review()

def show_application_intro():
    """Show the introduction and benefits of becoming a cleaner"""
    # Facebook login option
    if not st.session_state.facebook_authenticated:
        st.markdown("""
        <div class="form-section">
            <div class="form-section-title">
                <span style="font-size: 1.5rem;">🚀</span>
                Quick Start with Facebook
            </div>
            <p style="color: #666; margin-bottom: 1rem;">
                Sign up faster and build trust with customers by connecting your Facebook account.
                We'll pre-fill your application with your profile information.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        render_facebook_login_button()
        
        st.markdown("""
        <div style="text-align: center; margin: 1rem 0; color: #666;">
            <span>or</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Show Facebook user info
        user = st.session_state.facebook_user
        st.markdown(f"""
        <div class="mobile-success">
            <div style="display: flex; align-items: center; gap: 1rem; justify-content: center;">
                <img src="{user.get('picture', {}).get('data', {}).get('url', '')}" 
                     style="width: 50px; height: 50px; border-radius: 50%; border: 2px solid white;">
                <div>
                    <div style="font-weight: 600;">Welcome, {user.get('name', '')}!</div>
                    <div style="font-size: 0.9rem; opacity: 0.9;">Connected via Facebook</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Earnings potential
    st.markdown("""
    <div class="earning-estimate">
        <div style="font-size: 1.1rem; font-weight: 600; color: #2c3e50; margin-bottom: 1rem;">💰 Earning Potential</div>
        <div class="earning-amount">$20-35/hour</div>
        <div style="color: #666; font-size: 0.9rem;">Plus tips and bonuses</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Benefits
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="stats-card">
            <div class="stats-number">⏰</div>
            <div class="stats-label">Flexible Hours</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stats-card">
            <div class="stats-number">📱</div>
            <div class="stats-label">Mobile App</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Requirements overview
    st.markdown("""
    <div class="requirement-list">
        <div style="font-weight: 600; margin-bottom: 1rem; color: #2c3e50;">📋 Requirements</div>
        <div class="requirement-item">
            <span class="requirement-icon">✅</span>
            <span>18+ years old with valid ID</span>
        </div>
        <div class="requirement-item">
            <span class="requirement-icon">✅</span>
            <span>Clean background check</span>
        </div>
        <div class="requirement-item">
            <span class="requirement-icon">✅</span>
            <span>2+ professional references</span>
        </div>
        <div class="requirement-item">
            <span class="requirement-icon">✅</span>
            <span>Cleaning experience preferred</span>
        </div>
        <div class="requirement-item">
            <span class="requirement-icon">✅</span>
            <span>Own transportation & cleaning supplies</span>
        </div>
        <div class="requirement-item">
            <span class="requirement-icon">✅</span>
            <span>Professional liability insurance</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Application process steps
    st.markdown("### 🗺️ Application Process")
    
    steps = [
        "📝 Personal Information",
        "💼 Professional Background", 
        "📄 Document Upload",
        "👥 Reference Check",
        "🔍 Background Verification",
        "✅ Application Review"
    ]
    
    for i, step in enumerate(steps, 1):
        st.markdown(f"""
        <div class="verification-item">
            <div style="display: flex; align-items: center;">
                <div class="step-number" style="width: 25px; height: 25px; font-size: 0.8rem;">{i}</div>
                <span>{step}</span>
            </div>
            <span>⏳</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    if st.button("🚀 Start Application", type="primary", use_container_width=True):
        st.session_state.application_step = 2
        st.rerun()
    
    st.markdown("""
    <div style="text-align: center; color: #7f8c8d; font-size: 0.85rem; margin-top: 1rem;">
        ⏱️ Estimated completion time: 15-20 minutes<br>
        🔒 All information is secure and encrypted
    </div>
    """, unsafe_allow_html=True)

def show_personal_info_form():
    """Step 2: Personal information form"""
    st.markdown("""
    <div class="application-step">
        <div class="step-header">
            <div class="step-number">1</div>
            <span>Personal Information</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Show Facebook connection status
    if st.session_state.facebook_authenticated:
        user = st.session_state.facebook_user
        st.markdown(f"""
        <div style="background: #e8f5e8; padding: 0.8rem; border-radius: 8px; margin-bottom: 1rem; border-left: 4px solid #7a9b76;">
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span>📘</span>
                <span style="font-weight: 600; color: #2c3e50;">Facebook Profile Connected</span>
            </div>
            <div style="font-size: 0.85rem; color: #666; margin-top: 0.3rem;">
                Some fields have been pre-filled from your Facebook profile
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Form fields - pre-fill with Facebook data if available
    facebook_data = st.session_state.current_application if st.session_state.facebook_authenticated else {}
    
    col1, col2 = st.columns(2)
    with col1:
        first_name = st.text_input("First Name *", 
                                  value=facebook_data.get('first_name', ''),
                                  placeholder="Enter your first name")
        email = st.text_input("Email Address *", 
                             value=facebook_data.get('email', ''),
                             placeholder="your.email@example.com")
        phone = st.text_input("Phone Number *", placeholder="(555) 123-4567")
    
    with col2:
        last_name = st.text_input("Last Name *", 
                                 value=facebook_data.get('last_name', ''),
                                 placeholder="Enter your last name")
        date_of_birth = st.date_input("Date of Birth *", 
                                     min_value=datetime(1930, 1, 1).date(),
                                     max_value=datetime.now().date(),
                                     value=datetime(1990, 1, 1).date(),
                                     help="You must be at least 18 years old to apply")
        emergency_contact = st.text_input("Emergency Contact *", placeholder="Emergency contact number")
    
    address = st.text_area("Home Address *", placeholder="Full address including city, state, zip code")
    
    # ID verification
    st.markdown("### 🆔 Identity Verification")
    id_type = st.selectbox("ID Type *", ["Driver's License", "State ID", "Passport", "Military ID"])
    id_number = st.text_input("ID Number *", placeholder="Enter ID number", type="password", 
                             help="This information is encrypted and used only for verification purposes")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back", use_container_width=True):
            st.session_state.application_step = 1
            st.rerun()
    
    with col2:
        if st.button("Continue →", type="primary", use_container_width=True):
            # Check required fields
            missing_fields = []
            if not first_name.strip():
                missing_fields.append("First Name")
            if not last_name.strip():
                missing_fields.append("Last Name") 
            if not email.strip():
                missing_fields.append("Email Address")
            if not phone.strip():
                missing_fields.append("Phone Number")
            if not address.strip():
                missing_fields.append("Home Address")
            if not emergency_contact.strip():
                missing_fields.append("Emergency Contact")
            if not id_number.strip():
                missing_fields.append("ID Number")
            
            # Check age requirement (18+)
            today = datetime.now().date()
            age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
            
            if missing_fields:
                st.error(f"Please fill in these required fields: {', '.join(missing_fields)}")
            elif age < 18:
                st.error("You must be at least 18 years old to apply as a cleaner.")
            else:
                st.session_state.current_application.update({
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                    'phone': phone,
                    'date_of_birth': date_of_birth.strftime('%Y-%m-%d'),
                    'address': address,
                    'emergency_contact': emergency_contact,
                    'id_type': id_type,
                    'id_number': id_number
                })
                st.session_state.application_step = 3
                st.rerun()

def show_professional_info_form():
    """Step 3: Professional background form"""
    st.markdown("""
    <div class="application-step">
        <div class="step-header">
            <div class="step-number">2</div>
            <span>Professional Background</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Experience
    cleaning_experience = st.selectbox("Cleaning Experience *", 
                                     ["No experience", "Less than 1 year", "1-2 years", 
                                      "3-5 years", "5+ years", "Professional cleaner"])
    
    previous_work = st.text_area("Previous Work Experience", 
                                placeholder="Describe your work history, especially any cleaning or service-related jobs")
    
    # Skills and specializations
    st.markdown("### 🛠️ Skills & Specializations")
    skills = st.multiselect("Select your skills *", [
        "General House Cleaning", "Deep Cleaning", "Move-in/Move-out Cleaning",
        "Office Cleaning", "Post-construction Cleanup", "Carpet Cleaning",
        "Window Cleaning", "Pressure Washing", "Eco-friendly Cleaning",
        "Pet-friendly Cleaning", "Organizing Services"
    ])
    
    # Equipment and supplies
    st.markdown("### 🧽 Equipment & Supplies")
    has_equipment = st.checkbox("I have my own cleaning equipment and supplies")
    has_transportation = st.checkbox("I have reliable transportation")
    has_insurance = st.checkbox("I have professional liability insurance (or willing to obtain)")
    
    # Availability
    st.markdown("### 📅 Availability")
    col1, col2 = st.columns(2)
    with col1:
        days_available = st.multiselect("Days Available *", 
                                       ["Monday", "Tuesday", "Wednesday", "Thursday", 
                                        "Friday", "Saturday", "Sunday"])
    
    with col2:
        hours_per_week = st.selectbox("Hours per week *", 
                                    ["5-10 hours", "10-20 hours", "20-30 hours", 
                                     "30-40 hours", "40+ hours"])
    
    preferred_rate = st.slider("Preferred Hourly Rate", 15, 35, 25, 1, 
                              help="Based on your experience and local market rates")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back", use_container_width=True):
            st.session_state.application_step = 2
            st.rerun()
    
    with col2:
        if st.button("Continue →", type="primary", use_container_width=True):
            if skills and days_available:
                st.session_state.current_application.update({
                    'cleaning_experience': cleaning_experience,
                    'previous_work': previous_work,
                    'skills': skills,
                    'has_equipment': has_equipment,
                    'has_transportation': has_transportation,
                    'has_insurance': has_insurance,
                    'days_available': days_available,
                    'hours_per_week': hours_per_week,
                    'preferred_rate': preferred_rate
                })
                st.session_state.application_step = 4
                st.rerun()
            else:
                st.error("Please select at least one skill and available day")

def show_documents_upload():
    """Step 4: Document upload simulation"""
    st.markdown("""
    <div class="application-step">
        <div class="step-header">
            <div class="step-number">3</div>
            <span>Document Upload</span>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📄 Required Documents")
    
    # Document upload areas (simulated)
    documents = [
        ("Government ID", "Upload a clear photo of your government-issued ID", "id_document"),
        ("Proof of Address", "Utility bill or bank statement (last 3 months)", "address_proof"),
        ("Insurance Certificate", "Professional liability insurance (if available)", "insurance"),
        ("Work Authorization", "Social Security card or work permit", "work_auth")
    ]
    
    uploaded_docs = {}
    
    for doc_name, description, key in documents:
        st.markdown(f"**{doc_name}**")
        st.markdown(f"*{description}*")
        
        # Simulated file upload
        uploaded_file = st.file_uploader(f"Upload {doc_name}", key=key, 
                                       type=['jpg', 'jpeg', 'png', 'pdf'],
                                       help="Accepted formats: JPG, PNG, PDF (max 5MB)")
        
        if uploaded_file:
            uploaded_docs[key] = uploaded_file.name
            st.success(f"✅ {doc_name} uploaded successfully")
        else:
            st.markdown("""
            <div class="upload-area">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">📁</div>
                <div>Click to upload or drag and drop</div>
                <div style="font-size: 0.8rem; color: #666; margin-top: 0.5rem;">Max file size: 5MB</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Progress indicator
    progress = len(uploaded_docs) / len(documents) * 100
    st.markdown(f"""
    <div class="progress-bar">
        <div class="progress-fill" style="width: {progress}%;"></div>
    </div>
    <div style="text-align: center; color: #666; font-size: 0.9rem;">
        {len(uploaded_docs)}/{len(documents)} documents uploaded
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back", use_container_width=True):
            st.session_state.application_step = 3
            st.rerun()
    
    with col2:
        if st.button("Continue →", type="primary", use_container_width=True):
            # Require at least ID and work authorization
            required_docs = ['id_document', 'work_auth']
            if all(doc in uploaded_docs for doc in required_docs):
                st.session_state.current_application['documents'] = uploaded_docs
                st.session_state.application_step = 5
                st.rerun()
            else:
                st.error("Please upload at least your ID and work authorization documents")

def show_references_form():
    """Step 5: Professional references"""
    st.markdown("""
    <div class="application-step">
        <div class="step-header">
            <div class="step-number">4</div>
            <span>Professional References</span>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 👥 Professional References")
    st.markdown("*Please provide at least 2 professional references who can vouch for your work quality and reliability.*")
    
    references = []
    
    for i in range(3):
        st.markdown(f"**Reference {i+1}** {'*' if i < 2 else '(Optional)'}")
        
        col1, col2 = st.columns(2)
        with col1:
            ref_name = st.text_input(f"Full Name", key=f"ref_name_{i}", 
                                   placeholder="Reference full name")
            ref_phone = st.text_input(f"Phone Number", key=f"ref_phone_{i}",
                                    placeholder="Reference phone number")
        
        with col2:
            ref_email = st.text_input(f"Email", key=f"ref_email_{i}",
                                    placeholder="Reference email address")
            ref_relationship = st.selectbox(f"Relationship", 
                                          ["Former Employer", "Current Employer", "Client", 
                                           "Supervisor", "Colleague", "Other"],
                                          key=f"ref_rel_{i}")
        
        ref_company = st.text_input(f"Company/Organization", key=f"ref_company_{i}",
                                  placeholder="Where did you work together?")
        
        if ref_name and ref_phone:
            references.append({
                'name': ref_name,
                'phone': ref_phone,
                'email': ref_email,
                'relationship': ref_relationship,
                'company': ref_company
            })
        
        if i < 2:  # Add separator between required references
            st.markdown("---")
    
    # LinkedIn profile (optional)
    st.markdown("### 💼 LinkedIn Profile (Optional)")
    linkedin_url = st.text_input("LinkedIn URL", placeholder="https://linkedin.com/in/yourprofile")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back", use_container_width=True):
            st.session_state.application_step = 4
            st.rerun()
    
    with col2:
        if st.button("Continue →", type="primary", use_container_width=True):
            if len(references) >= 2:
                st.session_state.current_application.update({
                    'references': references,
                    'linkedin_url': linkedin_url
                })
                st.session_state.application_step = 6
                st.rerun()
            else:
                st.error("Please provide at least 2 professional references")

def show_background_check():
    """Step 6: Background check consent and questions"""
    st.markdown("""
    <div class="application-step">
        <div class="step-header">
            <div class="step-number">5</div>
            <span>Background Check & Verification</span>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🔍 Background Check Consent")
    st.markdown("""
    To ensure the safety of our customers, we require all cleaners to undergo a comprehensive background check.
    This includes:
    """)
    
    # Background check items
    check_items = [
        "Criminal background check",
        "Identity verification", 
        "Employment history verification",
        "Reference checks",
        "Social Security number verification"
    ]
    
    for item in check_items:
        st.markdown(f"• {item}")
    
    consent_background = st.checkbox("I consent to a background check", key="bg_consent")
    
    # Additional questions
    st.markdown("### ❓ Background Questions")
    
    criminal_history = st.radio("Have you ever been convicted of a crime?", 
                               ["No", "Yes"], key="criminal_q")
    
    if criminal_history == "Yes":
        criminal_details = st.text_area("Please provide details:", 
                                       placeholder="Explain the circumstances and date")
    else:
        criminal_details = ""
    
    work_authorization = st.radio("Are you authorized to work in the United States?", 
                                 ["Yes", "No"], key="work_auth_q")
    
    reliable_transport = st.radio("Do you have reliable transportation?", 
                                 ["Yes", "No"], key="transport_q")
    
    # Drug screening consent
    drug_screening = st.checkbox("I consent to drug screening if required", key="drug_consent")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back", use_container_width=True):
            st.session_state.application_step = 5
            st.rerun()
    
    with col2:
        if st.button("Continue →", type="primary", use_container_width=True):
            if consent_background and work_authorization == "Yes":
                st.session_state.current_application.update({
                    'background_consent': consent_background,
                    'criminal_history': criminal_history,
                    'criminal_details': criminal_details,
                    'work_authorization': work_authorization,
                    'reliable_transport': reliable_transport,
                    'drug_screening_consent': drug_screening
                })
                st.session_state.application_step = 7
                st.rerun()
            else:
                st.error("Background check consent and work authorization are required")

def show_application_review():
    """Step 7: Final review and submission"""
    st.markdown("""
    <div class="application-step">
        <div class="step-header">
            <div class="step-number">6</div>
            <span>Application Review</span>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📋 Review Your Application")
    
    app = st.session_state.current_application
    
    # Personal info summary
    st.markdown("**Personal Information**")
    st.write(f"• Name: {app.get('first_name', '')} {app.get('last_name', '')}")
    st.write(f"• Email: {app.get('email', '')}")
    st.write(f"• Phone: {app.get('phone', '')}")
    st.write(f"• Address: {app.get('address', '')}")
    
    # Professional info summary
    st.markdown("**Professional Background**")
    st.write(f"• Experience: {app.get('cleaning_experience', '')}")
    st.write(f"• Skills: {', '.join(app.get('skills', []))}")
    st.write(f"• Availability: {', '.join(app.get('days_available', []))}")
    st.write(f"• Preferred Rate: ${app.get('preferred_rate', 0)}/hour")
    
    # Documents
    st.markdown("**Documents Uploaded**")
    docs = app.get('documents', {})
    for doc_type, filename in docs.items():
        st.write(f"• {doc_type}: ✅ {filename}")
    
    # References
    st.markdown("**References**")
    refs = app.get('references', [])
    for i, ref in enumerate(refs, 1):
        st.write(f"• Reference {i}: {ref['name']} ({ref['relationship']})")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Terms and conditions
    st.markdown("### 📜 Terms and Conditions")
    
    terms_agreed = st.checkbox("""
    I agree to CleanFee's Terms of Service and Privacy Policy. I understand that:
    • All information provided is accurate and truthful
    • Background check and reference verification will be conducted
    • Final approval is subject to verification results
    • I will maintain professional standards and customer service
    """)
    
    # Final submission
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back", use_container_width=True):
            st.session_state.application_step = 6
            st.rerun()
    
    with col2:
        if st.button("🚀 Submit Application", type="primary", use_container_width=True):
            if terms_agreed:
                # Submit application
                application_id = f"APP{len(st.session_state.cleaner_applications) + 1:04d}"
                
                final_application = st.session_state.current_application.copy()
                final_application.update({
                    'id': application_id,
                    'submission_date': datetime.now().strftime('%Y-%m-%d %H:%M'),
                    'status': 'pending',
                    'terms_agreed': terms_agreed
                })
                
                st.session_state.cleaner_applications.append(final_application)
                st.session_state.application_status = 'pending'
                st.session_state.current_application = {}
                st.session_state.application_step = 1
                
                # Add notification
                notification = {
                    'id': len(st.session_state.notifications) + 1,
                    'type': 'application_submitted',
                    'title': 'Application Submitted! 📝',
                    'message': f'Your cleaner application ({application_id}) has been submitted and is under review.',
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M'),
                    'read': False
                }
                st.session_state.notifications.append(notification)
                
                st.success("🎉 Application submitted successfully!")
                st.balloons()
                st.rerun()
            else:
                st.error("Please agree to the terms and conditions")

def show_application_status():
    """Show pending application status"""
    st.markdown("""
    <div class="application-summary">
        <div style="font-size: 2rem; margin-bottom: 1rem;">⏳</div>
        <div style="font-size: 1.3rem; font-weight: 600; margin-bottom: 0.5rem;">Application Under Review</div>
        <div style="opacity: 0.9;">We're reviewing your application and conducting background checks</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Application timeline
    st.markdown("### 📅 Review Timeline")
    
    timeline_items = [
        ("Application Submitted", "✅", "completed"),
        ("Document Verification", "🔍", "pending"),
        ("Background Check", "⏳", "pending"),
        ("Reference Check", "📞", "pending"),
        ("Final Review", "👥", "pending"),
        ("Decision", "📋", "pending")
    ]
    
    for item, icon, status in timeline_items:
        status_class = "verified" if status == "completed" else "pending"
        st.markdown(f"""
        <div class="verification-item {status_class}">
            <div style="display: flex; align-items: center;">
                <span style="margin-right: 1rem; font-size: 1.2rem;">{icon}</span>
                <span>{item}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.info("💡 Review typically takes 3-5 business days. We'll notify you of any updates!")
    
    # Admin simulation buttons (for demo)
    st.markdown("---")
    st.markdown("### 🔧 Admin Actions (Demo)")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Approve Application", use_container_width=True):
            st.session_state.application_status = 'approved'
            # Add approval notification
            notification = {
                'id': len(st.session_state.notifications) + 1,
                'type': 'application_approved',
                'title': 'Application Approved! 🎉',
                'message': 'Congratulations! Your cleaner application has been approved. Welcome to CleanFee!',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'read': False
            }
            st.session_state.notifications.append(notification)
            st.rerun()
    
    with col2:
        if st.button("❌ Reject Application", use_container_width=True):
            st.session_state.application_status = 'rejected'
            st.rerun()

def show_cleaner_dashboard():
    """Show dashboard for approved cleaners"""
    st.markdown("""
    <div class="application-summary">
        <div style="font-size: 2rem; margin-bottom: 1rem;">🎉</div>
        <div style="font-size: 1.3rem; font-weight: 600; margin-bottom: 0.5rem;">Welcome to CleanFee!</div>
        <div style="opacity: 0.9;">You're now an approved cleaner</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="stats-card">
            <div class="stats-number">0</div>
            <div class="stats-label">Jobs Completed</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stats-card">
            <div class="stats-number">$0</div>
            <div class="stats-label">Total Earned</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stats-card">
            <div class="stats-number">0</div>
            <div class="stats-label">Pending Jobs</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Action buttons
    st.markdown("### 🚀 Get Started")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📱 Download Cleaner App", use_container_width=True):
            st.info("📱 The CleanFee Cleaner app download would be available here!")
    
    with col2:
        if st.button("📚 Training Materials", use_container_width=True):
            st.info("📚 Training materials and best practices would be available here!")
    
    # Next steps
    st.markdown("### 📋 Next Steps")
    st.markdown("""
    1. **Download the CleanFee Cleaner app** to receive job notifications
    2. **Complete your profile** with photos and additional details
    3. **Set your availability** to start receiving job requests
    4. **Review safety guidelines** and cleaning standards
    5. **Start earning!** Accept your first cleaning job
    """)

def show_reapplication_option():
    """Show options after rejection"""
    st.markdown("""
    <div style="background: #f8d7da; border: 1px solid #f5c6cb; color: #721c24; padding: 1rem; border-radius: 12px; text-align: center;">
        <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">❌</div>
        <div style="font-size: 1.2rem; font-weight: 600; margin-bottom: 0.5rem;">Application Not Approved</div>
        <div>We appreciate your interest, but we cannot approve your application at this time.</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🔄 What's Next?")
    st.markdown("""
    - **Review requirements** and ensure you meet all criteria
    - **Gain more experience** in cleaning or customer service
    - **Obtain required documents** like professional liability insurance
    - **Reapply in 6 months** with updated information
    """)
    
    if st.button("🔄 Start New Application", use_container_width=True):
        st.session_state.application_status = None
        st.session_state.application_step = 1
        st.session_state.current_application = {}
        st.rerun()

# Main content routing
if st.session_state.page == 'home':
    home_page()
elif st.session_state.page == 'booking':
    booking_page()
elif st.session_state.page == 'reviews':
    reviews_page()
elif st.session_state.page == 'bookings':
    my_bookings_page()
elif st.session_state.page == 'notifications':
    notifications_page()
elif st.session_state.page == 'favorites':
    favorites_page()
elif st.session_state.page == 'become_cleaner':
    become_cleaner_page()
elif st.session_state.page == 'profile':
    profile_page()

# Navigation is now handled by the column buttons above 