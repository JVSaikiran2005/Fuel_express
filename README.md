# Fuel Express - Fuel Delivery Management System

Fuel Express is a comprehensive web-based fuel delivery management system that enables users to order fuel directly to their GPS-tracked location. The system features three distinct interfaces for users, administrators, and delivery agents, providing a complete solution for fuel delivery operations.

## 🚀 Features

### User Interface
- **User Registration & Authentication**: Secure login system with email and password
- **GPS Location Tracking**: Automatic location detection for accurate fuel delivery
- **Order Placement**: Easy fuel ordering with quantity selection and address confirmation
- **Real-time Tracking**: Monitor delivery status and progress
- **Order History**: View past orders with timestamps and delivery details
- **Secure Payments**: Integrated payment options (credit/debit card, UPI)

### Admin Interface
- **Dashboard Analytics**: Overview of orders, users, and delivery statistics
- **Order Management**: Monitor and manage all orders across the platform
- **User Management**: View and manage customer accounts
- **Agent Assignment**: Assign delivery agents to active orders
- **Status Updates**: Track delivery progress and update order status
- **Reports**: Generate analytics and revenue reports

### Delivery Agent Interface
- **Order Assignment**: View assigned delivery requests
- **GPS Navigation**: Access customer locations for real-time navigation
- **Status Updates**: Update order status after delivery completion
- **Mobile-Friendly**: Responsive design for mobile and desktop access

## 🛠️ Technology Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Backend**: Python 3.8+ with Flask framework
- **Database**: SQLite (development) / PostgreSQL (production)
- **Authentication**: Flask-Login with password hashing
- **Maps Integration**: Google Maps API for GPS tracking
- **Payment Gateway**: Razorpay integration
- **UI Framework**: Bootstrap 5 with custom styling

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git (for version control)

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd fuel-express
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the root directory with the following variables:
```env
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
DATABASE_URL=sqlite:///fuel_express.db
GOOGLE_MAPS_API_KEY=your-google-maps-api-key
RAZORPAY_KEY_ID=your-razorpay-key-id
RAZORPAY_KEY_SECRET=your-razorpay-key-secret
```

### 5. Initialize Database
```bash
python app.py
```
The application will automatically create the database and tables on first run.

### 6. Run the Application
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## 👥 Default Accounts

### Admin Account
- **Email**: admin@fuel-express.com
- **Password**: admin123

### Test User Account
Register a new account through the registration page.

### Delivery Agent Account
Register a new delivery agent account through the registration page.

## 🗂️ Project Structure

```
fuel-express/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── README.md            # Project documentation
├── templates/           # HTML templates
│   ├── base.html        # Base template
│   ├── index.html       # Home page
│   ├── login.html       # Login page
│   ├── register.html    # Registration page
│   ├── user_dashboard.html      # User dashboard
│   ├── admin_dashboard.html     # Admin dashboard
│   └── delivery_dashboard.html  # Delivery agent dashboard
└── static/              # Static files
    ├── style.css        # Custom CSS styles
    └── script.js        # JavaScript functions
```

## 🔧 Configuration

### Google Maps API Setup
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Maps JavaScript API and Geocoding API
4. Create credentials (API Key)
5. Add the API key to your `.env` file

### Razorpay Payment Integration
1. Sign up at [Razorpay](https://razorpay.com/)
2. Get your Key ID and Key Secret from the dashboard
3. Add them to your `.env` file

## 🚀 Deployment

### Production Deployment
1. Set `FLASK_ENV=production` in your environment
2. Use a production WSGI server like Gunicorn
3. Configure a reverse proxy with Nginx
4. Use PostgreSQL for production database
5. Set up SSL certificates for HTTPS

### Docker Deployment
```bash
# Build the Docker image
docker build -t fuel-express .

# Run the container
docker run -p 5000:5000 fuel-express
```

## 📱 Mobile Responsiveness

The application is fully responsive and works seamlessly on:
- Desktop computers
- Tablets
- Mobile phones
- Various screen sizes and orientations

## 🔒 Security Features

- Password hashing with Werkzeug
- CSRF protection with Flask-WTF
- Input validation and sanitization
- Secure session management
- Role-based access control

## 🧪 Testing

Run the application and test the following features:
1. User registration and login
2. Order placement with GPS location
3. Admin order management
4. Delivery agent order assignment
5. Real-time status updates

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

## 🔮 Future Enhancements

- Real-time notifications with WebSocket
- Mobile app development
- Advanced analytics and reporting
- Multi-language support
- Integration with more payment gateways
- Advanced GPS tracking with route optimization
- Customer reviews and ratings system

---

**Fuel Express** - Making fuel delivery simple, safe, and efficient! ⛽
   pip install -r requirements.txt
   ```

3. **Start the application:**
   ```bash
   python run.py
   ```
   OR
   ```bash
   start.bat  # For Windows
   ```

4. **Access the application:**
   - Open your browser and go to `http://localhost:5000`
   - Use admin account: `admin@fuel-express.com` / `admin123`

### 📁 **Project Structure:**
- Complete Flask application with all routes and functionality
- Responsive HTML templates for all user interfaces
- Modern CSS styling with animations
- JavaScript for GPS tracking and real-time updates
- Database models for users, orders, and delivery agents
- Comprehensive documentation and setup instructions

### 🎯 **Key Features Working:**
- ✅ GPS location detection and address fetching
- ✅ Order placement with real-time calculation
- ✅ Admin order assignment to delivery agents
- ✅ Delivery status tracking and updates
- ✅ Payment processing integration ready
- ✅ Responsive design for all devices
- ✅ Secure authentication system
- ✅ Database management with proper relationships

The application is now **fully functional** and ready to use! You can start placing fuel orders, managing them through the admin panel, and tracking deliveries through the agent interface. All the core functionality you requested has been implemented with a modern, professional interface.
   python run.py
   



