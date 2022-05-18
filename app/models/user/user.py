import os
from app import db
from app.models.user.document_type import DocumentType
from app.models.user.role_user import role_user_table
from pandas import DataFrame as df


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
        secondary=role_user_table
    )

    def to_json(self):
        return {
            'id': self.id,
            'document_type_id': DocumentType.query.filter_by(id=self.document_type_id).first().to_json(),
            'name': self.name,
            'surname': self.surname,
            'email': self.email,
            'telephone': self.telephone,
            'roles': [role.to_json() for role in self.roles]
        }

    @staticmethod
    def to_csv(users):
        list_users = [user.to_json() for user in users]
        list_users = map(lambda user: {
            'id': user['id'],
            'document_type_id': user['document_type_id']['name'],
            'name': user['name'],
            'surname': user['surname'],
            'email': user['email'],
            'telephone': user['telephone'],
            'roles': (', ').join([role['name'] for role in user['roles']])
        }, list_users)
        df_users = df(list_users)
        path_user_csv = os.path.join("downloads", "users.csv")
        try:
            df_users.to_csv(os.path.join("app", path_user_csv), index=False, encoding='utf-8', sep=';')
            return path_user_csv
        except Exception as e:
            print(e)
            return False

