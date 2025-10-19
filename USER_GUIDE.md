# Fuel Express - Complete User Guide

## 🎉 Enhanced Fuel Express System

Your Fuel Express application now includes all the requested features:

### ✅ **Admin can register through fuel stations**
### ✅ **Web server runner functionality** 
### ✅ **Delivery task assignment to delivery agents**
### ✅ **Daily fuel price changes visible to users**

---

## 🚀 Quick Start Guide

### 1. **Start the Application**
```bash
# Navigate to project directory
cd "D:\Fuel express"

# Start the application
python run.py
```

### 2. **Access the Application**
- Open your browser and go to: `http://localhost:5000`
- The application will automatically create sample data on first run

---

## 👥 User Types & Registration

### **1. Customer (Regular User)**
- **Purpose**: Order fuel for delivery
- **Registration**: Select "Customer" during registration
- **Features**: 
  - View daily fuel prices from all stations
  - Place orders with GPS location tracking
  - Track order status in real-time
  - View order history

### **2. Fuel Station Admin**
- **Purpose**: Manage fuel station and daily prices
- **Registration**: Select "Fuel Station Admin" during registration
- **Required Information**:
  - Personal details (name, email, phone)
  - Station name and address
  - GPS coordinates (latitude, longitude)
- **Features**:
  - Update daily fuel prices
  - Monitor station orders
  - Track revenue and statistics
  - Manage station information

### **3. Delivery Agent**
- **Purpose**: Deliver fuel orders to customers
- **Registration**: Select "Delivery Agent" during registration
- **Required Information**:
  - Personal details
  - Vehicle number
- **Features**:
  - View assigned delivery tasks
  - Update delivery status
  - Access customer GPS locations
  - Track delivery progress

### **4. System Admin**
- **Purpose**: Manage the entire system
- **Default Account**: 
  - Email: `admin@fuel-express.com`
  - Password: `admin123`
- **Features**:
  - Monitor all orders and users
  - Assign delivery agents to orders
  - Manage fuel stations
  - Generate reports and analytics

---

## 🏪 Fuel Station Management

### **For Station Admins:**

#### **Setting Up Your Station:**
1. Register as "Fuel Station Admin"
2. Provide complete station information:
   - Station name (e.g., "City Fuel Station")
   - Full address
   - GPS coordinates (get from Google Maps)
3. Your station will be automatically activated

#### **Managing Daily Prices:**
1. Login to your station dashboard
2. Click "Update Prices" button
3. Set current petrol and diesel prices
4. Prices are immediately available for new orders
5. Update prices anytime during the day

#### **Monitoring Performance:**
- View total orders from your station
- Track pending and completed orders
- Monitor daily revenue
- See order details and customer information

---

## ⛽ Daily Fuel Price System

### **How It Works:**
1. **Station Admins** update prices daily
2. **Prices are locked** at the time of order placement
3. **Users see current prices** before ordering
4. **Price comparison** available across all stations

### **For Users:**
1. **View Current Prices**: Visit the "Fuel Prices" page
2. **Compare Stations**: See prices from all active stations
3. **Real-time Updates**: Prices update automatically
4. **Transparent Pricing**: No hidden charges

### **For Station Admins:**
1. **Daily Updates**: Set prices each morning
2. **Flexible Pricing**: Adjust based on market conditions
3. **Price History**: All changes are tracked
4. **Competitive Analysis**: See other station prices

---

## 📱 User Interface Guide

### **Home Page**
- Overview of Fuel Express features
- Quick access to registration and login
- Information about the service

### **Fuel Prices Page**
- Current prices from all stations
- Station comparison
- Price update information
- Accessible to everyone (no login required)

### **User Dashboard**
- Order placement with station selection
- Real-time price display
- GPS location tracking
- Order history and tracking

### **Station Admin Dashboard**
- Station information management
- Daily price updates
- Order monitoring
- Revenue analytics

### **Delivery Agent Dashboard**
- Assigned delivery tasks
- Customer location access
- Status update tools
- Delivery tracking

### **System Admin Dashboard**
- Complete system overview
- Order management
- User management
- Delivery agent assignment

---

## 🔄 Complete Workflow

### **Order Placement Process:**
1. **User** logs in and goes to dashboard
2. **User** clicks "New Order"
3. **User** selects fuel station from dropdown
4. **System** displays current prices for selected station
5. **User** selects fuel type and quantity
6. **System** calculates total with current prices
7. **User** confirms delivery address (GPS auto-detected)
8. **User** places order and makes payment
9. **Order** is sent to station admin for processing

### **Order Fulfillment Process:**
1. **Station Admin** sees new order in dashboard
2. **System Admin** assigns delivery agent to order
3. **Delivery Agent** receives assignment notification
4. **Delivery Agent** starts delivery and updates status
5. **Customer** tracks delivery in real-time
6. **Delivery Agent** completes delivery
7. **Order** marked as completed

### **Price Management Process:**
1. **Station Admin** logs into dashboard
2. **Station Admin** clicks "Update Prices"
3. **Station Admin** sets new petrol and diesel prices
4. **Prices** are immediately available for new orders
5. **Users** can see updated prices on fuel prices page
6. **All price changes** are tracked with timestamps

---

## 🛠️ Technical Features

### **GPS Integration:**
- Automatic location detection
- Address auto-completion
- Delivery location tracking
- Distance calculation

### **Real-time Updates:**
- Live price updates
- Order status tracking
- Delivery progress monitoring
- Revenue analytics

### **Security Features:**
- Password hashing
- Role-based access control
- Session management
- Input validation

### **Database Management:**
- Automatic table creation
- Sample data initialization
- Relationship management
- Data integrity

---

## 📊 Sample Data

The system comes with pre-loaded sample data:

### **Sample Fuel Stations:**
1. **City Fuel Station** - 123 Main Street, City Center
2. **Highway Fuel Stop** - 456 Highway Road, Industrial Area  
3. **Metro Fuel Center** - 789 Metro Plaza, Business District

### **Default Prices:**
- **Petrol**: ₹100.00 per liter
- **Diesel**: ₹95.00 per liter

### **Admin Account:**
- **Email**: admin@fuel-express.com
- **Password**: admin123

---

## 🚀 Getting Started

### **For New Users:**
1. Visit `http://localhost:5000`
2. Click "Register" 
3. Choose your account type
4. Fill in required information
5. Login and start using the system

### **For Station Owners:**
1. Register as "Fuel Station Admin"
2. Provide complete station details
3. Set your daily fuel prices
4. Start receiving orders

### **For Delivery Agents:**
1. Register as "Delivery Agent"
2. Provide vehicle information
3. Wait for order assignments
4. Complete deliveries and update status

---

## 🎯 Key Benefits

### **For Station Owners:**
- ✅ Complete control over pricing
- ✅ Direct customer management
- ✅ Revenue tracking and analytics
- ✅ Easy price updates

### **For Customers:**
- ✅ Transparent pricing
- ✅ Station choice and comparison
- ✅ Real-time order tracking
- ✅ Convenient fuel delivery

### **For Delivery Agents:**
- ✅ Clear task assignments
- ✅ GPS navigation support
- ✅ Easy status updates
- ✅ Mobile-friendly interface

### **For System:**
- ✅ Scalable architecture
- ✅ Real-time data updates
- ✅ Comprehensive analytics
- ✅ Secure and reliable

---

## 🆘 Support & Troubleshooting

### **Common Issues:**

1. **Application won't start:**
   - Ensure Python 3.8+ is installed
   - Install dependencies: `pip install -r requirements.txt`
   - Check if port 5000 is available

2. **Database errors:**
   - Delete `fuel_express.db` file and restart
   - Application will recreate database automatically

3. **GPS not working:**
   - Allow location access in browser
   - Use HTTPS for production deployment

4. **Prices not updating:**
   - Check if station admin is logged in
   - Verify price update was successful
   - Refresh the fuel prices page

### **Getting Help:**
- Check the console for error messages
- Review the application logs
- Ensure all dependencies are installed
- Verify database permissions

---

## 🎉 Congratulations!

Your Fuel Express system is now fully enhanced with:

✅ **Fuel station registration and management**  
✅ **Daily fuel price management**  
✅ **Real-time price updates**  
✅ **Enhanced delivery task assignment**  
✅ **Web server runner functionality**  
✅ **Complete user interface**  
✅ **GPS tracking and location services**  
✅ **Payment integration ready**  
✅ **Responsive design for all devices**  

**Your fuel delivery management system is ready for production use!** 🚀⛽

---

*For technical support or feature requests, please refer to the project documentation or contact the development team.*


