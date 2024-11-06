from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponseRedirect
from .models import User, Post, Follow
from django.views.decorators.csrf import csrf_exempt
import json
from django.urls import reverse
from django.core.paginator import Paginator

User = get_user_model()

# Manejar inicio de sesión
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("all_posts")
        else:
            return render(request, "network/login.html", {"message": "Invalid username and/or password."})
    else:
        return render(request, "network/login.html")

# Manejar cierre de sesión
def logout_view(request):
    logout(request)
    return redirect("all_posts")

# Manejar registro de usuario
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {"message": "Passwords must match."})
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {"message": "Username already taken."})
        login(request, user)
        return redirect("all_posts")
    else:
        return render(request, "network/register.html")

# Ver todas las publicaciones
def all_posts(request):
    posts = Post.objects.all().order_by("-timestamp")
    return render(request, "network/all_posts.html", {"posts": posts})

# Página de perfil de usuario
@login_required
def profile(request, user_id):
    user_profile = get_object_or_404(User, pk=user_id)
    posts = user_profile.posts.all().order_by("-timestamp")
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    followers_count = user_profile.followers.count()
    following_count = user_profile.following.count()
    is_following = Follow.objects.filter(user=request.user, followed_user=user_profile).exists()
    return render(request, "network/profile.html", {
        "user_profile": user_profile,
        "page_obj": page_obj,
        "followers_count": followers_count,
        "following_count": following_count,
        "is_following": is_following
    })

# Publicaciones de los usuarios seguidos
@login_required
def following(request):
    following_users = request.user.following.values_list('followed_user', flat=True)
    posts = Post.objects.filter(user__in=following_users).order_by("-timestamp")
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "network/following.html", {"page_obj": page_obj})




@login_required
@csrf_exempt
def toggle_follow(request, user_id):
    # Obtener el usuario al que se quiere seguir o dejar de seguir
    user_to_follow = get_object_or_404(User, pk=user_id)

    # Verificar si ya sigue al usuario
    if Follow.objects.filter(user=request.user, followed_user=user_to_follow).exists():
        # Si ya sigue, dejar de seguir
        Follow.objects.filter(user=request.user, followed_user=user_to_follow).delete()
        is_following = False
    else:
        # Si no sigue, agregar a la lista de seguidos
        Follow.objects.create(user=request.user, followed_user=user_to_follow)
        is_following = True

    # Obtener los nuevos conteos de seguidores y seguidos
    followers_count = user_to_follow.followers.count()
    following_count = request.user.following.count()

    # Retornar los datos actualizados en formato JSON
    return JsonResponse({
        "is_following": is_following,
        "followers_count": followers_count,
        "following_count": following_count
    })


@login_required
@csrf_exempt
def toggle_like(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.method == "PUT":
        # Alternar "like" o "unlike"
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            liked = False
        else:
            post.likes.add(request.user)
            liked = True
        
        # Retornar el nuevo estado y conteo de likes en formato JSON
        return JsonResponse({"liked": liked, "like_count": post.likes.count()})
    
    return JsonResponse({"error": "PUT request required."}, status=400)

@csrf_exempt
@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    # Verificar que el usuario sea el propietario de la publicación
    if request.user != post.user:
        return JsonResponse({"error": "You do not have permission to edit this post."}, status=403)

    if request.method == "PUT":
        data = json.loads(request.body)
        content = data.get("content", "")
        
        # Actualizar el contenido de la publicación
        post.content = content
        post.save()
        return JsonResponse({"success": True, "message": "Post updated successfully."})
    
    return JsonResponse({"error": "PUT request required."}, status=400)



def all_posts(request):
    posts = Post.objects.all().order_by("-timestamp")
    paginator = Paginator(posts, 10)  # Muestra 10 publicaciones por página

    # Obtener el número de página actual de la URL (default es 1)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "network/all_posts.html", {"page_obj": page_obj})


@login_required
def create_post(request):
    if request.method == "POST":
        content = request.POST["content"]
        # Crear la nueva publicación si hay contenido
        if content:
            Post.objects.create(user=request.user, content=content)
        return redirect("all_posts")

