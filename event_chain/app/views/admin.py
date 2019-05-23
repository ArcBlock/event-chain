from event_chain.app import controllers
from event_chain.app import utils
from event_chain.app.forms.admin import RegisterForm
from flask import Blueprint
from flask import g
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for, flash

admin = Blueprint(
    'admin',
    __name__
)


@admin.route("/login", methods=['GET', 'POST'])
def login():
    form = RegisterForm()
    if form.validate_on_submit():
        user = controllers.load_user(
            passphrase=form.passphrase.data,
            address=form.address.data,
        )
        session['user'] = user
        if user:
            return redirect(url_for('events.all'))
        else:
            flash("Passphrase and address don't match!", 'error')
            return redirect(url_for('admin.login'))
    else:
        utils.flash_errors(form)
    return render_template('admin/login.html', form=form)


@admin.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = controllers.register_user(
            form.name.data,
            form.passphrase.data
        )
        session['user'] = user
        g.logger.debug('New User registered!')
    else:
        utils.flash_errors(form)
        return render_template('admin/login.html', form=form)
    return redirect(url_for('events.all'))


@admin.route("/logout", methods=['GET', 'POST'])
def logout():
    session['user'] = None
    return redirect(url_for('admin.login'))
