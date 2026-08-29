import csv
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum, Count
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST
from .forms import EnquiryForm, PurchaseForm, TestDriveForm
from .models import Vehicle, Wishlist, Enquiry, TestDrive, Sale, Payment
from .services import initialize_chapa, verify_chapa

def home(request):
    qs = Vehicle.objects.filter(available=True)
    q = request.GET.get("q","").strip()
    body = request.GET.get("body","")
    fuel = request.GET.get("fuel","")
    transmission = request.GET.get("transmission","")
    min_price = request.GET.get("min_price","")
    max_price = request.GET.get("max_price","")
    if q:
        qs = qs.filter(Q(title__icontains=q)|Q(make__icontains=q)|Q(model__icontains=q)|Q(stock_number__icontains=q))
    if body: qs = qs.filter(body_type=body)
    if fuel: qs = qs.filter(fuel_type=fuel)
    if transmission: qs = qs.filter(transmission=transmission)
    if min_price:
        try: qs = qs.filter(price__gte=Decimal(min_price))
        except: pass
    if max_price:
        try: qs = qs.filter(price__lte=Decimal(max_price))
        except: pass
    featured = qs.filter(Q(featured=True)|Q(promoted=True))[:8]
    return render(request,"cars/home.html",{"vehicles":qs.order_by("-promoted","-featured","-created_at"),"featured":featured})

def vehicle_detail(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    form = EnquiryForm()
    test_form = TestDriveForm()
    return render(request,"cars/detail.html",{"vehicle":vehicle,"form":form,"test_form":test_form})

@login_required
def wishlist_toggle(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    item, created = Wishlist.objects.get_or_create(user=request.user, vehicle=vehicle)
    if not created: item.delete()
    return redirect(vehicle.get_absolute_url())

def enquiry(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    if request.method == "POST":
        form = EnquiryForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False); obj.vehicle=vehicle
            if request.user.is_authenticated: obj.user=request.user
            obj.save(); messages.success(request,"Your enquiry has been sent.")
    return redirect(vehicle.get_absolute_url())

def test_drive(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    if request.method == "POST":
        form = TestDriveForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False); obj.vehicle=vehicle
            if request.user.is_authenticated: obj.user=request.user
            obj.save(); messages.success(request,"Test-drive request submitted.")
    return redirect(vehicle.get_absolute_url())

def buy_vehicle(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    if request.method == "POST":
        form = PurchaseForm(request.POST)
        if form.is_valid():
            sale = form.save(commit=False)
            sale.vehicle = vehicle
            sale.user = request.user if request.user.is_authenticated else None
            sale.amount = vehicle.price
            sale.save()
            if sale.payment_method == "chapa":
                checkout, error = initialize_chapa(sale)
                if checkout:
                    sale.chapa_reference = sale.reference
                    sale.save(update_fields=["chapa_reference"])
                    return redirect(checkout)
                messages.error(request, f"Chapa initialization failed: {error}")
            elif sale.payment_method == "bank":
                messages.info(request,"Bank-transfer instructions have been recorded. The dealer can verify payment from Admin.")
            else:
                messages.info(request,"Cash payment selected. Please contact the dealership.")
            return redirect("purchase_success", sale.reference)
    else:
        form = PurchaseForm(initial={"customer_name": request.user.get_full_name() if request.user.is_authenticated else "",
                                     "customer_email": request.user.email if request.user.is_authenticated else ""})
    return render(request,"cars/purchase.html",{"vehicle":vehicle,"form":form})
def invoice(request, reference):
    sale = get_object_or_404(
        Sale.objects.select_related("vehicle"),
        reference=reference,
    )

    return render(
        request,
        "cars/invoice.html",
        {
            "sale": sale,
        },
    )


@require_POST
def start_chapa_payment(request, reference):
    sale = get_object_or_404(
        Sale.objects.select_related("vehicle"),
        reference=reference,
    )

    # Do not start another payment for an already-paid sale.
    if sale.payment_status == "paid":
        messages.info(
            request,
            "This sale has already been paid.",
        )
        return redirect("invoice", sale.reference)

    # Do not start payment for a cancelled sale.
    if sale.status == "cancelled":
        messages.error(
            request,
            "This sale has been cancelled.",
        )
        return redirect("invoice", sale.reference)

    # Only Chapa sales may use this endpoint.
    if sale.payment_method != "chapa":
        messages.error(
            request,
            "This sale is not configured for Chapa payment.",
        )
        return redirect("invoice", sale.reference)

    # Current Chapa limit observed from your API response.
    if sale.amount > Decimal("1000000"):
        messages.error(
            request,
            "Chapa online payment is currently limited to "
            "1,000,000 ETB.",
        )
        return redirect("invoice", sale.reference)

    # Do not create another payment if one already succeeded.
    existing_success = Payment.objects.filter(
        sale=sale,
        status="success",
    ).first()

    if existing_success:
        messages.info(
            request,
            "This payment has already been recorded.",
        )
        return redirect("invoice", sale.reference)

    checkout, error = initialize_chapa(sale)

    if checkout:
        sale.chapa_reference = sale.reference
        sale.save(
            update_fields=[
                "chapa_reference",
            ]
        )

        return redirect(checkout)

    messages.error(
        request,
        f"Chapa initialization failed: {error}",
    )

    return redirect(
        "invoice",
        sale.reference,
    )
def purchase_success(request, reference):
    sale = get_object_or_404(Sale, reference=reference)
    return render(request,"cars/success.html",{"sale":sale})

def payment_callback(request, reference):
    sale = get_object_or_404(Sale, reference=reference)
    result = verify_chapa(sale.reference)
    status = str(result.get("data",{}).get("status","")).lower()
    if status == "success":
        sale.payment_status="paid"; sale.status="reserved"; sale.paid_at=timezone.now(); sale.save()
        Payment.objects.get_or_create(sale=sale, transaction_reference=sale.reference,
            defaults={"method":"chapa","amount":sale.amount,"status":"success","raw_response":result})
    return redirect("purchase_success", reference)

def payment_success(request, reference):
    return payment_callback(request, reference)

@login_required
def dashboard(request):
    sales = Sale.objects.filter(user=request.user).select_related("vehicle").order_by("-created_at")
    return render(request,"cars/dashboard.html",{"sales":sales})

def reports(request):
    sales = Sale.objects.all()
    total_sales = sales.filter(status="completed").aggregate(total=Sum("amount"))["total"] or 0
    paid = sales.filter(payment_status="paid").aggregate(total=Sum("amount"))["total"] or 0
    inventory = Vehicle.objects.aggregate(total=Count("id"))
    available = Vehicle.objects.filter(available=True).count()
    by_make = list(sales.values("vehicle__make").annotate(count=Count("id"), revenue=Sum("amount")).order_by("-revenue")[:10])
    recent = sales.select_related("vehicle").order_by("-created_at")[:10]
    return render(request,"reports/dashboard.html",{"total_sales":total_sales,"paid":paid,"inventory":inventory["total"] or 0,"available":available,"by_make":by_make,"recent":recent})

def export_sales_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="automarket_sales_report.csv"'
    writer = csv.writer(response)
    writer.writerow(["Reference","Vehicle","Customer","Amount","Payment Method","Payment Status","Sale Status","Created"])
    for s in Sale.objects.select_related("vehicle").order_by("-created_at"):
        writer.writerow([s.reference,str(s.vehicle),s.customer_name,s.amount,s.payment_method,s.payment_status,s.status,s.created_at])
    return response

