from threading import Thread

from flask import render_template, current_app, request
from flask_mail import Message, Mail

mail = Mail()


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def log_message(msg, lvl='info'):
    """
    Logs message for given level
    @param msg : log message
    @param lvl : (default: info) - Log level
    """
    extra = {
        'remote_addr': request.remote_addr,
        'url': request.url
    }
    loggers = {
        'warning': current_app.logger.warning,
        'info': current_app.logger.info,
        'debug': current_app.logger.debug,
        'error': current_app.logger.error,
        'critical': current_app.logger.critical
    }
    loggers[lvl](msg, extra=extra)


def send_email(to, subject, template, sender, **kwargs):
    if isinstance(to, str):
        to = [to]
    app = current_app._get_current_object()
    msg = Message(subject, sender=sender, recipients=to)
    msg.body = render_template(f'email/{template}.txt.j2', **kwargs)
    msg.html = render_template(f'email/{template}.html.j2', **kwargs)
    if app.config['DEBUG']:
        send_async_email(app, msg)
    else:
        Thread(target=send_async_email, args=[app, msg]).start()

def print_debug(message):
    """
    Prints a message only when app is in debug mode
    @param message : message to print
    """
    if current_app.config['DEBUG']:
        print(message)
