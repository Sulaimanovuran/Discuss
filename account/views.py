from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from account.serializers import RegisterSerializer, LoginSerializer, ChangePasswordSerializer, \
    ForgotPasswordSerializer, PasswordRetrievalSerializer

User = get_user_model()


class RegistrationApiView(APIView):
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('Вы успешно зарегестрированы,'
                            'вам на почту отправлена ссылка для активации аккаунта', status=201)


class ActivationView(APIView):
    def get(self, request, activation_code):
        try:
            user = User.objects.get(activation_code=activation_code)
            user.is_active = True
            user.activation_code = ''
            user.save()
            return Response('Вы успешно активировали свой аккаунт =)', status=200)
        except User.DoesNotExist:
            return Response("Неверный код", status=400)


class LoginApiView(ObtainAuthToken):
    serializer_class = LoginSerializer


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializers = ChangePasswordSerializer(data=request.data,
                                               context={'request': request})

        serializers.is_valid(raise_exception=True)  # проверка на корректность введенных данных
        serializers.set_new_password()
        return Response('Вы успешно изменили свой пароль')


class LogOutApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = request.user
            Token.objects.filter(user=user).delete()
            return Response('Вы вышли из своего аккаунта')
        except:
            return Response(status=403)


class ForgotPasswordView(APIView):
    def post(self, request):
        data = request.data
        serializer = ForgotPasswordSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.send_code()
        return Response('Вам отправлено письмо для восстановления пароля')


class PasswordRetrievalView(APIView):
    def post(self, request):
        data = request.data
        serializer = PasswordRetrievalSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.set_new_pass()
        return Response('Вы успешно восстановили свой пароль')