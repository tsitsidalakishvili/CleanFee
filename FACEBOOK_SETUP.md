# Facebook OAuth Integration Setup

## Overview
CleanFee now supports Facebook login for cleaner registration, making the signup process faster and building customer trust through social verification.

## Features
- 🚀 **Quick signup** with Facebook profile data
- 📋 **Auto-filled forms** with name and email
- 📘 **Social verification** for increased trust
- 🔒 **Secure OAuth 2.0** authentication
- 📱 **Mobile-optimized** login flow

## Setup Instructions

### 1. Create Facebook App
1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Click "Create App" → "Consumer" → "Next"
3. Enter your app details:
   - **App Name**: CleanFee
   - **App Contact Email**: your-email@domain.com
4. Complete the security check and create the app

### 2. Configure Facebook Login
1. In your Facebook app dashboard, click "Add Product"
2. Find "Facebook Login" and click "Set Up"
3. Choose "Web" platform
4. Enter your site URL: `https://your-cleanfee-app.streamlit.app`

### 3. Configure OAuth Settings
1. Go to "Facebook Login" → "Settings"
2. Add these Valid OAuth Redirect URIs:
   ```
   https://your-cleanfee-app.streamlit.app
   https://your-cleanfee-app.streamlit.app/
   ```
3. Save changes

### 4. Get App Credentials
1. Go to "Settings" → "Basic"
2. Copy your **App ID** and **App Secret**
3. Add them to your Streamlit secrets

### 5. Configure Streamlit Secrets
1. Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml`
2. Update with your Facebook app credentials:
   ```toml
   FACEBOOK_APP_ID = "your_app_id_here"
   FACEBOOK_APP_SECRET = "your_app_secret_here"
   REDIRECT_URI = "https://your-cleanfee-app.streamlit.app"
   ```

### 6. Deploy to Streamlit Cloud
1. In Streamlit Cloud, go to your app settings
2. Add the secrets in the "Secrets" section:
   ```toml
   FACEBOOK_APP_ID = "your_app_id_here"
   FACEBOOK_APP_SECRET = "your_app_secret_here"
   REDIRECT_URI = "https://your-cleanfee-app.streamlit.app"
   ```

## How It Works

### For Cleaners
1. Click "Become a Cleaner" 
2. See Facebook login option with benefits
3. Click "Continue with Facebook"
4. Authorize the app (one-time)
5. Return to CleanFee with pre-filled application
6. Complete remaining required fields
7. Submit application

### Data Retrieved
- **Name**: First and last name
- **Email**: Primary email address
- **Profile Picture**: For application review
- **Facebook ID**: For verification purposes

### Privacy & Security
- ✅ Only basic profile data is requested
- ✅ Email permission is explicitly requested
- ✅ Data is used only for application processing
- ✅ No posting to Facebook timeline
- ✅ Secure OAuth 2.0 implementation

## Benefits

### For Cleaners
- **Faster signup**: No manual typing of basic info
- **Increased trust**: Social profile verification
- **Better approval rates**: Complete profile data
- **Professional appearance**: Connected social profile

### For Customers
- **Verified profiles**: Facebook-authenticated cleaners
- **Increased trust**: Real social media presence
- **Better screening**: Additional verification layer
- **Professional service**: Higher quality applicants

## Testing
1. Use Facebook's test users for development
2. Test the complete flow: login → pre-fill → submit
3. Verify data accuracy and security
4. Test mobile responsiveness

## Support
- Facebook app must be "Live" for public use
- Test with Facebook test users during development
- Monitor Facebook app dashboard for errors
- Check Streamlit logs for integration issues

## Troubleshooting

### Common Issues

#### 1. "www.facebook.com refused to connect"
**Cause**: Facebook blocks iframe embedding for security
**Solutions**:
- ✅ **New tab approach**: Button now opens Facebook in new tab
- ✅ **Alternative verification**: Manual social profile entry
- ✅ **Graceful fallback**: Manual registration always available

#### 2. "App Not Setup"  
**Cause**: App needs to be Live in Facebook settings
**Solution**: Go to App Review → Make app Live

#### 3. "Invalid Redirect URI"
**Cause**: OAuth settings don't match exactly
**Solution**: Check redirect URIs match your app URL exactly

#### 4. "App Secret Required"
**Cause**: Secrets not properly configured
**Solution**: Verify Streamlit secrets configuration

#### 5. "Permission Denied"
**Cause**: App permissions or review status issues
**Solution**: Check app permissions and review status

### Facebook Connection Alternatives

If Facebook OAuth isn't working:

1. **Social Profile URLs**: Users can manually enter their Facebook/LinkedIn profiles
2. **Manual Registration**: Traditional form-based signup still works
3. **Multiple Verification**: Support for LinkedIn, Instagram, other platforms
4. **Professional Networks**: LinkedIn verification often preferred for services

### Technical Solutions Implemented

1. **New Tab Opening**: Avoids iframe restrictions
2. **Error Handling**: Graceful fallbacks for all failure modes  
3. **Alternative Verification**: Social profile URL collection
4. **Progressive Enhancement**: Works with or without Facebook
5. **Mobile Optimization**: Works on all devices

### Debug Steps
1. Check Streamlit secrets configuration
2. Verify Facebook app OAuth settings  
3. Test with Facebook app test users
4. Monitor browser network requests
5. Check Streamlit logs for errors
6. Try alternative verification methods

### Best Practices
- Always provide manual registration option
- Use social verification as enhancement, not requirement
- Test thoroughly on mobile devices
- Monitor conversion rates with/without social login

Ready to launch with robust authentication! 🚀
