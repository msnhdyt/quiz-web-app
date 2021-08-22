from rest_framework import serializers
from answer.models import TakeAnswer
from account.models import TakeQuiz

# class QuizAnswerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = QuizAnswer
#         fields = '__all__'

class TakeAnswerSerializer(serializers.ModelSerializer):
    # score = serializers.SerializerMethodField(method_name='get_score')

    class Meta:
        model = TakeAnswer
        fields = '__all__'
    
    # def get_score(self, obj):
    #     return TakeQuiz.objects.get(id=obj.take_id_id).score