from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveSmallIntegerField()

    class Meta:
        permissions = [
            ("customer", "Can perform customers actions"),
        ]


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='employee_images/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        permissions = [
            ("employee", "Can perform employee actions"),
        ]

    def __str__(self):
        return self.user.username


class ProductCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.OneToOneField(Customer, on_delete=models.CASCADE)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        Pending = "1", "Pending"
        Accepted = "2", "Accepted"
        Completed = "3", "Completed"

    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length=10, choices=OrderStatus.choices, default=OrderStatus.Pending)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)


class Coupon(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2)  # For example, 10.00 for 10%
    expiration_date = models.DateField()

    def __str__(self):
        return self.code


class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class GlossaryEntry(models.Model):
    term = models.CharField(max_length=255)
    definition = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.term


class Review(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    review = models.TextField()
    rating = models.PositiveSmallIntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.rating}/5"
