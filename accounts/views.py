from django.contrib import auth, messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from accounts.models import Contact
from products.models import Product


def signup(request):
    if request.method == 'POST':
        if request.POST['password'] == request.POST['confirm_password']:
            try:
                user = User.objects.get(username=request.POST['username'])
                return render(request, 'accounts/signup.html',{'error': 'Username has been already been taken'})
            except User.DoesNotExist:
                user= User.objects.create_user(request.POST['username'], password= request.POST['password'])
                auth.login(request,user)
                return redirect('home')
        else:
            return render(request, 'accounts/signup.html', {'error': 'Passwords must match'})
    else:
        return render(request, 'accounts/signup.html')

def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'],password= request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'accounts/login.html', {'error': 'Username or Password is incorrect.'})
    else:
        return render(request, 'accounts/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')
    #return render(request, 'accounts/login.html')

@login_required(login_url='/accounts/login')
def profile(request):
    current_user = request.user
    following = Contact.objects.filter(user_from=current_user)
    followers = Contact.objects.filter(user_to=current_user)
    return render(request, 'accounts/profile.html',{
        'following': following,
        'followers': followers
    })

@login_required(login_url='/accounts/login')
def followers(request):
    current_user = request.user
    followers = Contact.objects.filter(user_to=current_user)
    return render(request, 'accounts/followers.html',{'followers': followers})

@login_required(login_url='/accounts/login')
def following(request):
    current_user = request.user
    followings = Contact.objects.filter(user_from=current_user)
    return render(request, 'accounts/following.html',{'followings': followings})

@login_required(login_url='/accounts/login')
def follow(request, user_id):
    current_user = request.user
    userExists = User.objects.get(pk=user_id)
    if userExists:
        contact = Contact()
        contact.user_from = current_user
        contact.user_to = userExists
        contact.save()
    return redirect('viewUserProfile' , username =userExists.username)

@login_required(login_url='/accounts/login')
def unfollow(request, user_id):
    current_user = request.user
    userExists = User.objects.get(pk=user_id)
    if userExists:
        contact = Contact.objects.filter(user_to=userExists, user_from= current_user)
        contact.delete()
    return redirect('viewUserProfile' , username =userExists.username)

@login_required(login_url='/accounts/login')
def viewUserProfile(request, username):
    userData = User.objects.get(username=username)# for getting single entry fron database
    if userData ==  request.user:
        return redirect('profile')
    #userData = User.objects.filter(username=username)# for getting multiple entry fron database
    followers = Contact.objects.filter(user_to=userData)
    followings = Contact.objects.filter(user_from=userData)
    posts = Product.objects.filter(hunter=userData)

    loggedInUserFollow = Contact.objects.filter(user_to=userData, user_from = request.user)
    followedByLoggedInUser = True
    if not loggedInUserFollow:
        followedByLoggedInUser = False
    return render(request, 'accounts/view-profile.html',{
        'viewUser': userData,
        'followers' : followers,
        'followings': followings,
        'posts': posts,
        'followedByLoggedInUser':followedByLoggedInUser
    })

@login_required(login_url='/accounts/login')
def changePassword(request):
    if request.method == 'POST':
        if request.POST['password'] == request.POST['confirm-password']:
            u = User.objects.get(username=request.user.username)
            u.set_password(request.POST['password'])
            u.save()
            update_session_auth_hash(request, u)
            messages.success(request, 'Password successfully changed.')
            # messages.debug(request, '%s SQL statements were executed.' % count)
            # messages.info(request, 'Three credits remain in your account.')
            # messages.success(request, 'Profile details updated.')
            # messages.warning(request, 'Your account expires in three days.')
            # messages.error(request, 'Document deleted.')
            return render(request, 'accounts/change-password.html')
        else:
            return render(request, 'accounts/change-password.html', {'error': 'It looks like that your entered Password does not match with Confirm Password!'})
    else:
        return render(request, 'accounts/change-password.html')