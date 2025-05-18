from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("menu/", views.menu, name="menu"),
    path("contact/", views.contact_us, name="contact"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("foodbag/", views.foodbag, name="foodbag"),
    path("order/",views.order,name="order"),
    path("dishes/<int:id>", views.dishes, name="dishes"),
    path("dish/<int:id>/", views.single_dish, name="dish"),
    path("add_to_bag/<int:id>/", views.add_to_bag, name="add_to_bag"),
    path("remove_dish/<int:id>", views.remove_dish, name="remove_dish"),
    path("check_user_exists/", views.check_user_exists, name="check_user_exist"),
    # path("admin/stock/", views.manage_stock, name="manage_stock"),
    # path("admin/stock/add/", views.add_food, name="add_food"),
    # path("admin/stock/update/<int:food_id>/", views.update_stock, name="update_stock"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
