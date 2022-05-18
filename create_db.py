from app import create_app, db
from app.models import *

db.create_all(app=create_app())
