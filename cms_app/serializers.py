from rest_framework import serializers
from django.contrib.auth.models import *
from cms_app.models import *

class User_register_serialzers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class Post_serialzers(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"

class Like_serializers(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = "__all__"