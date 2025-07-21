from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Non-binary', 'Non-binary'),
        ('Other', 'Other'),
        ('Prefer not to say', 'Prefer not to say'),
    ]
    
    FITNESS_LEVEL_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
        ('Professional', 'Professional'),
    ]
    
    MOTIVATION_LEVEL_CHOICES = [
        ('1 - Very Low', '1 - Very Low'),
        ('2 - Low', '2 - Low'),
        ('3 - Average', '3 - Average'),
        ('4 - High', '4 - High'),
        ('5 - Very High', '5 - Very High'),
    ]
    
    WORKOUT_TIME_CHOICES = [
        ('Morning (6-9 AM)', 'Morning (6-9 AM)'),
        ('Late Morning (9-12 PM)', 'Late Morning (9-12 PM)'),
        ('Afternoon (12-3 PM)', 'Afternoon (12-3 PM)'),
        ('Late Afternoon (3-6 PM)', 'Late Afternoon (3-6 PM)'),
        ('Evening (6-9 PM)', 'Evening (6-9 PM)'),
        ('Night (9-12 AM)', 'Night (9-12 AM)'),
    ]
    
    PRIMARY_GOAL_CHOICES = [
        ('Weight Loss', 'Weight Loss'),
        ('Muscle Gain', 'Muscle Gain'),
        ('General Fitness', 'General Fitness'),
        ('Endurance Training', 'Endurance Training'),
        ('Event Preparation', 'Event Preparation'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=100, null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    fitness_level = models.CharField(max_length=20, choices=FITNESS_LEVEL_CHOICES, null=True, blank=True)
    motivation_level = models.CharField(max_length=20, choices=MOTIVATION_LEVEL_CHOICES, null=True, blank=True)
    notifications = models.BooleanField(default=True)
    preferred_workout_time = models.CharField(max_length=30, choices=WORKOUT_TIME_CHOICES, null=True, blank=True)
    primary_goal = models.CharField(max_length=30, choices=PRIMARY_GOAL_CHOICES, null=True, blank=True)
    sleep_time = models.TimeField(null=True, blank=True)
    wake_up_time = models.TimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"



class Habit(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    frequency = models.CharField(max_length=50)  # daily, weekly, monthly
    time = models.TimeField(null=True, blank=True)  # Time when the habit should be done
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name