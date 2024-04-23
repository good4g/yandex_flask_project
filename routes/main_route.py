import os
from os import write
import asyncio

import flask
from flask import render_template, url_for, redirect, request, flash
from string import punctuation

from flask_login import login_required, logout_user, login_user, current_user

from data import db_session
from data.models import User, Posts
from forms.edit_data import EditData
from forms.enter_form import EnterForm
from forms.login_form import RegForm
from forms.add_post import AddPost
from forms.comment_form import CommentForm
from data.models import Comment


blueprint = flask.Blueprint(
    'main_route',
    __name__,
    template_folder='templates'
)


async def load_photo(data_photo):
    with open(f'static/img/photo_async_{data_photo.id}.png', 'wb') as file:
        file.write(data_photo.photo)


async def main(all_photo):
    task = [asyncio.create_task(load_photo(data)) for data in all_photo if data.photo]
    await asyncio.gather(*task)


@blueprint.route('/')
def base():
    db_sess = db_session.create_session()
    posts = db_sess.query(Posts).all()
    asyncio.run(main(posts))
    return render_template('index.html', posts=posts, str=str, user_here=False)


@login_required
@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@blueprint.route('/registration', methods=['POST', 'GET'])
def registration_account():
    form = RegForm()
    params = {'get_url': url_for('static', filename='css/my_style.css'),
              'form': form}
    if form.validate_on_submit():
        if len(form.password.data) >= 8:
            if (not form.password.data.isalpha()) and (not form.password.data.isdigit()):
                if any(symbol in punctuation for symbol in form.password.data):
                    if form.password.data == form.repeat_password.data:
                        db_sess = db_session.create_session()
                        if not db_sess.query(User).filter(User.email == form.email.data).first():
                            user = User()
                            user.fio = f'{form.surname.data} {form.name.data}'
                            user.email = form.email.data
                            user.set_password(form.password.data)
                            db_sess.add(user)
                            db_sess.commit()
                            return redirect('/')
                        return render_template('registration.html', **params,
                                               message='Такой пользователь уже есть')
                return render_template('registration.html', **params,
                                       message=f'Пароль должен содержать специальные символы: {punctuation}')
            return render_template('registration.html', **params,
                                   message='Пароль должен содержать буквы, цифры и специальные символы')
        return render_template('registration.html', **params,
                               message='Пароль должен содержать восемь или более символов')
    return render_template('registration.html', **params)


@blueprint.route('/enter', methods=['POST', 'GET'])
def enter_user():
    form = EnterForm()
    params = {'form': form, 'get_url': url_for('static', filename='css/my_style.css')}
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user:
            if user.check_password(form.password.data):
                login_user(user, remember=True)
                return redirect('/')
            return render_template('enter.html', **params, message='Пароль неверный')
        return render_template('enter.html', **params, message='Такого пользователя нет', not_found=True)
    return render_template('enter.html', **params)


@login_required
@blueprint.route('/add_post', methods=['GET', 'POST'])
def add_post():
    form = AddPost()
    params = dict(form=form, user_here=True, title='Добавить пост',
                  post_title='',
                  post_description='', post_content_text='')
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        posts = Posts()
        posts.author = f'{current_user.fio}'
        posts.title = form.title.data
        posts.description = form.description.data
        posts.content = form.content.data
        posts.photo = request.files['fieldF'].read()
        current_user.post.append(posts)
        db_sess.merge(posts)
        db_sess.commit()
        params['message'] = 'Новость успешно опубликована'
        return render_template('edit_or_add.html', **params)
    return render_template('edit_or_add.html', **params)


@login_required
@blueprint.route('/my_posts', methods=['GET', 'POST'])
def check_my_post():
    db_sess = db_session.create_session()
    return render_template('my_posts.html',
                           posts=db_sess.query(Posts).filter(Posts.id_author == current_user.id_user),
                           user_here=True, open=open, write=write, str=str)


@login_required
@blueprint.route('/view_post/<int:id>', methods=['GET', 'POST'])
def view_post(id):
    db_sess = db_session.create_session()
    post = db_sess.query(Posts).get(id)
    all_comment = db_sess.query(Comment).filter(Comment.id_post == id).order_by(Comment.time_comment).all()
    form = CommentForm()
    if form.validate_on_submit():
        comment_user = Comment()
        comment_user.text_comment = form.comment.data
        comment_user.id_post = id
        comment_user.id_author = current_user.id_user
        current_user.comment.append(comment_user)
        db_sess.merge(comment_user)
        db_sess.commit()
        return redirect('/view_post/' + str(id))
    return render_template('view_post.html', post=post, user_here=True, form=form, comment=all_comment)


@login_required
@blueprint.route('/del_post/<int:id>', methods=['GET', 'POST'])
def del_post(id):
    db_sess = db_session.create_session()
    db_sess.delete(db_sess.query(Posts).get(id))
    if f'static/img/photo_async_{id}.png' in os.listdir('static/img'):
        os.remove(f'static/img/photo_async_{id}.png')
    db_sess.commit()
    return redirect('/')


@login_required
@blueprint.route('/edit_post/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    form = AddPost()
    db_sess = db_session.create_session()
    value = db_sess.query(Posts).get(id)
    return render_template('edit_or_add.html', user_here=True, form=form,
                  title='Изменить пост', post_title=value.title, post_description=value.description, post_content_text=value.content)


@login_required
@blueprint.route('/del_comment/<int:id>/<int:id_post>', methods=['GET', 'POST'])
def del_comm(id, id_post):
    db_sess = db_session.create_session()
    db_sess.delete(db_sess.query(Comment).get(id))
    db_sess.commit()
    return redirect('/view_post/' + str(id_post))


@login_required
@blueprint.route('/profile_user/<int:id>', methods=['GET', 'POST'])
def user_profile(id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(id)
    quan = db_sess.query(Posts).filter(Posts.id_author == id).count()
    return render_template('profile_user.html', user_here=True, fio=user.fio, quan=quan)


@login_required
@blueprint.route('/edit_my_data/<int:id>', methods=['GET', 'POST'])
def edit_data(id):
    form = EditData()
    print(form.validate_on_submit(), form.errors, form.rename.data)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        db_sess.query(User).update(dict(fio=f'{form.rename.data} {form.re_surname.data}'))
        db_sess.commit()
        return redirect('/profile_user/' + str(id))
    return render_template('edit_data.html', form=form, user_here=True)


