from app import db


class Category(db.Model):
    
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True)
    call_logs = db.relationship('CallLog')
    