from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fuel_express.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# allow templates to use hasattr
app.jinja_env.globals.update(hasattr=hasattr)

# strftime filter for templates (supports "now" literal)
def jinja_strftime(value, fmt='%B %d, %Y'):
    if isinstance(value, str) and value.lower() == 'now':
        dt = datetime.utcnow()
    elif hasattr(value, 'strftime'):
        dt = value
    else:
        try:
            dt = datetime.fromisoformat(str(value))
        except Exception:
            return ''
    try:
        return dt.strftime(fmt)
    except Exception:
        return ''

app.jinja_env.filters['strftime'] = jinja_strftime

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Database Models
class FuelStation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.Text, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    admins = db.relationship('User', backref='fuel_station', lazy=True)
    daily_prices = db.relationship('DailyFuelPrice', backref='station', lazy=True)

class DailyFuelPrice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    station_id = db.Column(db.Integer, db.ForeignKey('fuel_station.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    petrol_price = db.Column(db.Float, nullable=False)
    diesel_price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('station_id', 'date', name='unique_station_date'),)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    user_type = db.Column(db.String(20), default='user')  # user, admin, delivery_agent, station_admin
    fuel_station_id = db.Column(db.Integer, db.ForeignKey('fuel_station.id'))
    vehicle_number = db.Column(db.String(20))          # for delivery agents
    is_available = db.Column(db.Boolean, default=True) # for delivery agents
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    orders = db.relationship('Order', backref='customer', lazy=True, foreign_keys='Order.user_id')
    assigned_orders = db.relationship('Order', backref='agent', lazy=True, foreign_keys='Order.delivery_agent_id')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'user_type': self.user_type,
            'fuel_station_id': self.fuel_station_id,
            'vehicle_number': self.vehicle_number,
            'is_available': self.is_available,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    fuel_station_id = db.Column(db.Integer, db.ForeignKey('fuel_station.id'), nullable=False)
    fuel_type = db.Column(db.String(20), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    delivery_address = db.Column(db.Text, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')
    total_amount = db.Column(db.Float, nullable=False)
    fuel_price_per_liter = db.Column(db.Float, nullable=False)
    payment_status = db.Column(db.String(20), default='pending')
    payment_id = db.Column(db.String(100))
    delivery_agent_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    delivered_at = db.Column(db.DateTime)

    fuel_station = db.relationship('FuelStation', backref='orders')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'fuel_station_id': self.fuel_station_id,
            'fuel_type': self.fuel_type,
            'quantity': self.quantity,
            'delivery_address': self.delivery_address,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'status': self.status,
            'total_amount': self.total_amount,
            'fuel_price_per_liter': self.fuel_price_per_liter,
            'payment_status': self.payment_status,
            'payment_id': self.payment_id,
            'delivery_agent_id': self.delivery_agent_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'delivered_at': self.delivered_at.isoformat() if self.delivered_at else None,
            'customer_name': self.customer.name if self.customer else None,
            'agent_name': getattr(self.agent, 'name', None) if self.agent else None,
            'station_name': self.fuel_station.name if self.fuel_station else None
        }

@login_manager.user_loader
def load_user(user_id):
    try:
        return db.session.get(User, int(user_id))
    except Exception:
        return None

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fuel-prices')
def fuel_prices():
    return render_template('fuel_prices.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user_type = request.form.get('user_type', 'user')

        user = User.query.filter_by(email=email, user_type=user_type).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            if user.user_type == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif user.user_type == 'station_admin':
                return redirect(url_for('station_dashboard'))
            elif user.user_type == 'delivery_agent':
                return redirect(url_for('delivery_dashboard'))
            else:
                return redirect(url_for('user_dashboard'))
        else:
            flash('Invalid credentials', 'error')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        phone = request.form.get('phone')
        user_type = request.form.get('user_type', 'user')

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered', 'error')
            return render_template('register.html')

        if user_type == 'station_admin':
            station_name = request.form.get('station_name', '')
            station_address = request.form.get('station_address', '')
            station_lat = float(request.form.get('station_latitude', 0))
            station_lng = float(request.form.get('station_longitude', 0))

            if not station_name or not station_address:
                flash('Station name and address are required for station admin', 'error')
                return render_template('register.html')

            fuel_station = FuelStation(
                name=station_name,
                address=station_address,
                latitude=station_lat,
                longitude=station_lng,
                phone=phone,
                email=email
            )
            db.session.add(fuel_station)
            db.session.flush()

            new_user = User(
                name=name,
                email=email,
                password_hash=generate_password_hash(password),
                phone=phone,
                user_type=user_type,
                fuel_station_id=fuel_station.id
            )
        elif user_type == 'delivery_agent':
            vehicle_number = request.form.get('vehicle_number', '')
            new_user = User(
                name=name,
                email=email,
                password_hash=generate_password_hash(password),
                phone=phone,
                user_type=user_type,
                vehicle_number=vehicle_number
            )
        else:
            new_user = User(
                name=name,
                email=email,
                password_hash=generate_password_hash(password),
                phone=phone,
                user_type=user_type
            )

        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/user/dashboard')
@login_required
def user_dashboard():
    if not (current_user.is_authenticated and current_user.user_type == 'user'):
        return redirect(url_for('index'))

    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('user_dashboard.html', orders=orders)

# ...existing code...
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if not (current_user.is_authenticated and current_user.user_type == 'admin'):
        return redirect(url_for('index'))

    orders_objs = Order.query.order_by(Order.created_at.desc()).all()
    users_objs = User.query.filter_by(user_type='user').all()
    agents_objs = User.query.filter_by(user_type='delivery_agent').all()

    stats = {
        'total_orders': len(orders_objs),
        'pending_orders': len([o for o in orders_objs if o.status == 'pending']),
        'completed_orders': len([o for o in orders_objs if o.status == 'completed']),
        'total_users': len(users_objs),
        'total_agents': len(agents_objs)
    }

    # JSON-serializable copies for JavaScript usage in the template
    orders_json = [o.to_dict() for o in orders_objs]
    users_json = [u.to_dict() for u in users_objs]
    agents_json = [a.to_dict() for a in agents_objs]

    # Pass ORM objects for template rendering and separate JSON lists for JS
    return render_template(
        'admin_dashboard.html',
        orders=orders_objs,
        users=users_objs,
        agents=agents_objs,
        stats=stats,
        orders_json=orders_json,
        users_json=users_json,
        agents_json=agents_json
    )
# ...existing code...
@app.route('/delivery/dashboard')
@login_required
def delivery_dashboard():
    if not (current_user.is_authenticated and current_user.user_type == 'delivery_agent'):
        return redirect(url_for('index'))

    assigned_orders = Order.query.filter_by(delivery_agent_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('delivery_dashboard.html', orders=assigned_orders)

@app.route('/station/dashboard')
@login_required
def station_dashboard():
    if not (current_user.is_authenticated and current_user.user_type == 'station_admin'):
        return redirect(url_for('index'))

    station = current_user.fuel_station
    orders = Order.query.filter_by(fuel_station_id=station.id).order_by(Order.created_at.desc()).all()

    today = datetime.utcnow().date()
    today_prices = DailyFuelPrice.query.filter_by(station_id=station.id, date=today).first()

    stats = {
        'total_orders': len(orders),
        'pending_orders': len([o for o in orders if o.status == 'pending']),
        'completed_orders': len([o for o in orders if o.status == 'completed']),
        'today_revenue': sum([o.total_amount for o in orders if o.status == 'completed' and o.created_at.date() == today])
    }

    return render_template('station_dashboard.html', station=station, orders=orders, stats=stats, today_prices=today_prices)

@app.route('/order', methods=['POST'])
@login_required
def create_order():
    if not (current_user.is_authenticated and current_user.user_type == 'user'):
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json()
    station_id = data.get('station_id')
    if not station_id:
        return jsonify({'error': 'Station ID required'}), 400

    station = FuelStation.query.get(station_id)
    if not station:
        return jsonify({'error': 'Invalid station'}), 400

    today = datetime.utcnow().date()
    today_prices = DailyFuelPrice.query.filter_by(station_id=station_id, date=today).first()
    if not today_prices:
        return jsonify({'error': 'No fuel prices set for today'}), 400

    fuel_price = today_prices.petrol_price if data['fuel_type'] == 'petrol' else today_prices.diesel_price
    total_amount = data['quantity'] * fuel_price

    order = Order(
        user_id=current_user.id,
        fuel_station_id=station_id,
        fuel_type=data['fuel_type'],
        quantity=data['quantity'],
        delivery_address=data['delivery_address'],
        latitude=data['latitude'],
        longitude=data['longitude'],
        total_amount=total_amount,
        fuel_price_per_liter=fuel_price
    )

    db.session.add(order)
    db.session.commit()

    return jsonify({'order_id': order.id, 'total_amount': total_amount, 'fuel_price': fuel_price})

@app.route('/payment/<int:order_id>', methods=['POST'])
@login_required
def process_payment(order_id):
    if not (current_user.is_authenticated and current_user.user_type == 'user'):
        return jsonify({'error': 'Unauthorized'}), 403

    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json()
    payment_method = data.get('payment_method', 'online')

    if payment_method == 'online':
        payment_id = f"pay_{order_id}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        order.payment_id = payment_id
        order.payment_status = 'paid'
        db.session.commit()

        return jsonify({
            'success': True,
            'payment_id': payment_id,
            'message': 'Payment processed successfully'
        })
    else:
        order.payment_status = 'pending'
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Order placed. Payment will be collected on delivery.'
        })

@app.route('/admin/assign_order/<int:order_id>', methods=['POST'])
@login_required
def assign_order(order_id):
    if not (current_user.is_authenticated and current_user.user_type == 'admin'):
        return jsonify({'error': 'Unauthorized'}), 403

    order = Order.query.get_or_404(order_id)
    agent_id = request.json.get('agent_id')

    agent = User.query.get(agent_id)
    if not agent or agent.user_type != 'delivery_agent':
        return jsonify({'error': 'Invalid agent'}), 400

    order.delivery_agent_id = agent_id
    order.status = 'assigned'
    db.session.commit()

    return jsonify({'success': True})

@app.route('/delivery/update_status/<int:order_id>', methods=['POST'])
@login_required
def update_delivery_status(order_id):
    if not (current_user.is_authenticated and current_user.user_type == 'delivery_agent'):
        return jsonify({'error': 'Unauthorized'}), 403

    order = Order.query.get_or_404(order_id)
    if order.delivery_agent_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    new_status = request.json.get('status')
    order.status = new_status

    if new_status == 'completed':
        order.delivered_at = datetime.utcnow()

    db.session.commit()

    return jsonify({'success': True})

@app.route('/api/orders')
@login_required
def get_orders():
    if current_user.user_type == 'user':
        orders = Order.query.filter_by(user_id=current_user.id).all()
    elif current_user.user_type == 'admin':
        orders = Order.query.all()
    elif current_user.user_type == 'delivery_agent':
        orders = Order.query.filter_by(delivery_agent_id=current_user.id).all()
    else:
        return jsonify({'error': 'Unauthorized'}), 403

    orders_data = []
    for order in orders:
        orders_data.append({
            'id': order.id,
            'fuel_type': order.fuel_type,
            'quantity': order.quantity,
            'delivery_address': order.delivery_address,
            'status': order.status,
            'total_amount': order.total_amount,
            'created_at': order.created_at.isoformat() if order.created_at else None,
            'customer_name': order.customer.name if order.customer else 'Unknown',
            'agent_name': order.agent.name if order.agent else None
        })

    return jsonify(orders_data)

@app.route('/station/update_prices', methods=['POST'])
@login_required
def update_daily_prices():
    if not (current_user.is_authenticated and current_user.user_type == 'station_admin'):
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json()
    station_id = current_user.fuel_station_id
    today = datetime.utcnow().date()

    existing_prices = DailyFuelPrice.query.filter_by(station_id=station_id, date=today).first()

    if existing_prices:
        existing_prices.petrol_price = data['petrol_price']
        existing_prices.diesel_price = data['diesel_price']
    else:
        new_prices = DailyFuelPrice(
            station_id=station_id,
            date=today,
            petrol_price=data['petrol_price'],
            diesel_price=data['diesel_price']
        )
        db.session.add(new_prices)

    db.session.commit()
    return jsonify({'success': True, 'message': 'Prices updated successfully'})

@app.route('/api/fuel_stations')
def get_fuel_stations():
    stations = FuelStation.query.filter_by(is_active=True).all()
    stations_data = []

    for station in stations:
        today = datetime.utcnow().date()
        today_prices = DailyFuelPrice.query.filter_by(station_id=station.id, date=today).first()

        stations_data.append({
            'id': station.id,
            'name': station.name,
            'address': station.address,
            'latitude': station.latitude,
            'longitude': station.longitude,
            'phone': station.phone,
            'petrol_price': today_prices.petrol_price if today_prices else None,
            'diesel_price': today_prices.diesel_price if today_prices else None
        })

    return jsonify(stations_data)

@app.route('/api/fuel_prices')
def get_fuel_prices():
    today = datetime.utcnow().date()
    prices = DailyFuelPrice.query.filter_by(date=today).join(FuelStation).filter(FuelStation.is_active == True).all()

    prices_data = []
    for price in prices:
        prices_data.append({
            'station_name': price.station.name,
            'station_address': price.station.address,
            'petrol_price': price.petrol_price,
            'diesel_price': price.diesel_price,
            'date': price.date.isoformat()
        })

    return jsonify(prices_data)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        admin = User.query.filter_by(email='admin@fuel-express.com').first()
        if not admin:
            admin = User(
                name='Admin',
                email='admin@fuel-express.com',
                password_hash=generate_password_hash('admin123'),
                user_type='admin'
            )
            db.session.add(admin)

        if not FuelStation.query.first():
            stations = [
                FuelStation(
                    name='City Fuel Station',
                    address='123 Main Street, City Center',
                    latitude=19.0760,
                    longitude=72.8777,
                    phone='+91-9876543210',
                    email='cityfuel@example.com'
                ),
                FuelStation(
                    name='Highway Fuel Stop',
                    address='456 Highway Road, Industrial Area',
                    latitude=19.0760,
                    longitude=72.8777,
                    phone='+91-9876543211',
                    email='highwayfuel@example.com'
                ),
                FuelStation(
                    name='Metro Fuel Center',
                    address='789 Metro Plaza, Business District',
                    latitude=19.0760,
                    longitude=72.8777,
                    phone='+91-9876543212',
                    email='metrofuel@example.com'
                )
            ]

            for station in stations:
                db.session.add(station)

            db.session.flush()

            today = datetime.utcnow().date()
            for station in stations:
                daily_price = DailyFuelPrice(
                    station_id=station.id,
                    date=today,
                    petrol_price=100.0,
                    diesel_price=95.0
                )
                db.session.add(daily_price)

        db.session.commit()

    app.run(debug=True)