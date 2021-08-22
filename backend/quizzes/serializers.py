from django.db.models import fields
from rest_framework import serializers
from quizzes.models import Quizzes
from account.models import MyUser, TakeQuiz
from drf_writable_nested.serializers import WritableNestedModelSerializer

class QuizzesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quizzes
        fields = '__all__'

class TakeQuizSerializer(WritableNestedModelSerializer):
    name = serializers.SerializerMethodField(method_name='get_name')

    class Meta:
        model = TakeQuiz
        fields = ['id','user_id', 'name','quiz_id', 'started_at', 'finished_at', 'similarity', 'score', ]
    
    def get_name(self, obj):
        return MyUser.objects.get(id=obj.user_id).first_name + ' ' + MyUser.objects.get(id=obj.user_id).last_name
    

class UserProfileSerializer(WritableNestedModelSerializer):
    quiz_taken = TakeQuizSerializer(source='takequiz_set', many=True)
    class Meta:
        model = MyUser
        fields = ['id','first_name','last_name', 'quiz_taken']