from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Product,Upvote,User

def home(request):
    products = Product.objects.exclude(hunter = User.objects.get(is_superuser=True)).order_by('-pub_date')
    return render(request,'products/home.html', {'products' :  products})

@login_required(login_url='/accounts/login')
def create(request):
    if request.method == 'POST':
        if request.POST['title'] and request.POST['body'] and request.POST['url'] and request.FILES['icon'] and request.FILES['image']:
            product = Product()
            product.title = request.POST['title']
            product.body = request.POST['body']
            if request.POST['url'].startswith('http://') or request.POST['url'].startswith('https://'):
                product.url = request.POST['url']
            else:
                product.url = 'http://' + request.POST['url']
            product.icon = request.FILES['icon']
            product.image = request.FILES['image']
            product.pub_date = timezone.datetime.now()
            product.hunter = request.user
            product.save()
            return redirect('/products/' + str(product.id))
        else:
            return render(request, 'products/create.html', {'error': 'All fields are required.'})
    else:
        return render(request,'products/create.html')

def edit(request, post_id):
    post = Product.objects.get(id=post_id)
    if request.method == 'POST':
        if request.POST['title'] and request.POST['body'] and request.POST['url'] and request.FILES['icon'] and request.FILES['image']:
            post.title = request.POST['title']
            post.body = request.POST['body']
            if request.POST['url'].startswith('http://') or request.POST['url'].startswith('https://'):
                post.url = request.POST['url']
            else:
                post.url = 'http://' + request.POST['url']
            post.icon = request.FILES['icon']
            post.image = request.FILES['image']
            post.hunter = request.user
            post.save()
            return redirect('/products/' + str(post.id))
        else:
            return render(request, 'products/edit.html', {'error': 'All fields are required.'})
    else:
        return render(request, 'products/edit.html',{'post': post})

def details(request, product_id):
    productDetail = get_object_or_404(Product, pk=product_id)
    upvoted = Upvote.objects.filter(product=product_id)
    return render(request, 'products/detail.html', {'product' : productDetail, 'upvoted': len(upvoted)})

@login_required(login_url='/accounts/login')
def upvote(request, product_id):
    current_user = request.user.id
    #upvoted = get_object_or_404(Upvote, product=product_id, user = current_user)
    upvoted = Upvote.objects.filter(user=current_user,product= product_id)
    if not upvoted:
        upvote = Upvote()
        upvote.user = get_object_or_404(User, pk=current_user)
        upvote.product = get_object_or_404(Product, pk=product_id)
        upvote.save()
    return redirect('/products/' + str(product_id))

@login_required(login_url='/accounts/login')
def myposts(request):
    posts = Product.objects.filter(hunter=get_object_or_404(User, pk=request.user.id))
    return render(request, 'products/my_post.html', {'posts': posts})

@login_required(login_url='/accounts/login')
def delete(request, post_id):
    post = Product.objects.get(id=post_id)
    post.delete()
    return redirect('/products/my-posts')