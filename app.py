from flask import Flask
from flask_migrate import Migrate

from models import db
from views import myapp

def create_app():
    app = Flask(__name__)
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://maksym:@localhost:5432/workshop_api"
    db.init_app(app)
    migrate = Migrate(app, db)
    return app

app = create_app()
app.app_context().push()

app.register_blueprint(myapp)

if __name__ == "__main__":
    app.run()
