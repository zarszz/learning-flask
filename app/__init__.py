from flask import Flask, session, g
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app.commands import bp as command_bp
from app.db import db
from app.models import User
from app.routes import admin

migrate: Migrate = Migrate()


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes import auth, requests, approvals
    from app.routes.main import bp as main_bp

    # HTTP blueprints
    app.register_blueprint(auth.bp)
    app.register_blueprint(requests.bp)
    app.register_blueprint(approvals.bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(admin.bp)

    # CLI blueprints
    app.register_blueprint(command_bp)

    @app.before_request
    def load_logged_in_user() -> None:
        user_id = session.get('user_id')
        if user_id is None:
            g.user = None
        else:
            g.user = User.query.get(user_id)
            print("[FROM @app.before_request] Current user: ", g.user.role.role_name)

    @app.context_processor
    def inject_user_role() -> dict:
        print("Injecting current_user:", g.user)  # Debug statement
        return dict(current_user=g.user)

    return app
