from flask import Blueprint, request, jsonify, send_file
from datetime import datetime
from sqlalchemy import exc
from app import db, cross_origin
from app.models import CallLog


call_log = Blueprint('call_log', __name__)


@call_log.route('/call_logs', methods=['POST'])
@cross_origin()
def create_call_log():
    data = request.json
    employee_id = data['employee_id']
    dt_employee_id = data['dt_employee_id']
    client_id = data['client_id']
    dt_client_id = data['dt_client_id']
    description = data['description']
    category_id = data['category_id']
    start_date_time = datetime.strptime(
        data['start_date_time'],
        '%d/%m/%Y %H:%M:%S'
    )
    end_date_time = datetime.strptime(
        data['end_date_time'],
        '%d/%m/%Y %H:%M:%S'
    )

    try:
        new_call_log = CallLog(
            employee_id=employee_id,
            client_id=client_id,
            description=description,
            category_id=category_id,
            start_date_time=start_date_time,
            end_date_time=end_date_time,
            dt_client_id=dt_client_id,
            dt_employee_id=dt_employee_id
        )
        db.session.add(new_call_log)
        db.session.commit()
        return jsonify({
            'message': "Llamada registrada exitosamente",
            'status': 200,
            'call_log': new_call_log.to_json()
        })

    except (Exception, exc.SQLAlchemyError) as e:
        return jsonify({
            'message': f"Error al crear el registro de llamada",
            'error': str(e),
            'status': 500,
        })


@call_log.route('/call_logs/<user_type>/<int:document_type_id>/<int:id_user>', methods=['GET'])
@call_log.route('/call_logs/<user_type>', methods=['GET'])
@cross_origin()
def get_call_logs(user_type, id_user=-1, document_type_id=-1):    
    try:
        if user_type == "all":
            call_logs = CallLog.query.all()
        elif user_type == "employee":
            call_logs = CallLog.query.filter_by(employee_id=id_user, dt_employee_id=document_type_id).all()
        elif user_type == "client":
            call_logs = CallLog.query.filter_by(
                client_id=id_user, dt_client_id=document_type_id).all()
        else:
            return jsonify({
                'message': "Tipo de usuario invalido",
                'status': 500
            })
        return jsonify({
            'message': "Registros de llamadas obtenidas exitosamente",
            'status': 200,
            'call_logs': [call_log.to_json() for call_log in call_logs]
        })
    except (Exception, exc.SQLAlchemyError) as e:
        return jsonify({
            'message': f"Error al obtener los registros de llamadas",
            'error': str(e),
            'status': 500,
        })


@call_log.route('/call_logs/<int:id>', methods=['DELETE'])
@cross_origin()
def delete_call_log(id):
    try:
        call_log = CallLog.query.filter_by(ticket=id).first()
        db.session.delete(call_log)
        db.session.commit()
        return jsonify({
            'message': "Registro de llamada eliminado exitosamente",
            'status': 200
        })
    except (Exception, exc.SQLAlchemyError) as e:
        return jsonify({
            'message': f"Error al eliminar el registro de llamada",
            'error': str(e),
            'status': 500,
        })


@call_log.route('/call_logs/<int:id>', methods=['PUT'])
@cross_origin()
def update_call_log(id):
    data = request.json
    try:
        call_log = CallLog.query.filter_by(ticket=id).first()
        call_log.employee_id = data['employee_id']
        call_log.client_id = data['client_id']
        call_log.dt_employee_id = data['dt_employee_id']
        call_log.dt_client_id = data['dt_client_id']
        call_log.description = data['description']
        call_log.category_id = data['category_id']
        call_log.start_date_time = datetime.strptime(
            data['start_date_time'],
            '%d/%m/%y %H:%M:%S'
        )
        call_log.end_date_time = datetime.strptime(
            data['end_date_time'],
            '%d/%m/%y %H:%M:%S'
        )
        db.session.commit()
        return jsonify({
            'message': "Registro de llamada actualizado exitosamente",
            'status': 200
        })
    except (Exception, exc.SQLAlchemyError) as e:
        return jsonify({
            'message': f"Error al actualizar el registro de llamada",
            'error': str(e),
            'status': 500,
        })


@call_log.route('/call_logs/download/<user_type>/<int:document_type_id>/<int:id_user>', methods=['GET'])
@call_log.route('/call_logs/download/<user_type>', methods=['GET'])
@cross_origin()
def download_call_logs_csv(user_type, id_user=-1, document_type_id=-1):
    try:
        if user_type == "all":
            call_logs = CallLog.query.all()
        elif user_type == "employee":
            call_logs = CallLog.query.filter_by(
                employee_id=id_user, dt_employee_id=document_type_id).all()
        elif user_type == "client":
            call_logs = CallLog.query.filter_by(
                client_id=id_user, dt_client_id=document_type_id).all()
        else:
            return jsonify({
                'message': "Tipo de usuario invalido",
                'status': 500
            })
        path_call_logs_csv = CallLog.to_csv(call_logs)
        filename = f"call_logs_{user_type}_{document_type_id}_{id_user}_.csv" if user_type != "all" else f"call_logs_{user_type}.csv"
        return send_file(
            path_call_logs_csv,
            as_attachment=True,
            mimetype='text/csv',
            attachment_filename=filename
        )

    except (Exception, exc.SQLAlchemyError) as e:
        return jsonify({
            'message': f"Error al descargar los registros de llamadas en un csv",
            'error': str(e),
            'status': 500,
        })
