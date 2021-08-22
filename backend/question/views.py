from os import error
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from nanoid import generate
from question.models import Question
from question.serializers import QuestionAnswerSerializer
import pandas as pd
import json

# Create your views here.
class QuestionView(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request, quiz_id, format=None):
        try:
            data = quiz_id
        except:
            data = {
                "error": "please set quiz_id paramater"
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        question = Question.objects.filter(quiz=data)
        serializer = QuestionAnswerSerializer(question, many=True)
        return Response(serializer.data)

    def post(self, request, quiz_id, format=None):
        # print(request.data['file'])
        try:
            df = pd.read_csv(request.data['file'])
            columns = list(df.columns)
            # print(columns)
            if columns[0] != "questions":
                # print(columns[0])
                # print("satu")
                raise ValueError("column doesn't match")
            if columns[1] != "answer":
                # print("dua")
                raise ValueError("column doesn't match")
        except ValueError:
            data = {
                "error": "column doesn't match"
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        #df = pd.read_csv(request.data['file'])
        df['quiz'] = pd.Series([quiz_id for i in range(len(df))])
        result = df.to_json(orient='records')
        # print("result", result)
        parsed = json.loads(result)
        json.dumps(parsed)  
        # print(parsed)

        for row in parsed:
            serializer = QuestionAnswerSerializer(data=row)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(parsed, status=status.HTTP_201_CREATED)