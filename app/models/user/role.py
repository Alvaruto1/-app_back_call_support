from app import db


class Role(db.Model):

    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name
        }