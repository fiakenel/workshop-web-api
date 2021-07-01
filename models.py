from flask_sqlalchemy import SQLAlchemy
import enum

db = SQLAlchemy()

class Client(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(90), nullable=False)
    phone = db.Column(db.Numeric(10,0), nullable=False, unique=True)
    orders = db.relationship('Order',
                             lazy='select',
                             backref=db.backref('client', lazy='joined'))

    def __repr__(self):
        return '<Клієнт {}>'.format(self.name)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Client.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

prod_order_rs = db.Table('prod_order_rs',
                    db.Column('order_id', db.Integer, db.ForeignKey('orders.id'), primary_key=True),
                    db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True))

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    products = db.relationship('Product',
                               secondary=prod_order_rs,
                               lazy='select',
                               backref=db.backref('order', lazy='select'))

    def __repr__(self):
        return '<Замовлення від {}>'.format(self.date)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Order.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(90), nullable=False, unique=True)
    price = db.Column(db.Numeric(5,2), nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'), nullable=False)
    comments = db.relationship('Comment',
                               lazy='select',
                               backref=db.backref('product', lazy='joined'))

    def __repr__(self):
        return '<Товар {}>'.format(self.name)

class Country(db.Model):
    __tablename__ = 'countries'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(90), nullable=False, unique=True)

    def __repr__(self):
        return '<Країна {}>'.format(self.name)

class Rating(enum.Enum):
    one = 1
    two = 2
    three = 3
    four = 4
    five = 5

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    rating = db.Column(db.Enum(Rating), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
