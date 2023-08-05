import datetime
from urllib import response
from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
# Create your views here.
from django.contrib.auth.models import *
from rest_framework.response import Response
from knox.views import LoginView as KnoxLoginView
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.hashers import make_password
from .serializers import *
from rest_framework import status
from rest_framework import permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.auth import TokenAuthentication

class UserRegistrationView(ModelViewSet):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = [IsAuthenticated, ]
    serializer_class = User_register_serialzers
    queryset= User.objects.all()
    lookup_field = "id"

    def create(self, request, *args, **kwargs):
        first_name = request.data['first_name']
        email = request.data['email']
        password = request.data['password']
        user_details = User.objects.create(first_name = first_name, username = email, email = email,password = make_password(password))
        serializer = self.serializer_class(user_details)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def update(self, request, *args, **kwargs):
        id = self.kwargs['id']
        first_name = request.data['first_name']
        email = request.data['email']

        obj = User.objects.get(id=id)
        obj.first_name = first_name
        obj.email = email
        obj.save()
        serializer = self.serializer_class(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        obj = User.objects.get(id = self.kwargs['id'], user = self.request.user).delete()
        return Response({"message": "Your Id has been Deleted"}, status=status.HTTP_200_OK)
    

class UserLoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    # serializer_class = AuthTokenSerializer


    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user=authenticate(request,username=email,password=password)
        login(request, user)
        temp_list = super(UserLoginView, self).post(request)
        temp_list.data['id'] = user.id
        temp_list.data['email'] = user.email

        return Response(temp_list.data)
    
class PostView(ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    serializer_class = Post_serialzers
    queryset= Post.objects.all().order_by('id')
    lookup_field = 'id'

    def create(self, request, *args, **kwargs):
        title = request.data["title"]
        descriptions = request.data["descriptions"]
        content = request.data["content"]

        post_obj = Post.objects.create(title = title, descriptions = descriptions, content = content, creation_date = datetime.date.today())
        serializer = self.serializer_class(post_obj)
        
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def update(self, request, *args, **kwargs):
        id = self.kwargs['id']
        title = request.data["title"]
        descriptions = request.data["descriptions"]
        content = request.data["content"]

        obj = Post.objects.get(id = id)
        obj.title = title
        obj.descriptions = descriptions
        obj.content = content
        obj.save()
        serializer = self.serializer_class(obj)
        return Response(serializer.data,status=status.HTTP_200_OK)
    

class LikeView(ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    serializer_class = Like_serializers
    queryset= Like.objects.all()
    lookup_field = "post_id"

    def list(self, request, *args, **kwargs):
        dict = {}
        obj = Post.objects.only().values("id","title").order_by("id")
        
        for i in obj:
            queryset = Like.objects.filter(post_id = i["id"]).count()
            dict[i["id"]] = (f"{queryset} likes")
        return Response(dict)
    
    def create(self, request, *args, **kwargs):
        
        user = self.request.user.id
        post = request.data['post']

        obj = Like.objects.create(user = user, post_id = post)
        serializer = self.serializer_class(obj)

        return Response({"message":"like post"},status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        postid =  self.kwargs['post_id']
        if Like.objects.filter(post = postid, user_id = self.request.user.id):
            obj = Like.objects.get(post = postid, user_id = self.request.user.id).delete()
            return Response({"message": "dislike post"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "already dislike"}, status=status.HTTP_400_BAD_REQUEST)


    


