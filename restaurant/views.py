from django.shortcuts import render, get_object_or_404, redirect
from restaurant.models import Contact, Dish, Team, Category, Profile, Order
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import FoodBag
from django.conf import settings
from .forms import FoodItemForm
from django.shortcuts import render
from .models import Category
from django.db.models import Q


def index(request):
    context = {}
    category = Category.objects.all().order_by("name")

    dishes = []

    for cat in category:
        dishes.append(
            {
                "cat_id": cat.id,
                "cat_name": cat.name,
                "cat_img": (
                    cat.image.url if cat.image else ""
                ),  # Ensure a valid image URL
                "items": list(cat.dish_set.all().values()),
            }
        )
        print(dishes)

    context = {"categories": category, "menu": dishes}
    return render(request, "index.html", context)


def contact_us(request):
    context = {}
    if request.method == "POST":
        name = request.POST.get("name")
        em = request.POST.get("email")
        sub = request.POST.get("subject")
        msz = request.POST.get("message")

        obj = Contact(name=name, email=em, subject=sub, message=msz)
        obj.save()
        context = {"message": f"Dear {name}, Thanks for your time!"}

    return render(request, "contact.html", context)


def about(request):
    return render(request, "about.html")


# def team_members(request):
#     context = {}
#     members = Team.objects.all().order_by("name")
#     context = {"team_members": members}
#     return render(request, "team.html", context)


def dishes(request, id):
    context = {}

    dish_category = Category.objects.get(id=id).name

    sort_option = request.GET.get("sort", "name")
    search_query = request.GET.get("q", "")
    dishes = Dish.objects.filter(category__id=id, is_available=True)

    if search_query:
        dishes = dishes.filter(
            Q(name__icontains=search_query) | Q(ingredients__icontains=search_query)
        )

    if sort_option == "price":
        dishes = dishes.order_by("discounted_price")
    elif sort_option == "price_desc":
        dishes = dishes.order_by("-discounted_price")
    else:
        dishes = dishes.order_by("name")

    context.update(
        {
            "dishes": dishes,
            "dish_category": dish_category,
            "query": search_query,
            "sort": sort_option,
        }
    )
    return render(request, "dishes.html", context)


def menu(request):
    categories = Category.objects.all()
    context = {"categories": categories}
    return render(request, "category_menu.html", context)


def check_user_exists(request):
    email = request.GET.get("email")
    check = User.objects.filter(username=email)
    if len(check) == 0:
        return JsonResponse({"status": 0, "message": "Not Exist"})
    else:
        return JsonResponse(
            {"status": 1, "message": "A user with this email already exists!"}
        )


def register(request):
    context = {}
    if request.method == "POST":
        # fetch data from html form
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("pass")
        contact = request.POST.get("number")
        check = User.objects.filter(username=email)
        if len(check) == 0:
            # Save data to both tables
            user = User.objects.create_user(email, email, password)
            user.first_name = name
            user.save()

            profile = Profile(user=user, contact_number=contact)
            profile.save()
            context = {"status": f"User {name} Registered Successfully!"}
        else:
            context = {"error": f"A User with this email already exists"}

    return render(request, "register.html", context)


def user_login(request):
    context = {}
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        checked_user = authenticate(request, username=email, password=password)
        if checked_user:
            login(request, checked_user)  # Use the imported login function
            if checked_user.is_superuser:
                return HttpResponseRedirect("/admin")
            return HttpResponseRedirect("/dashboard")
        else:
            context.update(
                {"message": "Invalid Login Details!", "class": "alert-danger"}
            )

    return render(request, "login.html", context)


@login_required
def dashboard(request):
    context = {}
    logedin_user = get_object_or_404(User, id=request.user.id)

    # Fetch or create the user's profile
    profile, created = Profile.objects.get_or_create(user=logedin_user)
    context["profile"] = profile

    # Update Profile
    if "update_profile" in request.POST:
        print("file=", request.FILES)
        name = request.POST.get("name")
        contact = request.POST.get("contact_number")
        add = request.POST.get("address")

        profile.user.first_name = name
        profile.user.save()
        profile.contact_number = contact
        profile.address = add

        if "profile_pic" in request.FILES:
            pic = request.FILES["profile_pic"]
            profile.profile_pic = pic

        profile.save()
        context["status"] = "Profile updated successfully!"

    # Change Password
    if "change_pass" in request.POST:
        curr_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")

        if logedin_user.check_password(curr_password):
            logedin_user.set_password(new_password)
            logedin_user.save()
            login(request, logedin_user)
            context["status"] = "Password Updated Successfully!"
        else:
            context["status"] = "Current Password Incorrect!"

    # Fetch Orders
    orders = Order.objects.filter(customer__user=logedin_user).order_by("-id")
    context["orders"] = orders

    return render(request, "dashboard.html", context)


def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/")


def single_dish(request, id):
    # Get the dish object based on the provided ID
    dish = Dish.objects.get(id=id)

    # Get all dishes (you can modify this if needed)
    dishes = Dish.objects.all()

    # Get the category name (assuming 'category' is a related model)
    dish_category = dish.category.name

    # Split the ingredients in the view (before passing to template)
    ingredients = dish.ingredients.split(",")  

    # Render the template with all the necessary context
    return render(
        request,
        "dish.html",
        {
            "dish": dish,
            "dishes": dishes,
            "dish_category": dish_category,
            "ingredients": ingredients,  # Pass the split ingredients list
        },
    )


@login_required(login_url="login")
def foodbag(request):
    foodbag_items = FoodBag.objects.filter(user=request.user)
    total_price = sum(
        (item.dish.discounted_price or 0) * item.quantity for item in foodbag_items
    )
    cart_empty = not foodbag_items.exists()

    return render(
        request,
        "foodbag.html",
        {
            "foodbag_items": foodbag_items,
            "total_price": total_price,
            "cart_empty": cart_empty,
        },
    )


@login_required
def remove_dish(request, id):

    # Find the dish in the user's food bag

    dish = get_object_or_404(Dish, id=id)
    FoodBag.objects.filter(user=request.user, dish=dish).delete()

    return redirect("foodbag")


@login_required(login_url="login")
def add_to_bag(request, id):
    dish = get_object_or_404(Dish, id=id)

    # Check if the item is already in the FoodBag
    foodbag_item, created = FoodBag.objects.get_or_create(user=request.user, dish=dish)

    if created:
        foodbag_item.quantity = 1  # Increase quantity if it already exists
    else:
        foodbag_item.quantity += 1
    foodbag_item.save()

    return redirect("foodbag")



# Ensure only staff can access
def is_admin(user):
    return user.is_staff


# Admin panel for managing stock
@login_required
def manage_stock(request):
    if is_admin:
        food_items = Dish.objects.all()
        return render(request, "admin_food_stock.html", {"food_items": food_items})
    return (request, "This permission is only for admin")


# Add new food item
@login_required
def add_food(request):
    if is_admin:
        if request.method == "POST":
            form = FoodItemForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("manage_stock")
            else:
                form = FoodItemForm()
            return render(request, "add_food.html", {"form": form})
    return render(request, "This permission is only for admin")


# Update food stock
@login_required
def update_stock(request, food_id):

    if is_admin:

        food_item = get_object_or_404(Dish, id=food_id)
        if request.method == "POST":
            form = FoodItemForm(request.POST, instance=food_item)
            if form.is_valid():
                form.save()
                return redirect("manage_stock")
            else:
                form = FoodItemForm(instance=food_item)
                return render(request, "update_food.html", {"form": form})
    return render(request, "This permission is only for admin")


@login_required(login_url="login")
def order(request):
    try:
        user_profile = Profile.objects.get(user=request.user)
        cart_items = FoodBag.objects.filter(user=request.user)

        if not cart_items.exists():

            return redirect("foodbag")  # Redirect to cart page

        for item in cart_items:
            Order.objects.create(
                customer=user_profile,
                item=item.dish,
                status="confirmed",
                payment_status="success",
            )
            item.delete()  

        return redirect("order_summary") 

    except Exception as e:

        return redirect("foodbag")
