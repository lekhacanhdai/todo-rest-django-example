from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Todo
from .serializers import TodoSerializer

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# Create your views here.
class TodoListApiView(APIView):
    list_task_response = openapi.Response("task", TodoSerializer(many=True))
    
    #1. List all
    @swagger_auto_schema(
        tags=['Task Controller'],
        operation_summary='Get all task', 
        operation_id='Get all task',
        operation_description='GET /todos/api/',
        responses={200: list_task_response}
        )
    def get(self, request, *args, **kwargs):
        '''
        List all the todo items for given requested user
        '''
        todos = Todo.objects.all()
        seriablizer = TodoSerializer(todos, many=True)
        return Response(seriablizer.data, status=status.HTTP_200_OK)
    
    #2.Create
    @swagger_auto_schema(
        tags=['Task Controller'],
        operation_summary='Add new task', 
        operation_id='Add new task todo',
        operation_description='POST /todos/api/',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'task': openapi.Schema(type=openapi.TYPE_STRING, description='name task'),
                'complete': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='complete')
            }
        ),
        responses={200: openapi.Response('task', TodoSerializer)}
        )
    def post(self, request, *args, **kwargs):
        data = {
            'task': request.data.get('task'),
            'complete': request.data.get('complete'),
            'user': request.user.id
        }
        seriablizer = TodoSerializer(data=data)
        if seriablizer.is_valid():
            seriablizer.save()
            return Response(seriablizer.data, status=status.HTTP_201_CREATED)
        return Response(seriablizer.errors, status=status.HTTP_400_BAD_REQUEST)
    
      
class TodoDetailApiView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get_object(self, todo_id):
        '''
        heper method to get object with given todo_id, and user_id
        '''
        try:
            return Todo.objects.get(id=todo_id)
        except Todo.DoesNotExist:
            return None
    #3. Retrieve
    todo_id_param = openapi.Parameter('todo_id', openapi.IN_PATH, description="Todo id path variable", type=openapi.TYPE_INTEGER, required=True)
    @swagger_auto_schema(
        tags=['Task Controller'],
        operation_summary='Get task by id', 
        manual_parameters=[todo_id_param], 
        operation_id='Get task by Id',
        operation_description='GET /todos/api/{todo_id}/',
        responses={200: openapi.Response('task', TodoSerializer)}
        )
    def get(self, request, todo_id, *args, **kwargs):
        todo_instance = self.get_object(todo_id)
        if not todo_instance:
            return Response(
                {"rest": "Object with todo id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = TodoSerializer(todo_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    #4 Update
    @swagger_auto_schema(
        tags=['Task Controller'], 
        operation_summary='Update task', 
        operation_id='Update task todo',
        manual_parameters=[todo_id_param],
        operation_description='PUT /todos/api/{todo_id}/',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'task': openapi.Schema(type=openapi.TYPE_STRING, description='name task'),
                'complete': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='complete')
            }
        ),
        responses={200: openapi.Response('task', TodoSerializer)}
        )
    def put(self, request, todo_id, *args, **kwargs):
        '''
        Update todo id item with given todo id if exists
        '''
        todo_instance = self.get_object(todo_id)
        if not todo_instance:
            return Response(
                {"res": "Object with todo id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'task': request.data.get('task'),
            'complete': request.data.get('complete'),
            'user': request.user.id
        }
        
        serializer = TodoSerializer(instance=todo_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #5. Delete
    @swagger_auto_schema(
        tags=['Task Controller'],
        operation_summary='Delete task', 
        operation_id='Delete task',
        manual_parameters=[todo_id_param],
        operation_description='DELETE /todos/api/{todo_id}/',
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT, 
                properties={
                    'res': openapi.Schema(type=openapi.TYPE_STRING, description='description')
                    }
                )
            }
        )
    def delete(self, request, todo_id, *args, **kwargs):
        '''
        Delete the todo item with given todo id if exists
        '''
        
        todo_instance = self.get_object(todo_id)
        if not todo_instance:
            return Response(
                {"res": "Object with todo id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        todo_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )
