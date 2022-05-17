from app import db


class DocumentType(db.Model):

    __tablename__ = 'document_type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    users = db.relationship('User')
