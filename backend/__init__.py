from fastapi import FastAPI
from sqlalchemy import SQLAlchemy
from app.core.config import settings

# api = Api()
db = SQLAlchemy()


def create_app():
    # Initialize Flask
    app = FastAPI(title=settings.PROJECT_NAME)

    '''
    # If the database file does not exist, create it (only for SQLite)
    if not os.path.exists(os.getenv('DATABASE_PATH') + os.getenv('DATABASE_NAME')):
        os.mknod(os.getenv('DATABASE_PATH') + os.getenv('DATABASE_NAME'))

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.getenv('DATABASE_PATH') + os.getenv('DATABASE_NAME')
    db.init_app(app)


    import main.resources as resources
    # Here will be initialized the rest of the app modules
    api.add_resource(resources.ScoreResource, '/score/<id>')
    api.add_resource(resources.ScoresResource, '/scores')
    api.add_resource(resources.PoemResource, '/poem/<id>')
    api.add_resource(resources.PoemsResource, '/poems')
    api.add_resource(resources.UserResource, '/user/<id>')
    api.add_resource(resources.UsersResource, '/users')


    # Flask.register_blueprint(app)
    api.init_app(app)
    '''

    # Return initialized app
    return app