from django.shortcuts import get_object_or_404

from rest_framework.views import APIView, Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from teacher.models import Lesson, Teacher
from teacher.serializers import TeacherSerializer, AddLessonSerializer, LessonSerializer 

class TeacherAPIView(APIView):
    def get(self, request, format=None):
        teachers = Teacher.objects.all()
        serializer = TeacherSerializer(teachers, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

class AddLessonAPIView(APIView):
    def post(self, request, id, format=None):
        teacher = get_object_or_404(Teacher, id=id)
        serializer = AddLessonSerializer(data=request.data)
        print('@',request.data)
        if serializer.is_valid():
            print('@@',serializer.validated_data.get('name'),serializer.validated_data.get('email'))
            lesson = Lesson(
                name = serializer.validated_data.get('name'),
                email = serializer.validated_data.get('email'),
                teacher = teacher
            )
            lesson.save()
            lesson_serializer = LessonSerializer(lesson, many=False)
            return Response(lesson_serializer.data, status=HTTP_201_CREATED)
        return Response({
                    "message": "There are validation errors", 
                    "errors": serializer.errors
                }, status=HTTP_400_BAD_REQUEST)