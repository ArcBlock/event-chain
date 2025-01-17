import logging

from event_chain.app import controllers
from event_chain.app import forms
from event_chain.app import models
from event_chain.app import utils
from flask import Blueprint
from flask import flash
from flask import redirect
from flask import session
from flask import url_for

api_ticket = Blueprint(
    'api_ticket',
    __name__,
    template_folder='templates',
)
logger = logging.getLogger('api-ticket')


@api_ticket.route("/buy", methods=['POST'])
def buy():
    if not session.get('user'):
        return redirect(url_for('admin.login'))
    utils.refresh_token()
    form = forms.EventForm()
    address = form.address.data
    event = models.get_event_factory(address)

    hash = controllers.buy_ticket(address, session.get('user'))
    if not hash:
        logger.error("Fail to buy ticket from web.")
        flash('Oops! Someone is faster than you. Get another ticket!')
        return redirect('/')
    else:
        logger.info("ticket is bought successfully from web.")
        flash(
            'Congratulations! Ticket for Event "{}" is bought '
            'successfully!'.format(
                event.title), category='info')
    return redirect(url_for('tickets.all'))


@api_ticket.route("/activate/<address>", methods=['GET', 'POST'])
def use(address):
    utils.refresh_token()

    controllers.consume(address, session['user'])
    flash('Your ticket has been checked successfully! Enjoy your event!',
          category='info')
    return redirect(url_for('tickets.all'))
