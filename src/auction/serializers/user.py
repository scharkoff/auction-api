from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[
        RegexValidator(
            regex=r"^\S+@\S+\.\S+$",
            message='Неверный формат почты'
        )
    ])

    ROLE_CHOICES = [
        ('user', 'User'),
        ('admin', 'Admin'),
    ]

    role = serializers.ChoiceField(choices=ROLE_CHOICES, default='user')

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Данный email уже используется")
        return value
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Данный логин уже используется")
        
        if len(value) < 3:
            raise serializers.ValidationError("Логин не может быть меньше 3-х символов")
        return value
    
    def create(self, validated_data):
        role = validated_data.pop('role', 'user')
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.role = role
        user.save()
        return user
    
    def update(self, instance, validated_data):
        role = validated_data.pop('role', None)
        
        if role is not None:
            instance.role = role
        
        return super().update(instance, validated_data)
