from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from nanoid import generate
from answer.models import TakeQuiz, TakeAnswer, QuizAnswer
from quizzes.serializers import UserProfileSerializer 

# Create your views here.

class QuizAnswerView(APIView):
    
    def get(self):
        pass
