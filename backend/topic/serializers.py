from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from topic.models import Topic
from account.models import UserTopic, MyUser
from quizzes.serializers import QuizzesSerializer

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['code','title', 'description', 'created_at']

class UserTopicSerializer(WritableNestedModelSerializer):
    title = serializers.ReadOnlyField(source='topic.title')
    created_at = serializers.ReadOnlyField(source='topic.created_at')
    desc = serializers.ReadOnlyField(source='topic.description')
    class Meta:
        model = UserTopic
        fields = ['date_joined', 'topic', 'title', 'created_at', 'desc']

class UserProfileSerializer(WritableNestedModelSerializer):
    user_topic = UserTopicSerializer(source='usertopic_set', many=True)
    class Meta:
        model = MyUser
        fields = ['id', 'user_topic']

class TopicQuizSerializer(serializers.ModelSerializer):
    quiz = QuizzesSerializer(many=True, read_only=True)

    class Meta:
        model = Topic
        fields = ['code', 'title', 'quiz']
