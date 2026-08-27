from django import forms
from .models import Enquiry, TestDrive, Sale

class EnquiryForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = ["name","email","phone","message"]
        widgets = {"message": forms.Textarea(attrs={"rows":4})}

class TestDriveForm(forms.ModelForm):
    class Meta:
        model = TestDrive
        fields = ["name","phone","preferred_date"]
        widgets = {"preferred_date": forms.DateTimeInput(attrs={"type":"datetime-local"})}

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ["customer_name","customer_email","customer_phone","payment_method"]
