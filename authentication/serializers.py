from rest_framework import serializers
from .models import CustomUser
from django.core.mail import send_mail
from django.conf import settings
import random
from django.contrib.auth import authenticate


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'full_name', 'nick_name', 'date_of_birth', 'phone', 'gender', 'password', 'profile_picture']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_picture = validated_data.pop('profile_picture', None)  
        user = CustomUser.objects.create_user(**validated_data)
        if profile_picture:
            user.profile_picture = profile_picture 
        user.is_active = True
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise serializers.ValidationError('Invalid email or password.')
        else:
            raise serializers.ValidationError('Both email and password are required.')

        attrs['user'] = user
        return attrs




from django.core.mail import EmailMultiAlternatives



class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user is associated with this email address.")
        return value

    def send_reset_code(self):
        email = self.validated_data['email']
        user = CustomUser.objects.get(email=email)

        reset_code = random.randint(1000, 9999)
        user.reset_code = reset_code
        user.save()

        subject = "Password Reset"
        from_email = "Telead <elearning198@gmail.com>"
        to = [user.email]
        text_content = f"Your Reset code is: {reset_code}. It is valid for 15 minutes."

        styled_otp = " ".join(f"<strong>{digit}</strong>" for digit in str(reset_code))

        html_content = f"""
        <div style="text-align: center; font-family: sans-serif;">
            <p style="font-size: 18px;">Your Reset code is:</p>
            <div style="background-color:#007BFF; color:white; padding:10px 20px;
                        display:inline-block; border-radius:6px; font-size:22px;
                        letter-spacing: 8px; font-weight: bold;">
                {styled_otp}
            </div>
            <p style="margin-top: 15px; font-size: 14px; color: #555;">
                This code is valid for 15 minutes.
            </p>
        </div>
        """

        msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        
        
class PasswordResetConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    reset_code = serializers.IntegerField()

    def validate(self, data):
        email = data.get("email")
        reset_code = data.get("reset_code")

        try:
            user = CustomUser.objects.get(email=email)

            if user.reset_code != reset_code:
                raise serializers.ValidationError({"reset_code": "Invalid reset code."})

        except CustomUser.DoesNotExist:
            raise serializers.ValidationError({"email": "Email not found."})

        return {"user": user}
    
    
class NewPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data["email"]
        if not CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "Email not found."})
        return data

    def save(self):
        email = self.validated_data["email"]
        new_password = self.validated_data["new_password"]

        user = CustomUser.objects.get(email=email)
        user.set_password(new_password)  
        user.reset_code = None 
        user.save()
        return user

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(required=False) 

    class Meta:
        model = CustomUser
        fields = ['full_name', 'phone', 'gender', 'date_of_birth', 'profile_picture']

    def update(self, instance, validated_data):
        if 'profile_picture' in validated_data:
            instance.profile_picture = validated_data['profile_picture']

        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)

        instance.save()
        return instance