from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path(
        "vehicle/<int:pk>/",
        views.vehicle_detail,
        name="vehicle_detail",
    ),

    path(
        "vehicle/<int:pk>/wishlist/",
        views.wishlist_toggle,
        name="wishlist_toggle",
    ),

    path(
        "vehicle/<int:pk>/enquiry/",
        views.enquiry,
        name="enquiry",
    ),

    path(
        "vehicle/<int:pk>/test-drive/",
        views.test_drive,
        name="test_drive",
    ),

    path(
        "vehicle/<int:pk>/buy/",
        views.buy_vehicle,
        name="buy_vehicle",
    ),

    path(
        "invoice/<str:reference>/",
        views.invoice,
        name="invoice",
    ),

    path(
        "payment/start/<str:reference>/",
        views.start_chapa_payment,
        name="start_chapa_payment",
    ),

    path(
        "purchase/<str:reference>/success/",
        views.purchase_success,
        name="purchase_success",
    ),

    path(
        "payment/callback/<str:reference>/",
        views.payment_callback,
        name="payment_callback",
    ),

    path(
        "payment/success/<str:reference>/",
        views.payment_success,
        name="payment_success",
    ),

    path(
        "dashboard/",
        views.dashboard,
        name="dashboard",
    ),

    path(
        "reports/",
        views.reports,
        name="reports",
    ),

    path(
        "reports/sales.csv",
        views.export_sales_csv,
        name="export_sales_csv",
    ),
]