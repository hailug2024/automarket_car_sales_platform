import requests
from django.conf import settings

def initialize_chapa(sale):
    if not settings.CHAPA_SECRET_KEY:
        return None, "CHAPA_SECRET_KEY is not configured."

    payload = {
        "amount": str(sale.amount),
        "currency": sale.vehicle.currency,
        "email": sale.customer_email,
        "first_name": sale.customer_name.split()[0],
        "last_name": " ".join(sale.customer_name.split()[1:]) or "Customer",
        "tx_ref": sale.reference,
        "callback_url": f"{settings.PUBLIC_BASE_URL}/payment/callback/{sale.reference}/",
        "return_url": f"{settings.PUBLIC_BASE_URL}/payment/success/{sale.reference}/",
        "customization": {
            "title": "AutoMarket Vehicle Purchase",
            "description": f"Vehicle {sale.vehicle.stock_number}",
        },
    }
    headers = {"Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}", "Content-Type": "application/json"}
    try:
        response = requests.post(
            f"{settings.CHAPA_BASE_URL}/v1/transaction/initialize",
            json=payload, headers=headers, timeout=30
        )
        data = response.json()
        if response.ok and data.get("status") == "success":
            return data.get("data", {}).get("checkout_url"), None
        return None, data
    except requests.RequestException as exc:
        return None, str(exc)

def verify_chapa(tx_ref):
    headers = {"Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}"}
    try:
        response = requests.get(
            f"{settings.CHAPA_BASE_URL}/v1/transaction/verify/{tx_ref}",
            headers=headers, timeout=30
        )
        return response.json()
    except requests.RequestException as exc:
        return {"status":"error","message":str(exc)}
