from authentication import auth_app
import os
from flask import Flask, Response, session, request, flash, url_for, redirect, render_template, g
from flask.ext.login import LoginManager, login_user, logout_user, current_user, login_required
import logging
from app.models import User
from app.forms import LoginForm, RegistrationForm

app = Flask(__name__)
logging.basicConfig(filename='authentication.log', level=logging.DEBUG)
log = logging.getLogger(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@app.route('/')
def home():
    if not session.get('logged_in'):
        return login()
    else:
        return image()


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('login.html', form=form)
    if form.validate_on_submit():
        remember_me = True if 'remember_me' in request.form else False
        user = User(user_id=form.user.id)
        login_user(user, remember=remember_me)
        flash('Logged in successfully')
        session['logged_in'] = True
        log.info('Logged in successfully')
    else:
        flash('Username or Password is invalid. Please try again', 'error')
        log.info('Login if failed')
        return redirect(url_for('login'))
    return redirect(request.args.get("next"))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'GET':
        return render_template('register.html')
    if form.is_validate():
        user = User(form.username.data, form.email.data,
                    form.password.data)
    db.session.add(user)
    flash('Thanks for registering!')
    log.info('User is created successfully')
    db.session.commit()
    return redirect(url_for('login'))


@app.route('/image', methods=['GET', 'POST'])
@login_required
def image():
    pass


@app.route('/logout')
@login_required
def logout():
    logout_user()
    session['logged_in'] = False
    return home()


@app.before_request
def before_request():
    g.user = current_user


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='localhost', port=8000)