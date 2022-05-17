from app import db
from app.models.user.role_user import role_user_table


class User(db.Model):
    
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    document_type_id = db.Column(
        db.Integer,
        db.ForeignKey('document_type.id'),
        primary_key=True
    )
    name = db.Column(db.String(40), nullable=False)
    surname = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
    telephone = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(120), nullable=False)

    roles = db.relationship(
        'Role',
        secondary=role_user_table,
        back_populates='users'
    )

    call_logs = db.relationship('CallLog')
