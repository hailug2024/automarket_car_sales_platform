from django.conf import settings
from django.db import models
from django.urls import reverse
import uuid

class Vehicle(models.Model):
    BODY_TYPES = [("sedan","Sedan"),("suv","SUV"),("hatchback","Hatchback"),("pickup","Pickup"),("van","Van"),("coupe","Coupe"),("other","Other")]
    TRANSMISSIONS = [("automatic","Automatic"),("manual","Manual"),("cvt","CVT")]
    FUEL_TYPES = [("petrol","Petrol"),("diesel","Diesel"),("hybrid","Hybrid"),("electric","Electric")]
    title = models.CharField(max_length=200)
    stock_number = models.CharField(max_length=50, unique=True)
    make = models.CharField(max_length=80)
    model = models.CharField(max_length=80)
    year = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=14, decimal_places=2)
    currency = models.CharField(max_length=10, default="ETB")
    mileage = models.PositiveIntegerField(default=0)
    body_type = models.CharField(max_length=20, choices=BODY_TYPES, default="sedan")
    transmission = models.CharField(max_length=20, choices=TRANSMISSIONS, default="automatic")
    fuel_type = models.CharField(max_length=20, choices=FUEL_TYPES, default="petrol")
    engine = models.CharField(max_length=100, blank=True)
    color = models.CharField(max_length=60, blank=True)
    doors = models.PositiveIntegerField(default=4)
    seats = models.PositiveIntegerField(default=5)
    description = models.TextField(blank=True)
    featured = models.BooleanField(default=False)
    promoted = models.BooleanField(default=False)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.year} {self.make} {self.model}"

    def get_absolute_url(self):
        return reverse("vehicle_detail", args=[self.pk])

    @property
    def primary_image(self):
        return self.images.filter(is_primary=True).first() or self.images.first()

class VehicleImage(models.Model):
    VIEW_TYPES = [
        ("front","Exterior Front"),("rear","Exterior Rear"),("left","Left Side"),
        ("right","Right Side"),("interior_front","Interior Front"),
        ("interior_rear","Interior Rear"),("dashboard","Dashboard"),
        ("engine","Engine"),("trunk","Trunk"),("gallery","Additional Gallery"),
    ]
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="images")
    view_type = models.CharField(max_length=30, choices=VIEW_TYPES, default="gallery")
    image = models.ImageField(upload_to="vehicles/%Y/%m/")
    caption = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["view_type", "-uploaded_at"]

class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [models.UniqueConstraint(fields=["user","vehicle"], name="unique_wishlist")]

class Enquiry(models.Model):
    STATUS = [("new","New"),("contacted","Contacted"),("closed","Closed")]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=40)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS, default="new")
    created_at = models.DateTimeField(auto_now_add=True)

class TestDrive(models.Model):
    STATUS = [("requested","Requested"),("approved","Approved"),("completed","Completed"),("cancelled","Cancelled")]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=40)
    preferred_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS, default="requested")
    created_at = models.DateTimeField(auto_now_add=True)

class Sale(models.Model):
    STATUS = [("pending","Pending"),("reserved","Reserved"),("completed","Completed"),("cancelled","Cancelled")]
    PAYMENT = [("chapa","Chapa"),("bank","Bank Transfer"),("cash","Cash")]
    reference = models.CharField(max_length=20, unique=True, default=lambda: uuid.uuid4().hex[:12].upper())
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT)
    customer_name = models.CharField(max_length=120)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=40)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT, default="chapa")
    payment_status = models.CharField(max_length=20, default="unpaid")
    status = models.CharField(max_length=20, choices=STATUS, default="pending")
    chapa_reference = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)

class Payment(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name="payments")
    transaction_reference = models.CharField(max_length=120, unique=True)
    method = models.CharField(max_length=30)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    status = models.CharField(max_length=30, default="pending")
    raw_response = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
