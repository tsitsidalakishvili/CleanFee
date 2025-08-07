import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, date
from data.cleaners_data import (
    get_cleaners_dataframe, 
    get_cleaner_reviews, 
    get_cleaner_availability,
    CLEANERS_DATA
)

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
        padding: 1rem 1rem 5rem 1rem !important;
        max-width: 100% !important;
    }
    
    /* App header */
    .app-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem 1rem;
        margin: -1rem -1rem 1rem -1rem;
        text-align: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .app-title {
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }
    
    .app-subtitle {
        font-size: 0.9rem;
        opacity: 0.9;
        margin: 0.3rem 0 0 0;
    }
    
    /* Mobile cleaner cards */
    .mobile-cleaner-card {
        background: white;
        border-radius: 16px;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: none;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .mobile-cleaner-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.12);
    }
    
    .cleaner-avatar {
        width: 70px;
        height: 70px;
        border-radius: 50%;
        object-fit: cover;
        border: 3px solid #f0f0f0;
    }
    
    .cleaner-info {
        flex: 1;
        margin-left: 1rem;
    }
    
    .cleaner-name {
        font-size: 1.1rem;
        font-weight: 600;
        color: #2c3e50;
        margin: 0 0 0.3rem 0;
    }
    
    .cleaner-rating {
        display: flex;
        align-items: center;
        margin: 0.3rem 0;
    }
    
    .rating-text {
        font-size: 0.85rem;
        color: #666;
        margin-left: 0.5rem;
    }
    
    .cleaner-price {
        font-size: 1.3rem;
        font-weight: 700;
        color: #27ae60;
        margin: 0.5rem 0;
    }
    
    .cleaner-experience {
        font-size: 0.8rem;
        color: #7f8c8d;
        background: #f8f9fa;
        padding: 0.3rem 0.6rem;
        border-radius: 12px;
        display: inline-block;
        margin: 0.3rem 0;
    }
    
    /* Mobile skill tags */
    .mobile-skill-tag {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 0.3rem 0.7rem;
        border-radius: 15px;
        font-size: 0.7rem;
        margin: 0.2rem 0.3rem 0.2rem 0;
        display: inline-block;
        font-weight: 500;
    }
    
    /* Mobile buttons */
    .mobile-btn {
        background: linear-gradient(135deg, #667eea, #764ba2);
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
        box-shadow: 0 2px 10px rgba(102, 126, 234, 0.3);
    }
    
    .mobile-btn:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .mobile-btn-secondary {
        background: transparent;
        color: #667eea;
        border: 2px solid #667eea;
        box-shadow: none;
    }
    
    .mobile-btn-secondary:hover {
        background: #667eea;
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
    }
    
    .nav-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-decoration: none;
        color: #95a5a6;
        transition: color 0.2s ease;
        cursor: pointer;
        padding: 0.3rem;
    }
    
    .nav-item.active {
        color: #667eea;
    }
    
    .nav-icon {
        font-size: 1.5rem;
        margin-bottom: 0.2rem;
    }
    
    .nav-label {
        font-size: 0.7rem;
        font-weight: 500;
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
        background: linear-gradient(135deg, #00b894, #00cec9);
        color: white;
        padding: 1rem;
        border-radius: 16px;
        margin: 1rem 0;
        text-align: center;
        font-weight: 500;
        box-shadow: 0 4px 15px rgba(0, 184, 148, 0.3);
    }
    
    /* Review cards */
    .mobile-review-card {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.8rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        border-left: 4px solid #667eea;
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
            padding: 0.5rem 0.5rem 5rem 0.5rem !important;
        }
        
        .app-header {
            margin: -0.5rem -0.5rem 1rem -0.5rem;
        }
        
        .mobile-cleaner-card {
            margin: 0.8rem 0;
            padding: 0.8rem;
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

def display_star_rating(rating):
    """Display star rating"""
    full_stars = int(rating)
    half_star = 1 if rating - full_stars >= 0.5 else 0
    empty_stars = 5 - full_stars - half_star
    
    stars = "⭐" * full_stars + "⭐" * half_star + "☆" * empty_stars
    return f"{stars} ({rating:.1f})"

def display_mobile_cleaner_card(cleaner):
    """Display a mobile-optimized cleaner card"""
    # Create mobile card HTML
    stars = "⭐" * int(cleaner['rating'])
    skills_html = " ".join([f'<span class="mobile-skill-tag">{skill}</span>' for skill in cleaner['skills']])
    
    card_html = f"""
    <div class="mobile-cleaner-card">
        <div style="display: flex; align-items: flex-start;">
            <img src="{cleaner['image_url']}" class="cleaner-avatar" alt="{cleaner['name']}">
            <div class="cleaner-info">
                <div class="cleaner-name">{cleaner['name']}</div>
                <div class="cleaner-rating">
                    <span class="review-stars">{stars}</span>
                    <span class="rating-text">({cleaner['rating']:.1f}) • {cleaner['total_reviews']} reviews</span>
                </div>
                <div class="cleaner-price">${cleaner['hourly_rate']:.2f}/hour</div>
                <div class="cleaner-experience">{cleaner['experience_years']} years experience</div>
            </div>
        </div>
        <div style="margin-top: 0.8rem;">
            <div style="font-size: 0.85rem; color: #555; margin-bottom: 0.5rem;">{cleaner['bio']}</div>
            <div>{skills_html}</div>
        </div>
    </div>
    """
    
    st.markdown(card_html, unsafe_allow_html=True)
    
    # Mobile buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button(f"📅 Book {cleaner['name']}", key=f"select_{cleaner['id']}", help="Book this cleaner"):
            st.session_state.selected_cleaner = cleaner.to_dict()
            st.session_state.page = 'booking'
            st.rerun()
    
    with col2:
        if st.button(f"⭐ Reviews", key=f"reviews_{cleaner['id']}", help="View reviews"):
            st.session_state.selected_cleaner = cleaner.to_dict()
            st.session_state.page = 'reviews'
            st.rerun()

def home_page():
    """Display the mobile-optimized home page"""
    # Mobile app header
    st.markdown("""
    <div class="app-header">
        <div class="app-title">🧹 CleanFee</div>
        <div class="app-subtitle">Professional Home Cleaning</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Mobile filters section
    with st.expander("🔍 Filter Cleaners", expanded=False):
        st.markdown('<div class="filter-title">Find Your Perfect Cleaner</div>', unsafe_allow_html=True)
        
        price_range = st.slider("💰 Hourly Rate", 15, 35, (15, 35), 1, help="Set your budget range")
        min_rating = st.slider("⭐ Minimum Rating", 1.0, 5.0, 4.0, 0.1, help="Filter by rating")
        experience_filter = st.selectbox("🎯 Experience Level", [0, 2, 5, 7], index=0, 
                                        format_func=lambda x: f"{x}+ years" if x > 0 else "Any experience")
    
    # Get and filter cleaners
    cleaners_df = get_cleaners_dataframe()
    
    filtered_cleaners = cleaners_df[
        (cleaners_df['hourly_rate'] >= price_range[0]) &
        (cleaners_df['hourly_rate'] <= price_range[1]) &
        (cleaners_df['rating'] >= min_rating) &
        (cleaners_df['experience_years'] >= experience_filter)
    ]
    
    # Results count with emoji
    st.markdown(f"""
    <div style="text-align: center; padding: 1rem 0; font-size: 1.1rem; font-weight: 600; color: #2c3e50;">
        👥 {len(filtered_cleaners)} Professional Cleaners Available
    </div>
    """, unsafe_allow_html=True)
    
    # Display mobile cleaner cards
    for _, cleaner in filtered_cleaners.iterrows():
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
                    'id': len(st.session_state.bookings) + 1,
                    'cleaner_id': cleaner['id'],
                    'cleaner_name': cleaner['name'],
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
                    'booking_date': datetime.now().strftime('%Y-%m-%d %H:%M')
                }
                
                st.session_state.bookings.append(booking)
                
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

# Navigation buttons (hidden but functional)
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("🏠", key="nav_home", help="Home"):
        st.session_state.page = "home"
        st.rerun()
with col2:
    if st.button("📅", key="nav_bookings", help="My Bookings"):
        st.session_state.page = "bookings"
        st.rerun()
with col3:
    if st.button("💬", key="nav_support", help="Support"):
        st.info("Support feature coming soon!")
with col4:
    if st.button("👤", key="nav_profile", help="Profile"):
        st.info("Profile feature coming soon!")

# Hide the navigation buttons with CSS
st.markdown("""
<style>
    .row-widget.stHorizontal > div {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# Main content routing
if st.session_state.page == 'home':
    home_page()
elif st.session_state.page == 'booking':
    booking_page()
elif st.session_state.page == 'reviews':
    reviews_page()
elif st.session_state.page == 'bookings':
    my_bookings_page()

# Render bottom navigation
render_bottom_nav() 