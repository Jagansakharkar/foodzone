from django.db import models
from django.contrib.auth.models import User


# Contact Model
class Contact(models.Model):
    name = models.CharField(max_length=250)
    email = models.EmailField()
    subject = models.CharField(max_length=250)
    message = models.TextField()
    added_on = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Contact Table"


# Category Model
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to="categories/%Y/%m/%d")
    icon = models.CharField(max_length=50, blank=True)
    description = models.TextField()
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# Team Model
class Team(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    image = models.ImageField(upload_to="team")
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# Dish Model
class Dish(models.Model):
    name = models.CharField(max_length=200, unique=True)
    image = models.ImageField(upload_to="dishes/%Y/%m/%d")
    ingredients = models.TextField()
    details = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.FloatField()
    discounted_price = models.FloatField(blank=True, null=True)
    is_available = models.BooleanField(default=True)
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    stock = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.discounted_price is None or self.discounted_price > self.price:
            self.discounted_price = self.price
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Dish Table"


# Profile Model (User Profile)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(
        upload_to="profiles/%Y/%m/%d", null=True, blank=True
    )
    contact_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    loyalty_points = models.IntegerField(default=0)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name

    class Meta:
        verbose_name_plural = "Profile Table"


# Order Model
class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]

    customer = models.ForeignKey(Profile, on_delete=models.CASCADE)
    item = models.ForeignKey(Dish, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20, choices=ORDER_STATUS_CHOICES, default="pending"
    )
    invoice_id = models.CharField(max_length=100, blank=True)
    payer_id = models.CharField(max_length=100, blank=True)
    payment_status = models.CharField(
        max_length=20,
        choices=[("success", "Success"), ("failure", "Failure")],
        default="failure",
    )
    ordered_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order by {self.customer.user.first_name} ({self.status})"

    class Meta:
        verbose_name_plural = "Order Table"


# FoodBag Model (Shopping Cart)
class FoodBag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.dish.name} - {self.user.username}"

    class Meta:
        verbose_name_plural = "Food Bag"


# Coupon Model (Optional: for discount codes or promotions)
class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    expiry_date = models.DateTimeField()

    def __str__(self):
        return self.code

    class Meta:
        verbose_name_plural = "Coupon Table"


# Review Model (Optional: for user reviews on dishes)
class Review(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    customer = models.ForeignKey(Profile, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(
        choices=[
            (1, "1 Star"),
            (2, "2 Stars"),
            (3, "3 Stars"),
            (4, "4 Stars"),
            (5, "5 Stars"),
        ]
    )
    comment = models.TextField(blank=True)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.customer.user.first_name} on {self.dish.name}"

    class Meta:
        verbose_name_plural = "Review Table"
