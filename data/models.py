from datetime import datetime

import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'
    id_user = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    fio = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True)
    password = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    post = orm.relationship('Posts', back_populates='user')
    comment = orm.relationship('Comment', back_populates='user')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_id(self):
        return self.id_user


class Posts(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'post'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    id_author = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id_user'), nullable=True)
    author = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    content = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    photo = sqlalchemy.Column(sqlalchemy.BLOB, nullable=True)
    time_pub = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now)
    user = orm.relationship('User')
    comment = orm.relationship('Comment')


class Comment(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'comment'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    id_post = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('post.id'))
    fio_author = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey('users.fio'))
    id_author = sqlalchemy.Column(sqlalchemy.Integer)
    text_comment = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    time_comment = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now)
    user = orm.relationship('User')
    post = orm.relationship('Posts')




