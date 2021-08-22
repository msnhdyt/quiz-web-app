from django.db import models
from quizzes.models import Quizzes

# Create your models here.
class Question(models.Model):
    questions = models.TextField(default="No question")
    answer = models.TextField(default="No answer")
    quiz = models.ForeignKey(Quizzes, on_delete=models.CASCADE)