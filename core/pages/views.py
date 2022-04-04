from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login,logout,authenticate
from django.db.models import Count,Q
from .models import User,Post,Comment,Room,Message

# Create your views here.

#Home func
def home(request):
    if request.user.is_anonymous:
        return redirect("/login")
    else:
        posts=Post.objects.annotate(totallikes=Count('likes')).order_by("-totallikes","-create_date")
        # print(posts[0].postedby.username)/
        return render(request,"home.html",{
            "username":request.user.username,
            "fullname":request.user.fullname,
            "posts":posts,
            "joined":True
        })

#Signup func
def register(request):
    if request.method=="POST":
        fullname=request.POST.get("fullname")
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        cpassword=request.POST.get("cpassword")
        if password==cpassword:
            user=User(fullname=fullname,username=username,email=email,password=make_password(password))
            user.save()
        return redirect("/")
    else:
        if request.user.is_anonymous:
            return render(request,"register.html")
        else:
            return redirect("/")

#Login func
def loginFunc(request):
    try:
        if request.method=="POST":
            username=request.POST.get("username")
            password=request.POST.get("password")
            user=authenticate(username=username,password=password)
            login(request,user)
            return redirect("/")
        else:
            if request.user.is_anonymous:
                return render(request,"login.html")
            else:
                return redirect("/")
    except:
        return redirect("/login")

#Logout func
def logoutFunc(request):
    if request.user.is_anonymous is not None:
        logout(request)
    return redirect("/login")

#Create post
def createPost(request):
    if request.user.is_anonymous:
        return redirect("/login")
    elif request.method=="POST":
        title=request.POST.get("title")
        content=request.POST.get("content")
        postedby=request.user
        post=Post(title=title,content=content,postedby=postedby)
        post.save()
        return redirect("/")

#Like/unlike post
def likeUnlikePost(request,id):
    if request.user.is_anonymous:
        return redirect("/")
    else:
        post=Post.objects.get(id=id)
        if request.user in post.likes.all():
            post.likes.remove(request.user.id)
        else:
            post.likes.add(request.user.id)
        post.save()
        return redirect("/")

#Edit post
def editPost(request,id):
    post=Post.objects.get(id=id)
    if request.user.is_anonymous or post.postedby!=request.user:
        return redirect("/")
    else:
        return render(request,"editpost.html",{
            "post":post,
            "joined":True
        })

#Update post
def updatePost(request,id):
    post=Post.objects.get(id=id)
    if request.user.is_anonymous or post.postedby!=request.user:
        pass
    else:
        if request.method=="POST":
            title=request.POST.get("title")
            content=request.POST.get("content")
            post.title=title
            post.content=content
            post.save()
    return redirect("/")

#Delete post
def deletePost(request,id):
    post=Post.objects.get(id=id)
    if request.user.is_anonymous or post.postedby!=request.user:
        pass
    else:
        Post.objects.filter(id=id).delete()
    return redirect("/")

#Comment page
def commentPage(request,id):
    post=Post.objects.get(id=id)
    comments=Comment.objects.filter(post=id).order_by("-id")
    if request.user.is_anonymous:
        return redirect("/login")
    else:
        return render(request,"comments.html",{
            "post":post,
            "comments":comments,
            "joined":True,
            "user":request.user
        })

#Create comment
def createComment(request,id):
    post=Post.objects.get(id=id)
    if request.user.is_anonymous:
        pass
    else:
        if request.method=="POST":
            commentedby=request.user
            content=request.POST.get("content")
            comment=Comment(commentedby=commentedby,post=post,content=content)
            comment.save()
    return redirect("/comments/{}".format(id))

#Delete comment
def deleteComment(request,commentid):
    comment=Comment.objects.get(id=commentid)
    postid=comment.post.id
    if request.user.is_anonymous or comment.commentedby!=request.user:
        pass
    else:
        Comment.objects.filter(id=commentid).delete()
        pass
    return redirect("/comments/{}".format(postid))

#Search user (POST request)
def searchUserPost(request):
    if request.user.is_anonymous:
        pass
    else:
        if request.method=="POST":
            field=request.POST.get("field")
            users=User.objects.filter(username=field)
            print(users)
    return redirect("/")

#Search user (GET request)
def searchUserGet(request,id):
    user=User.objects.get(id=id)
    if request.user.is_anonymous or request.user==user:
        return redirect("/")
    else:
        return render(request,"user.html",{
            "user":user,
            "joined":True
        })

#Join room
def joinRoom(request,userid):
    user=User.objects.get(id=userid)
    try:
        if request.user.is_anonymous or request.user==user:
            return redirect("/")
        room=Room.objects.filter(user=request.user.id).get(user=user.id)
        messages=Message.objects.filter(room=room)
        return render(request,"chat.html",{
            "room":room,
            "joined":True,
            "otheruser":user,
            "messages":messages
        })
    except:
        room=Room.objects.create()
        room.user.add(request.user.id,user.id)
        room.save()
        return render(request,"chat.html",{
            "room":room,
            "joined":True,
            "otheruser":user,
            "own":request.user
        })

#Send message
def sendMessage(request,roomid,userid):
    if request.user.is_anonymous:
        return redirect("/login")
    else:
        if request.method=="POST":
            room=Room.objects.get(id=roomid)
            textmessage=request.POST.get("textmessage")
            message=Message(room=room,sender=request.user,message=textmessage)
            message.save()
        return redirect("/search/chat/{}".format(userid))