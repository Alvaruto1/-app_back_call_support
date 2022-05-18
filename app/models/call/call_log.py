import os
from app import db
from app.models.call.category import Category
from app.models.user.user import User
from pandas import DataFrame as df


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
    dt_employee_id = db.Column(
        db.Integer,
        db.ForeignKey('user.document_type_id'),
        nullable=False
    )
    dt_client_id = db.Column(
        db.Integer,
        db.ForeignKey('user.document_type_id'),
        nullable=False
    )
    category_id = db.Column(
        db.Integer, db.ForeignKey('category.id'),
        nullable=False
    )

    employee_f_id = db.relationship('User', foreign_keys=[employee_id])
    employee_dt_id = db.relationship(
        'User', foreign_keys=[dt_employee_id])
    client_f_id = db.relationship('User', foreign_keys=[client_id])
    client_dt_id = db.relationship('User', foreign_keys=[dt_client_id])

    def to_json(self):
        return {
            'ticket': self.ticket,
            'start_date_time': self.start_date_time,
            'end_date_time': self.end_date_time,
            'description': self.description,
            'client': User.query.filter_by(id=self.client_id).first().to_json(),
            'employee': User.query.filter_by(id=self.employee_id, document_type_id=self.dt_employee_id).first().to_json(),
            'category': Category.query.filter_by(id=self.category_id).first().to_json()
        }

    @staticmethod
    def to_csv(call_logs):
        list_call_logs = [call_log.to_json() for call_log in call_logs]
        list_call_logs = map(lambda call_log: {
            'ticket': call_log['ticket'],
            'start_date_time': call_log['start_date_time'],
            'end_date_time': call_log['end_date_time'],
            'description': call_log['description'],
            'client': f"{call_log['client']['name']} {call_log['client']['surname']}",
            'client_id': call_log['client']['id'],
            'employee': f"{call_log['employee']['name']} {call_log['employee']['surname']}",
            'employee_id': call_log['employee']['id'],
            'dt_employee': call_log['employee']['document_type_id']['name'],
            'dt_client': call_log['client']['document_type_id']['name'],
            'category': call_log['category']['name']
        }, list_call_logs)
        df_call_logs = df(list_call_logs)
        path_call_log_csv = os.path.join("downloads", "call_logs.csv")
        try:
            df_call_logs.to_csv(os.path.join(
                "app", path_call_log_csv), index=False, encoding='utf-8', sep=';')
            return path_call_log_csv
        except Exception as e:
            print(e)
            return False
