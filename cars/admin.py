from django.contrib import admin
from .models import Vehicle, VehicleImage, Wishlist, Enquiry, TestDrive, Sale, Payment

class VehicleImageInline(admin.TabularInline):
    model = VehicleImage
    extra = 1

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ("title","stock_number","price","year","available","featured","promoted","created_at")
    list_filter = ("available","featured","promoted","body_type","fuel_type","transmission")
    search_fields = ("title","stock_number","make","model","color")
    inlines = [VehicleImageInline]

admin.site.register(Wishlist)
admin.site.register(Enquiry)
admin.site.register(TestDrive)
admin.site.register(Sale)
admin.site.register(Payment)
