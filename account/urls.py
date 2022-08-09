from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from account.views import *

urlpatterns = [
    path('register/', RegistrationApiView.as_view()),
    path('active/<uuid:activation_code>/', ActivationView.as_view()),
    path('change_password/', ChangePasswordView.as_view()),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('reset_password/', ForgotPasswordView.as_view()),
    path('restore_password/', ForgotPasswordComplete.as_view())
]