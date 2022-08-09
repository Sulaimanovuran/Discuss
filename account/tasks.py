from django.core.mail import send_mail

from main.celery import app


@app.task
def celery_send_confirmation_email(code, email):
    body = f'http://localhost:8000/account/active/{code}/'
    send_mail(
        'From Discuss',
        body,
        'sulimanovuran@gmail.com',
        [email]
    )


@app.task
def restore_password_mail(code, email, username):
    body = f'Здравствуйте {username.title()}\n Ваш код для восстановления пароля\n{code}'
    send_mail(
        'From Discuss',
        body,
        'sulaimaonovuran@gmail.com',
        [email]
    )