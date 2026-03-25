from datetime import datetime
from flask_login import UserMixin
from app import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(10), nullable=False, default='user')
    is_premium = db.Column(db.Boolean, default=False, nullable=False)
    hostel_room = db.Column(db.String(100), nullable=True)
    contact_no = db.Column(db.String(15), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    orders = db.relationship('Order', backref='customer', lazy=True)
    reviews = db.relationship('Review', backref='author', lazy=True)
    payments = db.relationship('Payment', backref='payer', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        from itsdangerous import URLSafeTimedSerializer as Serializer
        from flask import current_app
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id})

    @staticmethod
    def verify_reset_token(token):
        from itsdangerous import URLSafeTimedSerializer as Serializer
        from flask import current_app
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token, max_age=1800)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.role}')"

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    base_price = db.Column(db.Float, nullable=False)
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.id'), nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)

    order_items = db.relationship('OrderItem', backref='service', lazy=True)
    reviews = db.relationship('Review', backref='service_reviewed', lazy=True)

    def __repr__(self):
        return f"Service('{self.name}', ₹{self.base_price})"

class Shop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    rating = db.Column(db.Float, default=5.0)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    serviceable_pincodes = db.Column(db.String(500), default="110001,110002") # Comma separated
    services = db.relationship('Service', backref='shop', lazy=True)

    def __repr__(self):
        return f"Shop('{self.name}', '{self.location}')"

    def recalculate_rating(self):
        ratings = [o.rating for o in Order.query.filter_by(shop_id=self.id).filter(Order.rating.isnot(None)).all()]
        if ratings:
            self.rating = round(sum(ratings) / len(ratings), 1)
        else:
            self.rating = 5.0
        db.session.commit()

class Coupon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    discount_type = db.Column(db.String(10), nullable=False)
    discount_value = db.Column(db.Float, nullable=False)
    min_purchase = db.Column(db.Float, nullable=False, default=0.0)
    active = db.Column(db.Boolean, default=True)
    expiry_date = db.Column(db.DateTime, nullable=True)

    orders = db.relationship('Order', backref='coupon', lazy=True)

    def is_valid(self):
        from datetime import datetime
        if not self.active:
            return False
        if self.expiry_date and datetime.utcnow() > self.expiry_date:
            return False
        return True

    def apply_discount(self, amount):
        if self.discount_type == 'percent':
            return max(0.0, amount * (1 - self.discount_value / 100.0))
        return max(0.0, amount - self.discount_value)

    def __repr__(self):
        return f"Coupon('{self.code}', {self.discount_type}, {self.discount_value})"

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.id'), nullable=True)
    coupon_id = db.Column(db.Integer, db.ForeignKey('coupon.id'), nullable=True)
    tracking_code = db.Column(db.String(40), nullable=False, unique=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(30), nullable=False, default='Pending')
    total_price = db.Column(db.Float, nullable=False)
    pickup_address = db.Column(db.String(255), nullable=False)
    pickup_date = db.Column(db.String(20), nullable=False)
    pickup_time = db.Column(db.String(20), nullable=False)
    special_instructions = db.Column(db.Text, nullable=True)
    items_json = db.Column(db.Text, nullable=False) # Stores order items as dynamic JSON
    
    rating = db.Column(db.Integer, nullable=True)
    review_comments = db.Column(db.Text, nullable=True)

    shop = db.relationship('Shop', backref='orders', lazy=True)
    order_items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')
    payments = db.relationship('Payment', backref='order', lazy=True)

    def __repr__(self):
        return f"Order('{self.id}', '{self.status}', ₹{self.total_price})"

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    garment_type = db.Column(db.String(50), nullable=False, default='Other')
    quantity = db.Column(db.Integer, nullable=False, default=1)
    unit_price = db.Column(db.Float, nullable=False)
    sub_total = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"OrderItem('{self.service.name}', qty={self.quantity}, subtotal=₹{self.sub_total})"

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    method = db.Column(db.String(30), nullable=False, default='mock')
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(30), nullable=False, default='Pending')
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Payment('Order {self.order_id}', ₹{self.amount}, '{self.status}')"

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Review('Service {self.service_id}', rating={self.rating})"

class ShopReview(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('shop_reviews', lazy=True))

    def __repr__(self):
        return f"ShopReview('{self.user_id}', rating={self.rating})"

class Franchise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    contact_no = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    investment = db.Column(db.String(50), nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Franchise('{self.full_name}', '{self.city}', '{self.email}')"
