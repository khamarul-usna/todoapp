from django.shortcuts import render
from rest_framework.viewsets import ViewSet ,ModelViewSet
from rest_framework.response import Response
from api.serializers import TodoSerializer,RegistrationSerialiser
from api.models import Todos
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework import authentication,permissions
# Create your views here.
class TodosView(ViewSet):
    def list(self,request,*args,**kw):
        qs=Todos.objects.all()
        serializer=TodoSerializer(qs,many=True)
        return Response(data=serializer.data)
    def create(self,request,*args,**Kw):
        serializer=TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
    def retrieve(self,request,*arg,**kw):
        m_id=kw.get("pk")
        qs=Todos.objects.get(id=m_id)
        serializer=TodoSerializer(data=qs,many=False)
        return Response(data=serializer.data)
    def distroy(self,request,*arg,**kw):
        m_id=kw.get("pk")
        Todos.objects.get(id=m_id).delete()
        return Response(data="deleted")
    def update(self,request,*arg,**kw):
        id=kw.get("pk")
        obj=Todos.objects.get(id=id)
        serializer=TodoSerializer(data=request.data,instance=obj)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)




class TodoModelViews(ModelViewSet):

    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=TodoSerializer
    queryset=Todos.objects.all()
    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)
    def create(self, request, *args, **kwargs):
        serialzer=TodoSerializer(data=request.data,context={"user":request.user})
        if serialzer.is_valid():
            serialzer.save()
            return Response(data=serialzer.data)
        else: 
            return Response(data=serialzer.errors)
    # def create(self, request, *args, **kwargs):
    #     serializer=TodoSerializer(data=request.data)
    #     if serializer.is_valid():
    #         Todos.objects.create(**serializer.validated_data,user=request.user)
    #         return Response(data=serializer.data)

    #     else:
    #         return Response(data=serializer.errors)
    # def list(self, request, *args, **kwargs):
    #     qs=Todos.objects.filter(user=request.user)
    #     serializer=TodoSerializer(qs,many=True)
    #     return Response(data=serializer.data)
    def get_queryset(self):
        return Todos.objects.filter(user=self.request.user)

    @action(methods=["GET"],detail=False)
    def pending_todos(self,request,*arg,**kw):
        qs=Todos.objects.filter(status=False)
        serializer=TodoSerializer(qs,many=True)
        return Response(data=serializer.data)
    @action(methods=["GET"],detail=False)
    def completed_todos(self,request,*arg,**kw):
        qs=Todos.objects.filter(status=True)
        serializer=TodoSerializer(qs,many=True)
        return Response(data=serializer.data)
    @action(methods=["POST"],detail=True)
    def mark_as_done(self,request,*arg,**kw):
        m_id=kw.get("pk")
        object=Todos.objects.get(id=m_id)
        object.status=True
        object.save()
        serializer=TodoSerializer(object,many=False)
        return Response(data=serializer.data)
       


    
class UserView(ModelViewSet):
    serializer_class=RegistrationSerialiser
    queryset=User.objects.all()
    # def create(self,request,*args,**kw):
    #     serializer=RegistrationSerialiser(data=request.data)
    #     if serializer.is_valid():
    #         User.objects.create_user(**serializer.validated_data)
    #         return Response(data=serializer.data)
    #     else:
    #         return  Response(data=serializer.errors)
