from account.models import MyUser, TakeQuiz
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AND, IsAuthenticated
from nanoid import generate
from quizzes.models import Quizzes
from quizzes.serializers import QuizzesSerializer, TakeQuizSerializer, UserProfileSerializer
from topic.models import Topic
from question.models import Question
from question.serializers import QuestionSerializer, QuestionAnswerSerializer
from datetime import datetime
from answer.models import TakeAnswer
from answer.serializers import TakeAnswerSerializer
from rest_framework.renderers import JSONRenderer
from evaluate.similarity import Similarity
import random

# Create your views here.
class QuizzesView(APIView):

    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    def get(self, requests, code, user_id, format=None):
        data = Quizzes.objects.filter(topic=code)
        serializer = QuizzesSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, requests, code, user_id, format=None):
        """
        data = {
            "title":"quiz q",
            "description":"desc"
        }
        """
        print(code)
        data = requests.data
        print(data)
        print(user_id)
        # topic = Topic.objects.get(code=data['topic'])
        # data['topic'] = topic
        # print(data['topic'])
        data['topic'] = code
        data['id'] = generate(size=15)
        print(data)
        serializer = QuizzesSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TakeQuizView(APIView):
    
    def get(self, request, quiz_id, user_id, format=None):
        # try:
            user = MyUser.objects.get(id=user_id)
            print(user)
            quiz = Quizzes.objects.get(id=quiz_id)
            print(quiz)
            try: 
                q = TakeQuiz.objects.get(user__id=user_id, quiz__id=quiz_id)
                id = q.id
            except: 
                id = generate(size=20)
            print(id)
            similarity = None
            score = None
            user.quiz_taken.add(quiz, through_defaults={
                'id': id, 'similarity': similarity, 'score':score
            })
            print("sebelum")
            question = Question.objects.filter(quiz=quiz_id)
            print(question)
            data = QuestionSerializer(question, many=True).data
            data = {"take_id":id, "question": data}
            return Response(data, status=status.HTTP_201_CREATED)
        # except:
        #     error = {"message": "please check quiz_id or user_id"}
        #     return Response(error, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, quiz_id, user_id, format=None):
        take_id = request.data['take_id']
        takequiz = TakeQuiz.objects.get(id=take_id)
        a = TakeQuizSerializer(takequiz, data={'finished_at':datetime.now()}, partial=True)
        if a.is_valid():
            a.save()
        return Response(a.data, status=status.HTTP_201_CREATED)

class QuizTakenView(APIView):
    def get(self, request, quiz_id, user_id, format=None):
        user = MyUser.objects.filter(id=user_id)
        return Response(UserProfileSerializer(user, many=True).data)

class SubmitView(APIView):

    def post(self, request, quiz_id, user_id, format=None):
        """
        data = { "data" : [
                {
                "question": "question id ",
                "student_answer": "answer"
                },
                {
                "question": "question id ",
                "student_answer": "answer"
                },
            ]
        }
        """
        similarity = Similarity()

        data = request.data
        data = data['data']

        try: 
            take_id = TakeQuiz.objects.get(user__id=user_id, quiz__id=quiz_id)
            for row in data:
                x = row['student_answer'].lower()
                y = Question.objects.get(id=row['question']).answer.lower()
                print((x, y))
                row['similarity'] = similarity.calculate(x, y)[0][0]
                row['take_id'] = take_id.id

                serializer = TakeAnswerSerializer(data=row)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            message = {"message": "You have successfully submitted"}
            return Response(message, status=status.HTTP_201_CREATED)
        except: 
            error = {"message": "please check quiz_id or user_id"}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

class AllReportView(APIView):

    def get(self, request, quiz_id, format=None):
        quiz = TakeQuiz.objects.filter(quiz__id=quiz_id)
        return Response(TakeQuizSerializer(quiz, many=True).data)

class DetailReportView(APIView):
    # renderer_classes = [JSONRenderer]
    def get(self, request, quiz_id, user_id, format=None):
        question_answer = Question.objects.filter(quiz__id=quiz_id)
        question_answer_data = QuestionAnswerSerializer(question_answer, many=True).data

        take_quiz = TakeQuiz.objects.get(user__id=user_id, quiz__id=quiz_id)

        take_answer = TakeAnswer.objects.filter(take_id__id=take_quiz.id)
        take_answer_data = TakeAnswerSerializer(take_answer, many=True).data
        List = []
        for a,b in zip(question_answer_data,take_answer_data):
            List.append({**a, **b})
        data = {
            "name": MyUser.objects.get(id=user_id).first_name,
            "score": take_quiz.score,
            "data": List
        }
        # print(type(data), type(serializer))
        return Response(data)

class CalculateView(APIView):

    def get(self, request, quiz_id, format=None):
        #sim = Similarity()
        threshold = 0.7
        take_id_object = TakeQuiz.objects.filter(quiz=quiz_id)
        for i in take_id_object.iterator():
            take_answer_object = TakeAnswer.objects.filter(take_id=i.id)

            score = 0
            sum_similarity = 0
            for j in take_answer_object.iterator():
                question_id = j.question_id
                answer = Question.objects.get(id=question_id).answer.lower()
                student_answer = j.student_answer.lower()

                #similarity = sim.calculate(student_answer, answer)[0][0]
                similarity = random.uniform(0,1)
                sum_similarity += similarity
                true_or_false = False
                if similarity >= threshold:
                    true_or_false = True
                    score += 1
                a = TakeAnswerSerializer(j, data={'similarity':similarity, 'true_or_false':true_or_false}, partial=True)
                if a.is_valid():
                    a.save()
            #print(score, take_answer_object.count())
            score = score / take_answer_object.count() * 100
            sum_similarity = sum_similarity / take_answer_object.count()
            take_quiz = TakeQuiz.objects.get(id=i.id)
            take_quiz_serializer = TakeQuizSerializer(take_quiz, data={'score':score, 'similarity':sum_similarity}, partial=True)
            if take_quiz_serializer.is_valid():
                take_quiz_serializer.save()

        data = {"message":"Yeay!!! the scores have been calculated"}
        return Response(data, status=status.HTTP_200_OK)