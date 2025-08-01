from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from .serializers import UserSerializer, HabitSerializer
from .models import Habit, Profile


# ✅ Reusable response formatter
def standard_response(success=True, message="", data=None, http_status=status.HTTP_200_OK):
    return Response({
        "status": success,
        "message": message,
        "data": data
    }, status=http_status)


# ✅ Login API
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
            return standard_response(
                success=True,
                message="Login successful",
                data={
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': serializer.data
                }
            )
        return standard_response(success=False, message="Invalid credentials", http_status=status.HTTP_401_UNAUTHORIZED)


# ✅ Registration API
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        mutable_data = request.data.copy()
        if 'confirmPassword' not in mutable_data:
            mutable_data['confirmPassword'] = mutable_data.get('password', '')

        serializer = UserSerializer(data=mutable_data)
        if serializer.is_valid():
            serializer.save()
            return standard_response(success=True, message="Registration successful", data=serializer.data, http_status=status.HTTP_201_CREATED)
        return standard_response(success=False, message="Registration failed", data=serializer.errors, http_status=status.HTTP_400_BAD_REQUEST)


# ✅ User Profile API (Get & Update)
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return standard_response(success=True, message="Profile fetched successfully", data=serializer.data)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return standard_response(success=True, message="Profile updated successfully", data=serializer.data)
        return standard_response(success=False, message="Profile update failed", data=serializer.errors, http_status=status.HTTP_400_BAD_REQUEST)


# ✅ All Habits (for testing/admin/demo purposes)
class HabitListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        habits = Habit.objects.all()
        serializer = HabitSerializer(habits, many=True)
        return standard_response(success=True, message="All habits fetched", data=serializer.data)


# ✅ User-specific Habits API
class HabitView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_habits = Habit.objects.filter(user=request.user)
        serializer = HabitSerializer(user_habits, many=True)
        return standard_response(success=True, message="Your habits fetched", data=serializer.data)

    def post(self, request):
        serializer = HabitSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return standard_response(success=True, message="Habit created successfully", data=serializer.data, http_status=status.HTTP_201_CREATED)
        return standard_response(success=False, message="Habit creation failed", data=serializer.errors, http_status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, habit_id):
        try:
            habit = Habit.objects.get(id=habit_id, user=request.user)
            serializer = HabitSerializer(habit, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return standard_response(success=True, message="Habit updated successfully", data=serializer.data)
            return standard_response(success=False, message="Habit update failed", data=serializer.errors, http_status=status.HTTP_400_BAD_REQUEST)
        except Habit.DoesNotExist:
            return standard_response(success=False, message="Habit not found or unauthorized", http_status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, habit_id):
        try:
            habit = Habit.objects.get(id=habit_id, user=request.user)
            habit.delete()
            return standard_response(success=True, message="Habit deleted successfully", http_status=status.HTTP_204_NO_CONTENT)
        except Habit.DoesNotExist:
            return standard_response(success=False, message="Habit not found or unauthorized", http_status=status.HTTP_404_NOT_FOUND)


# ✅ Profile Choices (for dropdowns in frontend)
class ProfileChoicesView(APIView):
    permission_classes = [AllowAny]

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
        return standard_response(success=True, message="Profile choices fetched", data=choices)
