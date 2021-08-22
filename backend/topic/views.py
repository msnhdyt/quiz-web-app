from account.models import MyUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Topic
from .serializers import TopicSerializer, UserProfileSerializer, TopicQuizSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from nanoid import generate
from datetime import datetime
from rest_framework.renderers import JSONRenderer

# Create your views here.
class TopicView(APIView):
    """
    List all topics, or create a new topic.
    """
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        topic = Topic.objects.all()
        serializer = TopicSerializer(topic, many=True)
        return Response(serializer.data)

    # def post(self, requests, format=None):
    #     data = requests.data
    #     data['code'] = generate(size=10)
    #     serializer = TopicSerializer(data=data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Join(APIView):

    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    # renderer_classes = [JSONRenderer]
    # def get(self, requests, format=None):
    #     queryset = UserProfile.objects.all()
    #     # print(queryset)
    #     serializer = UserProfileSerializer(queryset, many=True)
    #     # print(repr(serializer))
    #     #user_count = MyUser.objects.filter(is_active=True).count()
    #     #data = {'user_count': user_count}
    #     # print(serializer.data)
    #     return Response(serializer.data)

    def post(self, requests, user_id, format=None):
        data = requests.data
        """
        data = {
            "code":"xxxx"
        }
        """
        # print(data)
        try:
            topic = Topic.objects.get(code=data['code'])
            user = MyUser.objects.get(id=user_id)
            date_joined = datetime.now()
            user.user_topic.add(topic, through_defaults={'date_joined': date_joined})
        except:
            # print(Topic.objects.get(code=data['code']))
            error = {"error": "code not found"}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        detail_topic = Topic.objects.get(code=data['code'])
        serializer = TopicSerializer(detail_topic)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class TopicDetailView(APIView):
    
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request, code, format=None):
        topic = Topic.objects.get(code=code)
        serializer = TopicSerializer(topic)
        return Response(serializer.data) 

    # def post(self, request, format=None):
    #     data = request.data
    #     topic = Topic.objects.get(code=data['code'])
    #     serializer = TopicSerializer(topic)
    #     return Response(serializer.data)

class UserTopicView(APIView):
    
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    def get(self, request, user_id, format=None):
        data = MyUser.objects.get(id=user_id)
        # print(queryset)
        serializer = UserProfileSerializer(data)
        # print(repr(serializer))
        #user_count = MyUser.objects.filter(is_active=True).count()
        #data = {'user_count': user_count}
        # print(serializer.data)
        return Response(serializer.data)

    def post(self, request, user_id, format=None):
        """
        data = {
            "title":"judul ",
            "description": "desc"
        }
        """
        user = MyUser.objects.get(id=user_id)
        data = request.data
        data['code'] = generate(size=10)
        serializer = TopicSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

            topic = Topic.objects.get(code=data['code'])
            date_joined = datetime.now()
            user.user_topic.add(topic, through_defaults={'date_joined': date_joined})

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TopicQuizView(APIView):
    
    def get(self, request, code, format=None):
        data = Topic.objects.get(code=code)
        serializer = TopicQuizSerializer(data)
        return Response(serializer.data)