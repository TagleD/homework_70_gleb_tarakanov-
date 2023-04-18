from django.http import JsonResponse, Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import TaskSerializer, ProjectSerializer
from webapp.models import Task, Project


# Create your views here.


# Представления для задач

class TaskListView(APIView):
    def get(self, request, *args, **kwargs):
        objects = Task.objects.all()
        serializer = TaskSerializer(objects, many=True)
        return Response(serializer.data, status=200)

    def post(self, request, *args, **kwargs):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetailUpdateDeleteView(APIView):
    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise Http404

    def get(self, request, *args, **kwargs):
        object = self.get_object(pk=kwargs.get('pk'))
        serializer = TaskSerializer(object)
        return JsonResponse(serializer.data, safe=False, status=200)

    def put(self, request, *args, **kwargs):
        object = self.get_object(pk=kwargs.get('pk'))
        serializer = TaskSerializer(object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        object = self.get_object(pk=kwargs.get('pk'))
        object.delete()
        return Response({'id': kwargs.get('pk')}, status=status.HTTP_204_NO_CONTENT)


# Представления для проектов
class ProjectDetailUpdateDeleteView(APIView):
    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404

    def get(self, request, *args, **kwargs):
        object = self.get_object(pk=kwargs.get('pk'))
        serializer = ProjectSerializer(object)
        return Response(serializer.data, status=200)

    def put(self, request, *args, **kwargs):
        object = self.get_object(pk=kwargs.get('pk'))
        serializer = ProjectSerializer(object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        object = self.get_object(pk=kwargs.get('pk'))
        object.delete()
        return Response({'id': kwargs.get('pk')}, status=status.HTTP_204_NO_CONTENT)
