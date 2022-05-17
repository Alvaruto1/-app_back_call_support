from app import db
from app.models.user.role_user import role_user_table


class Role(db.Model):

    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True)
    users = db.relationship(
        'User',
        secondary=role_user_table,
        back_populates='roles'
    )
