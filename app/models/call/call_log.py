from app import db


class CallLog(db.Model):

    __tablename__ = 'call_log'
    ticket = db.Column(db.Integer, primary_key=True)
    start_date_time = db.Column(db.DateTime, nullable=False)
    end_date_time = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    employee_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False
    )
    category_id = db.Column(
        db.Integer, db.ForeignKey('category.id'),
        nullable=False
    )
