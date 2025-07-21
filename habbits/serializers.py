from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Habit, Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'name', 'age', 'gender', 'weight', 'height',
            'fitness_level', 'motivation_level', 'notifications',
            'preferred_workout_time', 'primary_goal', 'sleep_time',
            'wake_up_time'
        ]

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    password = serializers.CharField(write_only=True)
    confirmPassword = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'confirmPassword', 'profile']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        # Check if passwords match
        if data.get('password') != data.get('confirmPassword'):
            raise serializers.ValidationError({"confirmPassword": "Passwords don't match"})
        
        # Check for duplicate email (username) during creation
        if not self.instance:  # Only for create, not update
            email = data.get('email')
            if email and User.objects.filter(username=email).exists():
                raise serializers.ValidationError({"email": "A user with this email already exists."})
        
        return data

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        validated_data.pop('confirmPassword')
        email = validated_data['email']

        # Create user with email as username
        user = User.objects.create_user(
            username=email,
            email=email,
            password=validated_data['password']
        )
        Profile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        profile = instance.profile

        instance.email = validated_data.get('email', instance.email)
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        instance.save()

        for field, value in profile_data.items():
            setattr(profile, field, value)
        profile.save()

        return instance


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = ['id', 'name', 'description', 'frequency', 'time', 'user', 'created_at', 'updated_at']