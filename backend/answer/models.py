from django.db import models
from question.models import Question
from account.models import MyUser, TakeQuiz
from quizzes.models import Quizzes

# Create your models here.

# class QuizAnswer(models.Model):
#     text = models.TextField()
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.id

class TakeAnswer(models.Model):
    student_answer = models.TextField()
    similarity = models.FloatField(null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    take_id = models.ForeignKey(TakeQuiz, on_delete=models.CASCADE)
    true_or_false = models.BooleanField(null=True)

    def __str__(self):
        return str(self.id)