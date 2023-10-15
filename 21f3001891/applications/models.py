from applications.database import db

class Users(db.Model):
    __tablename__ = 'users'
    Username = db.Column(db.String, unique=True, primary_key=True)
    Password = db.Column(db.String, nullable=False)

class Admins(db.Model):
    __tablename__ = 'admins'
    Username = db.Column(db.String, unique=True, primary_key=True)
    Password = db.Column(db.String, nullable=False)

class Categories(db.Model):
    __tablename__ = 'categories'
    cid = db.Column(db.Integer, unique=True, autoincrement=True, primary_key=True)
    cname = db.Column(db.String, unique=True, nullable=False)
    cimage = db.Column(db.String)

class Products(db.Model):
    __tablename__ = 'products'
    pid = db.Column(db.Integer, unique=True, autoincrement=True, primary_key=True)
    pname = db.Column(db.String, unique=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    manufacturing_date= db.Column(db.String, nullable=False)
    expdate= db.Column(db.String, nullable=False)
    cname= db.Column(db.String, nullable=False)
    pimage = db.Column(db.String, nullable=False)

class Cart(db.Model):
    __tablename__ = 'cart'
    username = db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.Integer, nullable=False)
    pname = db.Column(db.String, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    cname= db.Column(db.String, nullable=False)