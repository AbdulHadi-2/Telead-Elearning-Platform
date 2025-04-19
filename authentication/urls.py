from django.urls import path
from .views import RegisterView, LogoutView,LoginView,NewPasswordView,PasswordResetRequestView, PasswordResetConfirmView,UserProfileUpdateView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('new-password/', NewPasswordView.as_view(), name='new-password'),
    path('profile/update/', UserProfileUpdateView.as_view(), name='profile-update'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
