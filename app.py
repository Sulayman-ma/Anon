"""Main file"""

from flask_migrate import Migrate
from anon.models import User, Admin
from anon import create_app, db
from config import Config



app = create_app(Config)

# migration extension
migrate = Migrate(app, db)

@app.shell_context_processor
def context_processor():
    return dict(db = db, User = User, Admin = Admin)