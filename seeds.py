from app import db
from app.models import Role, Category, DocumentType

roles_text = ['Cliente', 'Empleado', 'Administrador']
categories_text = ['PQRs', 'Soporte', 'Otros']
document_types_text = ['Cedula', 'Pasaporte', 'NIT']

for role in roles_text:
    db.session.add(Role(name=role))

for category in categories_text:
    db.session.add(Category(name=category))

for document_type in document_types_text:
    db.session.add(DocumentType(name=document_type))

db.session.commit()