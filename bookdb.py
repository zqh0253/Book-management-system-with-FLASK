# set FLASK_APP=bookdb.py
# set FLASK_ENV=development
from app import app, db
from app.models import User

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}