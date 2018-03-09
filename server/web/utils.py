from flask_mail import Message, Mail
from threading import Thread
from flask import render_template, current_app

mail = Mail()


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    if isinstance(to, str):
        to = [to]
    app = current_app._get_current_object()
    msg = Message(subject, sender=app.config['FLASKY_MAIL_SENDER'], recipients=to)
    msg.body = render_template(f'email/{template}.txt.j2', **kwargs)
    msg.html = render_template(f'email/{template}.html.j2', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr
