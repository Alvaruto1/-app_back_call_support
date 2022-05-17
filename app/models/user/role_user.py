from app import db


role_user_table = db.Table(
    'role_user',
    db.Base.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)
