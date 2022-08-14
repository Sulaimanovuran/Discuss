from django.core.mail import send_mail
from rest_framework.response import Response

from main.celery import app
from thread.models import Awareness, Comment, Answer


@app.task
def send_comment(answer, author, body):
    answer1 = Answer.objects.get(text=answer)
    message = f'Привет, под твоим ответом: {answer1},\nбыл оставлен комментарий с текстом: {body}.\nПользователем: {author}'
    try:
        user = Awareness.objects.get(email=answer1.owner)
        send_mail(
           'From forum project',
           message,
           'sulimanovuran@gmail.com',
           [user.email]
        )
    except Awareness.DoesNotExist:
        pass
