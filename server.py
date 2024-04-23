from flask import Flask
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager

from data import db_session
from data.models import *
from routes import main_route
from flask_admin import Admin


app = Flask(__name__)
admin = Admin(app, template_mode='bootstrap4')
login_manager = LoginManager(app)
app.config['SECRET_KEY'] = 'MY_LEARNING_SITE'


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


if __name__ == '__main__':
    db_session.global_init('db/ngl.db')
    admin.add_view(ModelView(User, db_session.create_session()))
    admin.add_view(ModelView(Posts, db_session.create_session()))
    app.register_blueprint(main_route.blueprint)
    app.run(debug=True)