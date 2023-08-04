from django.urls import path
from.views import *

app_name = "cms_app"
urlpatterns = [
    path('userregister',UserRegistrationView.as_view({'get':'list','post':'create'}),name="user_registration_View"),
    path('userregister/<int:id>',UserRegistrationView.as_view({'put':'update','get':'retrieve','delete':'destroy'}), name='user_registration_View'),
    path('login',UserLoginView.as_view(), name='login'),
    path('post',PostView.as_view({'post':'create','get':'list'}), name='post'),
    path('post/<int:id>',PostView.as_view({'put':'update','get':'retrieve'}), name='post'),
    path('like',LikeView.as_view({'post':'create','get':'list'}), name='like'),
    path('like/<int:post_id>',LikeView.as_view({'delete':'destroy','get':'retrieve'}), name='like'),
]
