from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Habit, Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'name', 'age', 'gender', 'weight', 'height', 'mobile_number',
            'fitness_level', 'motivation_level', 'notifications',
            'preferred_workout_time', 'primary_goal', 'sleep_time',
            'wake_up_time', 'weekly_goal'
        ]

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    password = serializers.CharField(write_only=True)
    confirmPassword = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'password', 'confirmPassword', 'profile'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        if data.get('password') != data.get('confirmPassword'):
            raise serializers.ValidationError("Passwords don't match")
        return data

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        validated_data.pop('confirmPassword', None)
        
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        
        Profile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        profile = instance.profile

        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        for field, value in profile_data.items():
            setattr(profile, field, value)
        profile.save()

        return instance

class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = ['id', 'name', 'description', 'frequency', 'time', 'user', 'created_at', 'updated_at']