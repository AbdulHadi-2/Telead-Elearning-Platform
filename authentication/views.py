from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import UserProfileUpdateSerializer
from .models import CustomUser
from .serializers import RegisterSerializer, LoginSerializer
from .serializers import PasswordResetRequestSerializer, PasswordResetConfirmSerializer,NewPasswordSerializer
from rest_framework_simplejwt.tokens import RefreshToken 

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        
        if user.is_active:
            token = RefreshToken.for_user(user)  
            
            response_data = {
                "message": "Login successful",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "full_name": user.full_name,
                    "nick_name": user.nick_name,
                    "date_of_birth": user.date_of_birth.isoformat(),
                    "phone": user.phone,
                    "gender": user.gender,
                    "date_joined": user.date_joined.isoformat(),
                    "profile_picture": request.build_absolute_uri(user.profile_picture.url) if user.profile_picture else None,
                },
                "token": str(token.access_token), 
            }
            return Response(response_data, status=status.HTTP_200_OK)
        
        return Response({"error": "Account is not active"}, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetRequestView(APIView):
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.send_reset_code()
            return Response({"message": "Reset code sent to your email."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetConfirmView(APIView):
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        
        if serializer.is_valid():
            return Response({"status": "Reset code is valid."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NewPasswordView(APIView):
    def post(self, request):
        serializer = NewPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "Password updated successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]  

    def put(self, request):
        user = request.user  
        data = request.data.copy()

        if 'profile_picture' in request.FILES:  
            data['profile_picture'] = request.FILES['profile_picture']

        serializer = UserProfileUpdateSerializer(user, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Profile updated successfully",
                "user": serializer.data
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
from rest_framework.authtoken.models import Token
from django.contrib.auth import logout
import logging

logger = logging.getLogger(__name__)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        logout(request)
        if hasattr(user, 'auth_token'):
            user.auth_token.delete()
        else:
            Token.objects.filter(user=user).delete()
        
        logger.info(f"User {user.email} logged out successfully.")
        return Response({"status": "Logged out successfully."}, status=status.HTTP_200_OK)
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    