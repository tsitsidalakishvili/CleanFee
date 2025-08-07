# 🧹 CleanFee - Mobile Home Cleaning App

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://cleanfee-mobile.streamlit.app)

A modern, mobile-first Streamlit web application for booking professional home cleaning services. Designed to look and feel like a native mobile app!

## 📱 Live Demo

**🚀 [Try CleanFee Live](https://cleanfee-mobile.streamlit.app)**

## ✨ Features

### 📲 **Mobile-First Design**
- Native app-like interface with gradients and animations
- Bottom navigation bar (like Instagram/Twitter)
- Touch-optimized buttons and interactions
- Card-based layout for easy browsing
- Responsive design for all screen sizes

### 🧹 **Core Functionality**
- **Browse Cleaners**: Professional profiles with photos, ratings, and reviews
- **Smart Filtering**: Filter by price, rating, and experience level
- **Easy Booking**: Intuitive date/time selection with availability checking
- **Real-time Pricing**: Dynamic cost calculation with add-on services
- **Booking Management**: Track upcoming and completed services
- **Rating System**: Rate and review completed cleanings

### 👥 **Professional Cleaners**
- 5 verified cleaners with realistic profiles
- Real profile photos and detailed bios
- Skill specializations and experience levels
- Dynamic availability system
- Customer reviews and ratings

## 🚀 Quick Start (Local Development)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/cleanfee-mobile-app.git
   cd cleanfee-mobile-app
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app:**
   ```bash
   streamlit run app.py
   ```

4. **Open in browser:**
   The app will open at `http://localhost:8501`

## 📱 How to Use

### 1. 🏠 Browse Cleaners
- Scroll through beautiful cleaner cards
- Use the filter to find cleaners by budget and rating
- Tap "Book" to start booking or "Reviews" to read feedback

### 2. 📅 Book a Service
- Select your preferred date and available time slot
- Choose cleaning duration (1-5 hours)
- Add optional services (deep cleaning, oven, etc.)
- Enter contact information and confirm booking

### 3. 📊 Manage Bookings
- View upcoming bookings in the "Bookings" tab
- Mark services as completed when finished
- Rate your cleaner and leave a review

### 4. ⭐ View Reviews
- Read authentic customer reviews
- See overall ratings and detailed feedback
- Make informed decisions about your cleaner

## 🏗️ Project Structure

```
CleanFee/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore file
├── data/
│   └── cleaners_data.py  # Cleaner profiles and data
└── README.md             # This documentation
```

## 🎨 Design Features

- **Gradient Backgrounds**: Beautiful purple-blue gradients
- **Card-Based Layout**: Modern card design with shadows
- **Mobile Navigation**: Bottom tab bar navigation
- **Touch-Friendly**: Large buttons and touch targets
- **Professional Colors**: Carefully chosen color scheme
- **Smooth Animations**: Hover effects and transitions

## 🛠️ Technical Stack

- **Framework**: Streamlit 1.28+
- **Data**: Pandas for data manipulation
- **Images**: Unsplash API for professional photos
- **Styling**: Custom CSS for mobile-first design
- **State Management**: Streamlit session state
- **Deployment**: Streamlit Community Cloud

## 🌟 Demo Data

The app includes:
- **5 Professional Cleaners** with unique specializations
- **Realistic Reviews** and ratings
- **Dynamic Availability** system
- **Varied Pricing** from $20-$28/hour
- **Multiple Services** and add-ons

## 🚀 Deployment on Streamlit Cloud

This app is optimized for deployment on Streamlit Community Cloud:

1. **Fork this repository** on GitHub
2. **Connect to Streamlit Cloud** at [share.streamlit.io](https://share.streamlit.io)
3. **Deploy** with one click!

## 📈 Future Enhancements

- [ ] Real-time chat with cleaners
- [ ] Payment integration (Stripe)
- [ ] GPS location tracking
- [ ] Push notifications
- [ ] Cleaner availability calendar
- [ ] Multi-language support
- [ ] Dark mode theme

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 📞 Support

For support or questions, please open an issue on GitHub.

---

**🧹 CleanFee** - Professional home cleaning at your fingertips!

Made with ❤️ using Streamlit
