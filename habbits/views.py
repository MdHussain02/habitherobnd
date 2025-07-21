# habbits/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .serializers import UserSerializer, HabitSerializer
from .models import Habit, Profile
from django.contrib.auth import authenticate


class CustomLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('username')
        password = request.data.get('password')

        # Authenticate using email as username
        user = authenticate(username=email, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            serializer = UserSerializer(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Add confirmPassword if not provided
        mutable_data = request.data.copy()
        if 'confirmPassword' not in mutable_data:
            mutable_data['confirmPassword'] = mutable_data.get('password', '')

        serializer = UserSerializer(data=mutable_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Other views remain unchanged for brevity
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class HabitListView(APIView):
    permission_classes = [IsAuthenticated]
    

    def get(self, request):
        habits = Habit.objects.all()  # Show all habits created by all users
        serializer = HabitSerializer(habits, many=True)
        return Response(serializer.data)

class HabitView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Return habits created by the logged-in user
        user_habits = Habit.objects.filter(user=request.user)
        serializer = HabitSerializer(user_habits, many=True)
        return Response({"your_habits": serializer.data})

    def post(self, request):
        serializer = HabitSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, habit_id):
        try:
            habit = Habit.objects.get(id=habit_id, user=request.user)
            serializer = HabitSerializer(habit, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Habit.DoesNotExist:
            return Response({"error": "Habit not found or unauthorized"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, habit_id):
        try:
            habit = Habit.objects.get(id=habit_id, user=request.user)
            habit.delete()
            return Response({"message": "Habit deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Habit.DoesNotExist:
            return Response({"error": "Habit not found or unauthorized"}, status=status.HTTP_404_NOT_FOUND)
        

class ProfileChoicesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        def to_name_value(choices):
            return [{"value": val, "label": label} for val, label in choices]

        choices = {
            'gender': to_name_value(Profile.GENDER_CHOICES),
            'fitness_level': to_name_value(Profile.FITNESS_LEVEL_CHOICES),
            'motivation_level': to_name_value(Profile.MOTIVATION_LEVEL_CHOICES),
            'preferred_workout_time': to_name_value(Profile.WORKOUT_TIME_CHOICES),
            'primary_goal': to_name_value(Profile.PRIMARY_GOAL_CHOICES),
        }
        return Response(choices)

