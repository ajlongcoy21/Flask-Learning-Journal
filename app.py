# source ./env/bin/activate
# deactivate

from flask import Flask, g, render_template, flash, redirect, url_for, abort
from flask_bcrypt import check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

import forms
import models

DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

app = Flask(__name__)
app.secret_key = 'asdf;lkajd23497@)(*@&$asfl;ajaf'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None

@app.before_request
def before_request():
    """
    Connect to the database before each request.
    """
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user

@app.after_request
def after_request(response):
    """
    Close the database connection after each request
    """
    g.db.close()
    return response

@app.route('/')
@app.route('/entries')
def index():
    template = 'index.html'
    journal_entries = models.Entry.select().order_by(-models.Entry.timestamp)
    return render_template(template, journal_entries=journal_entries)

@app.route('/register', methods=('GET', 'POST'))
def register():
    """
    docstring
    """
    form = forms.RegisterForm()
    if form.validate_on_submit():
        flash("Yay, you registered!", "success")
        models.User.create_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        return redirect(url_for('index'))
    return render_template('register.html', form=form)

@app.route('/login', methods=('GET', 'POST'))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash("Your email or password doesn't match!", "error")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You've been logged in!", "success")
                return redirect(url_for('index'))
            else:
                flash("Your email or password doesn't match!", "error")
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You've been logged out! Come back soon!", "success")
    return redirect(url_for('index'))

@app.route('/entries/new', methods=('GET', 'POST'))
def entries_new():
    form = forms.EntryForm()
    if form.validate_on_submit():
        models.Entry.create(
            user=g.user._get_current_object(), 
            title=form.title.data.strip(), 
            date=form.date.data, time=form.time.data, learned=form.learned.data.strip(), 
            resources=form.resources.data.strip())
        flash("Entry Posted!", "success")
        return redirect(url_for('index'))
    return render_template('new.html', form=form)

@app.route('/entries/<int:id>')
def entries(id):
    try:
        journal_entry = models.Entry.get_by_id(id)
    except models.DoesNotExist:
        flash("Journal entry does not exist!", "error")
        return redirect(url_for('index'))
    else:
        return render_template('detail.html', entry=journal_entry)

@app.route('/entries/<int:id>/edit', methods=('GET', 'POST'))
def entries_edit(id):
    try:
        journal_entry = models.Entry.get_by_id(id)
    except models.DoesNotExist:
        flash("Journal entry does not exist!", "error")
        return redirect(url_for('index'))
    else:
        form = forms.EditForm(title=journal_entry.title, date=journal_entry.date, time=journal_entry.time, learned=journal_entry.learned, resources=journal_entry.resources)

        if form.validate_on_submit():
            models.Entry.update(
                user=g.user._get_current_object(), 
                title=form.title.data.strip(), 
                date=form.date.data, time=form.time.data, learned=form.learned.data.strip(), 
                resources=form.resources.data.strip()).where(models.Entry.id == id).execute()
            flash("Entry Updated!", "success")
            return redirect(url_for('index'))
        else:
            print('here now')
            return render_template('edit.html', form=form, entry=journal_entry)

@app.route('/entries/<int:id>/delete')
def delete(id):
    try:
        models.Entry.get_by_id(id)
    except models.DoesNotExist:
        flash("Journal entry does not exist, so it cannot be deleted", "error")
        return redirect(url_for('index'))
    else:
        models.Entry.delete_by_id(id)
        flash("Journal entry successfully deleted!", "success")
        return redirect(url_for('index'))

if __name__ == '__main__':
    models.initialize()
    try:
        models.User.create_user(
            username='testuser',
            email='testuser@gmail.com',
            password='test',
            admin=True
        )
    except ValueError:
        pass

    app.run(debug=DEBUG, host=HOST, port=PORT)