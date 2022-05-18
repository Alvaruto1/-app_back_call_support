import os
from flask import Blueprint, request, jsonify, send_file, session, send_from_directory
from sqlalchemy import exc
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required
from app import db, cross_origin
from app.models import User, Role

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
@cross_origin()
def login():
    data = request.json
    email = data['email']
    password = data['password']

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({
            'message': "Email incorrecto o contraseña erronea",
            'status': 401
        })
    return jsonify({
        'message': "Login exitoso",
        'status': 200,
        'user': user.to_json(),
        'token': create_access_token(identity=user.id)
    })


@auth.route('/logged_in', methods=['GET'])
@cross_origin()
@jwt_required()
def logged_in():
    return jsonify({
        'message': "Usuario logueado",
        'status': 200,
        'is_logged_in': True
    })


@auth.route('/signup', methods=['POST'])
@cross_origin()
def signup():
    data = request.json
    email = data['email']
    password = data['password']
    name = data['name']
    surname = data['surname']
    telephone = data['telephone']
    document_type_id = data['document_type_id']
    id = data['id']
    role = data['role_name']

    try:
        new_user = User(
            email=email,
            name=name,
            surname=surname,
            telephone=telephone,
            document_type_id=document_type_id,
            password=generate_password_hash(password, method='sha256'),
            id=id
        )
        role = Role.query.filter_by(name=role).first()
        new_user.roles.append(role)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({
            'message': "Usuario creado exitosamente",
            'status': 200,
            'user': new_user.to_json(),
            'token': create_access_token(identity=new_user.id)
        })
    except (Exception, exc.SQLAlchemyError) as e:
        return jsonify({
            'message': f"Error al crear el usuario",
            'status': 500,
            'error': str(e)
        })


@auth.route('/users/<user_type>', methods=['GET'])
@cross_origin()
def get_users(user_type="all"):
    users = None
    try:
        if user_type == "all":
            users = User.query.all()
        elif user_type == "employee":
            users = User.query.join(Role, User.roles).filter_by(id=2).all()
        elif user_type == "client":
            users = User.query.join(Role, User.roles).filter_by(id=1).all()
        else:
            return jsonify({
                'message': "Tipo de usuario invalido",
                'status': 500
            })
        return jsonify({
            'message': "Usuarios obtenidos exitosamente",
            'status': 200,
            'users': [user.to_json() for user in users]
        })
    except (Exception, exc.SQLAlchemyError) as e:
        return jsonify({
            'message': f"Error al obtener los usuarios",
            'status': 500,
            'error': str(e)
        })


@auth.route('/users/<int:type_document_id>/<int:user_id>', methods=['DELETE'])
@cross_origin()
def delete_user(user_id, type_document_id):
    try:
        user = User.query.filter_by(
            id=user_id,
            document_type_id=type_document_id
        ).first()
        db.session.delete(user)
        db.session.commit()
        return jsonify({
            'message': "Usuario eliminado exitosamente",
            'status': 200
        })
    except (Exception, exc.SQLAlchemyError) as e:
        return jsonify({
            'message': f"Error al eliminar el usuario",
            'status': 500,
            'error': str(e)
        })


@auth.route('/users/<int:type_document_id>/<int:user_id>', methods=['PUT'])
@cross_origin()
def update_user(user_id, type_document_id):
    try:
        user = User.query.filter_by(
            id=user_id, 
            document_type_id=type_document_id
        ).first()
        data = request.json
        user.email = data['email']
        user.name = data['name']
        user.surname = data['surname']
        user.telephone = data['telephone']
        user.document_type_id = data['document_type_id']
        user.password = generate_password_hash(
            data['password'], method='sha256')
        db.session.commit()
        return jsonify({
            'message': "Usuario actualizado exitosamente",
            'status': 200,
            'user': user.to_json()
        })
    except (Exception, exc.SQLAlchemyError) as e:
        return jsonify({
            'message': f"Error al actualizar el usuario",
            'status': 500,
            'error': str(e)
        })


@auth.route('/users/search/<int:type_document_id>/<int:user_id>', methods=['GET'])
@cross_origin()
def get_user_by_document(type_document_id, user_id):
    try:
        user = User.query.filter_by(
            document_type_id=type_document_id, id=user_id).first()
        return jsonify({
            'message': "Usuario obtenido exitosamente",
            'status': 200,
            'user': user.to_json()
        })
    except (Exception, exc.SQLAlchemyError) as e:
        return jsonify({
            'message': f"Error al obtener el usuario",
            'status': 500,
            'error': str(e)
        })


@auth.route('/users/download/<int:type_document_id>/<int:user_id>', methods=['GET'])
@cross_origin()
def download_info_user_csv(type_document_id, user_id):
    user = User.query.filter_by(
        document_type_id=type_document_id,
        id=user_id
    ).first()
    user_json = user.to_json()
    document_type_name = user_json['document_type_id']['name']
    path_user_csv = User.to_csv([user])

    if not path_user_csv:
        raise ValueError("No se pudo generar el archivo")

    try:
        return send_file(
            path_user_csv,
            mimetype='text/csv',
            attachment_filename=f"info_user_{document_type_name}_{user_id}.csv",
            as_attachment=True
        )
    except (Exception, exc.SQLAlchemyError) as e:
        return jsonify({
            'message': f"Error al descargar el csv del usuario",
            'status': 500,
            'error': str(e)
        })


@auth.route('/users/download/<user_type>', methods=['GET'])
@auth.route('/users/download/', methods=['GET'])
@cross_origin()
def download_info_users_csv(user_type="all"):
    if user_type == "all":
        users = User.query.all()
    else:
        users = User.query.join(Role, User.roles).filter_by(
            name="Cliente" if user_type == "client" else "Empleado"
        ).all()
    path_user_csv = User.to_csv(users)

    if not path_user_csv:
        raise ValueError("No se pudo generar el archivo")

    try:
        return send_file(
            path_user_csv,
            mimetype='text/csv',
            attachment_filename=f"info_{user_type}s.csv",
            as_attachment=True
        )
    except (Exception, exc.SQLAlchemyError) as e:
        return jsonify({
            'message': f"Error al descargar el csv de los usuarios",
            'status': 500,
            'error': str(e)
        })


@auth.route('/logout')
@cross_origin()
def logout():
    return 'logout'
