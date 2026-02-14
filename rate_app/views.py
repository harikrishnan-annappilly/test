from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from .models import Tbl_User, Tbl_Movie, Tbl_Rating
from .utilities import get_star_rating


# Create your views here.
def index(request):
    user_id = request.session.get("user_id")
    context = {}
    if user_id:
        user = Tbl_User.objects.get(id=user_id)
        context["logged_user"] = user
    else:
        context["logged_user"] = None
    return render(request, "index.html", context)


def user_register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = make_password(request.POST.get("password"))
        role = request.POST.get("role")
        if Tbl_User.objects.filter(username=username).exists():
            return render(request, "user_register.html", {"message": "User already exists"})
        user = Tbl_User(username=username, password=password, role=role)
        user.save()
        return render(request, "user_register.html", {"message": f"User {username} registered successfully"})
    return render(request, "user_register.html")


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = Tbl_User.objects.filter(username=username).first()
        if not user:
            return render(request, "user_login.html", {"message": "User not found"})
        if not check_password(password, user.password):
            return render(request, "user_login.html", {"message": "Invalid password"})
        request.session["user_id"] = user.id
        request.session["user_name"] = user.username
        request.session["user_role"] = user.role
        if user:
            return redirect("index")
    return render(request, "user_login.html")


def user_logout(request):
    del request.session["user_id"]
    del request.session["user_name"]
    del request.session["user_role"]
    return redirect("index")


# movie section
def movie_show_all(request):
    user_id = request.session.get("user_id")
    user = Tbl_User.objects.filter(id=user_id).first()
    if not user:
        return redirect("user_login")

    movies = Tbl_Movie.objects.all()
    message = request.GET.get("message")
    context = {"movies": movies, "logged_user": user}
    if message:
        context["message"] = message
    return render(request, "movie_show_all.html", context)


def movie_show_one(request):
    user_id = request.session.get("user_id")
    user = Tbl_User.objects.filter(id=user_id).first()
    if not user:
        return redirect("user_login")

    movie_id = request.GET.get("movie_id")
    movie = Tbl_Movie.objects.filter(id=movie_id).first()
    ratings = Tbl_Rating.objects.filter(movie_id=movie)
    average_rating = round(sum([rating.rating for rating in ratings]) / len(ratings), 1) if ratings else "#NA"
    if movie:
        movie.rating = average_rating if average_rating != "#NA" else 0
        movie.save()

    current_user_rating = Tbl_Rating.objects.filter(user_id=user, movie_id=movie).first()
    context = {
        "movie": movie,
        "ratings": ratings,
        "ratings_count": len(ratings),
        "rate_button_text": "Write a Review" if not current_user_rating else "Update My Review",
        "logged_user": user,
    }
    if not movie:
        context = {"message": "Movie not found", "logged_user": user}
    return render(request, "movie_show_one.html", context)


def movie_delete(request):
    movie_id = request.GET.get("movie_id")
    print(movie_id)
    movie = Tbl_Movie.objects.filter(id=movie_id).first()
    movie_name = "#NA"
    if movie:
        movie_name = movie.name
        movie.delete()
    return redirect(f"/movies?message=Movie {movie_name} deleted successfully")


def movie_add(request):
    user_id = request.session.get("user_id")
    user = Tbl_User.objects.filter(id=user_id).first()
    if not user:
        return redirect("user_login")

    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        genre = request.POST.get("genre")
        rating = 0
        year = request.POST.get("year")
        movie = Tbl_Movie(name=name, description=description, genre=genre, rating=rating, year=year)
        movie.save()
        return redirect(f"/movies?message=Movie {name} added successfully")
    return render(request, "movie_add.html", {"logged_user": user})


# review section
def review_add(request):
    user_id = request.session.get("user_id")
    user = Tbl_User.objects.filter(id=user_id).first()
    if not user:
        return redirect("user_login")

    movie_id = request.GET.get("movie_id")
    movie = Tbl_Movie.objects.filter(id=movie_id).first()
    if not movie:
        return redirect("movie_show_all")
    review = Tbl_Rating.objects.filter(user_id=user, movie_id=movie).first()

    if request.method == "POST":
        comment = request.POST.get("comment")
        rating = get_star_rating(comment)
        if review:
            review.rating = rating
            review.comment = comment
        else:
            review = Tbl_Rating(user_id=user, movie_id=movie, rating=rating, comment=comment)
        review.save()
        return redirect(f"/movie_show_one/?movie_id={movie.id}")

    context = {"logged_user": user, "movie": movie}
    if review:
        context["review"] = review
    return render(
        request,
        "review_add.html",
        context,
    )


def review_delete(request):
    user_id = request.session.get("user_id")
    user = Tbl_User.objects.filter(id=user_id).first()
    if not user:
        return redirect("user_login")

    review_id = request.GET.get("review_id")
    review = Tbl_Rating.objects.filter(id=review_id).first()
    if review:
        movie_id = review.movie_id.id
        review.delete()
        return redirect(f"/movie_show_one/?movie_id={movie_id}")
    return redirect(f"/movies")
