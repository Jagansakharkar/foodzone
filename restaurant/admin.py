from django.contrib import admin
from .models import Order

from django.contrib import admin
from restaurant.models import (
    Contact,
    Category,
    Team,
    Dish,
    Profile,
    Order,
    FoodBag,
    Review,
    Coupon,
)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "email", "subject", "added_on", "is_approved"]
    list_filter = ["is_approved", "added_on"]
    search_fields = ["name", "email", "subject"]
    list_editable = ["is_approved"]
    list_per_page = 20


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "added_on", "updated_on"]
    search_fields = ["name"]
    ordering = ["name"]
    # Removed prepopulated_fields since slug doesn't exist in your model


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "designation",
        "added_on",
        "updated_on",
    ]  # Changed 'role' to 'designation'
    search_fields = ["name", "designation"]  # Changed 'role' to 'designation'
    list_filter = ["designation"]  # Changed 'role' to 'designation'


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "is_available", "stock", "added_on")
    search_fields = (
        "name",
        "category__name",
        "ingredients",
        "details",
    )  # Changed 'description' to 'details'
    list_filter = ("category", "is_available")
    ordering = ("-added_on",)
    list_editable = ("price", "is_available", "stock")
    # Removed filter_horizontal since ingredients is TextField, not ManyToMany
    actions = ["update_stock", "make_available", "make_unavailable"]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "category",
                    "price",
                    "ingredients",
                    "details",
                )  # Changed 'description' to 'details'
            },
        ),
        ("Availability", {"fields": ("is_available", "stock")}),
        ("Pricing", {"fields": ("discounted_price",)}),  # Added discounted_price
        ("Media", {"fields": ("image",)}),
    )

    def update_stock(self, request, queryset):
        for dish in queryset:
            dish.stock += 10
            dish.save()
        self.message_user(
            request, "Stock updated successfully (+10 for each selected dish)."
        )

    update_stock.short_description = "Add 10 to stock"

    def make_available(self, request, queryset):
        queryset.update(is_available=True)

    make_available.short_description = "Mark selected dishes as available"

    def make_unavailable(self, request, queryset):
        queryset.update(is_available=False)

    make_unavailable.short_description = "Mark selected dishes as unavailable"


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "contact_number",
        "address",
        "updated_on",
    ]  # Removed 'is_verified'
    search_fields = [
        "user__username",
        "contact_number",
        "address",
    ]  # Changed 'phone' to 'contact_number'
    # Removed list_filter since 'is_verified' doesn't exist
    raw_id_fields = ["user"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "customer",
        "item",
        "status",
        "payment_status",
        "ordered_on",
    ]
    list_filter = ["status", "payment_status", "ordered_on"]
    search_fields = ["customer__user__username", "id", "item__name"]
    date_hierarchy = "ordered_on"
    readonly_fields = ["ordered_on"]
    list_per_page = 30
    list_editable = ["status", "payment_status"]


@admin.register(FoodBag)
class FoodBagAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "dish", "quantity", "added_on"]
    list_filter = ["added_on"]
    raw_id_fields = ["user", "dish"]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "customer",
        "dish",
        "rating",
        "added_on",
    ]  # Changed 'user' to 'customer'
    list_filter = ["rating", "added_on"]  # Changed 'created_at' to 'added_on'
    search_fields = ["customer__user__username", "dish__name"]  # Updated search fields
    readonly_fields = ["added_on"]  # Changed from 'created_at'


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = [
        "code",
        "discount_percentage",
        "expiry_date",
        "is_active",
    ]  # Updated field names
    list_filter = ["is_active", "expiry_date"]  # Updated field names
    search_fields = ["code"]
    list_editable = ["is_active", "discount_percentage"]  # Updated field names
