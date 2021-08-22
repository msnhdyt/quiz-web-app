from django.db.models import fields
from rest_framework import serializers
from question.models import Question

class QuestionAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        exclude = ['id']

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        exclude = ['quiz', 'answer']
