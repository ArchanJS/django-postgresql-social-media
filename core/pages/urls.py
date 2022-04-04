from django.contrib import admin
from django.urls import path
from pages import views

urlpatterns = [
    path('', views.home, name="homepage"),
    path('register',views.register,name="registerpage"),
    path('login',views.loginFunc,name="loginpage"),
    path('logout',views.logoutFunc,name="logoutpage"),
    path('createpost',views.createPost,name="createpost"),
    path('like/<str:id>',views.likeUnlikePost,name="createpost"),
    path('edit/<str:id>',views.editPost,name="editpost"),
    path('update/<str:id>',views.updatePost,name="updatepost"),
    path('delete/<str:id>',views.deletePost,name="deletepost"),
    path('comments/<str:id>',views.commentPage,name="commentpage"),
    path('createcomment/<str:id>',views.createComment,name="createcomment"),
    path('comments/deletecomment/<str:commentid>',views.deleteComment,name="deletecomment"),
    path('search',views.searchUserPost,name="searchuserpost"),
    path('search/<str:id>',views.searchUserGet,name="searchuserget"),
    path('search/chat/<str:userid>',views.joinRoom,name="joinroom"),
    path('sendmessage/<str:roomid>/<str:userid>',views.sendMessage,name="sendmessage"),
]
