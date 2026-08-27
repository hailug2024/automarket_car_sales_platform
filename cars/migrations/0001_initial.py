from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid

class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(name="Vehicle", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("title", models.CharField(max_length=200)),("stock_number", models.CharField(max_length=50, unique=True)),
            ("make", models.CharField(max_length=80)),("model", models.CharField(max_length=80)),("year", models.PositiveIntegerField()),
            ("price", models.DecimalField(decimal_places=2,max_digits=14)),("currency", models.CharField(default="ETB",max_length=10)),
            ("mileage", models.PositiveIntegerField(default=0)),("body_type", models.CharField(choices=[("sedan","Sedan"),("suv","SUV"),("hatchback","Hatchback"),("pickup","Pickup"),("van","Van"),("coupe","Coupe"),("other","Other")],default="sedan",max_length=20)),
            ("transmission", models.CharField(choices=[("automatic","Automatic"),("manual","Manual"),("cvt","CVT")],default="automatic",max_length=20)),
            ("fuel_type", models.CharField(choices=[("petrol","Petrol"),("diesel","Diesel"),("hybrid","Hybrid"),("electric","Electric")],default="petrol",max_length=20)),
            ("engine", models.CharField(blank=True,max_length=100)),("color", models.CharField(blank=True,max_length=60)),
            ("doors", models.PositiveIntegerField(default=4)),("seats", models.PositiveIntegerField(default=5)),("description", models.TextField(blank=True)),
            ("featured", models.BooleanField(default=False)),("promoted", models.BooleanField(default=False)),("available", models.BooleanField(default=True)),
            ("created_at", models.DateTimeField(auto_now_add=True)),("updated_at", models.DateTimeField(auto_now=True)),
        ]),
        migrations.CreateModel(name="VehicleImage", fields=[
            ("id",models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")),
            ("view_type",models.CharField(choices=[("front","Exterior Front"),("rear","Exterior Rear"),("left","Left Side"),("right","Right Side"),("interior_front","Interior Front"),("interior_rear","Interior Rear"),("dashboard","Dashboard"),("engine","Engine"),("trunk","Trunk"),("gallery","Additional Gallery")],default="gallery",max_length=30)),
            ("image",models.ImageField(upload_to="vehicles/%Y/%m/")),("caption",models.CharField(blank=True,max_length=200)),("is_primary",models.BooleanField(default=False)),
            ("uploaded_at",models.DateTimeField(auto_now_add=True)),
            ("vehicle",models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name="images",to="cars.vehicle")),
        ]),
        migrations.CreateModel(name="Wishlist", fields=[
            ("id",models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")),("created_at",models.DateTimeField(auto_now_add=True)),
            ("user",models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,to=settings.AUTH_USER_MODEL)),("vehicle",models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,to="cars.vehicle")),
        ]),
        migrations.AddConstraint(model_name="wishlist",constraint=models.UniqueConstraint(fields=("user","vehicle"),name="unique_wishlist")),
        migrations.CreateModel(name="Enquiry", fields=[
            ("id",models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")),("name",models.CharField(max_length=120)),("email",models.EmailField(max_length=254)),("phone",models.CharField(max_length=40)),("message",models.TextField()),("status",models.CharField(choices=[("new","New"),("contacted","Contacted"),("closed","Closed")],default="new",max_length=20)),("created_at",models.DateTimeField(auto_now_add=True)),
            ("user",models.ForeignKey(blank=True,null=True,on_delete=django.db.models.deletion.SET_NULL,to=settings.AUTH_USER_MODEL)),("vehicle",models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,to="cars.vehicle"))]),
        migrations.CreateModel(name="TestDrive", fields=[
            ("id",models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")),("name",models.CharField(max_length=120)),("phone",models.CharField(max_length=40)),("preferred_date",models.DateTimeField()),("status",models.CharField(choices=[("requested","Requested"),("approved","Approved"),("completed","Completed"),("cancelled","Cancelled")],default="requested",max_length=20)),("created_at",models.DateTimeField(auto_now_add=True)),
            ("user",models.ForeignKey(blank=True,null=True,on_delete=django.db.models.deletion.SET_NULL,to=settings.AUTH_USER_MODEL)),("vehicle",models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,to="cars.vehicle"))]),
        migrations.CreateModel(name="Sale", fields=[
            ("id",models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")),("reference",models.CharField(default=lambda: uuid.uuid4().hex[:12].upper(),max_length=20,unique=True)),
            ("customer_name",models.CharField(max_length=120)),("customer_email",models.EmailField(max_length=254)),("customer_phone",models.CharField(max_length=40)),
            ("amount",models.DecimalField(decimal_places=2,max_digits=14)),("payment_method",models.CharField(choices=[("chapa","Chapa"),("bank","Bank Transfer"),("cash","Cash")],default="chapa",max_length=20)),("payment_status",models.CharField(default="unpaid",max_length=20)),
            ("status",models.CharField(choices=[("pending","Pending"),("reserved","Reserved"),("completed","Completed"),("cancelled","Cancelled")],default="pending",max_length=20)),
            ("chapa_reference",models.CharField(blank=True,max_length=100)),("created_at",models.DateTimeField(auto_now_add=True)),("paid_at",models.DateTimeField(blank=True,null=True)),
            ("user",models.ForeignKey(blank=True,null=True,on_delete=django.db.models.deletion.SET_NULL,to=settings.AUTH_USER_MODEL)),("vehicle",models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,to="cars.vehicle"))]),
        migrations.CreateModel(name="Payment", fields=[
            ("id",models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")),("transaction_reference",models.CharField(max_length=120,unique=True)),("method",models.CharField(max_length=30)),("amount",models.DecimalField(decimal_places=2,max_digits=14)),("status",models.CharField(default="pending",max_length=30)),("raw_response",models.JSONField(blank=True,default=dict)),("created_at",models.DateTimeField(auto_now_add=True)),
            ("sale",models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name="payments",to="cars.sale"))]),
    ]
