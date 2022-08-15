from django.core.mail import send_mail
from django.template.loader import render_to_string

from main.celery import app


@app.task
def send_activation_email(code, email):
    message = render_to_string('send_activation_mail.html', {'email': email, 'code': code})
    send_mail(
        'From Discuss',
        '',
        'sulimanovuran@gmail.com',
        [email],
        html_message=message
    )


@app.task
def restore_password_mail(code, email, username):
    message = render_to_string('send_restore_password_mail.html', {'username': username, 'code': code})
    send_mail(
        'From Discuss',
        '',
        'sulaimaonovuran@gmail.com',
        [email],
        html_message=message
    )
