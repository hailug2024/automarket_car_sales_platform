# AutoMarket Car Sales Platform

A Django-based car dealership and online vehicle sales platform designed for Ethiopia.

## Main features
- Vehicle inventory management
- Multiple vehicle images by view: exterior front, rear, left side, right side, interior front, interior rear, dashboard, engine, trunk and additional gallery
- Promoted/featured vehicles
- Advanced search and filtering
- Vehicle details and image gallery
- Customer registration/login
- Wishlist
- Enquiry/contact workflow
- Test-drive requests
- Booking/reservation workflow
- Payment methods: Chapa, bank transfer and cash/manual payment
- Chapa checkout initialization and callback verification hooks
- Sales/order management
- Customer and dealer dashboards
- Admin dashboard
- Sales, inventory, payment and customer reports
- CSV report export
- Responsive Bootstrap UI
- MySQL-ready configuration through environment variables

## Quick start

1. Create a virtual environment:
   `python -m venv venv`
2. Activate it on Windows:
   `venv\Scripts\activate`
3. Install:
   `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and edit values.
5. Run:
   `python manage.py migrate`
6. Create admin:
   `python manage.py createsuperuser`
7. Start:
   `python manage.py runserver`

Open:
- Public site: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/
- Reports: http://127.0.0.1:8000/reports/

## Chapa
Put your Chapa secret key in `.env`:
`CHAPA_SECRET_KEY=...`

Set:
`PUBLIC_BASE_URL=https://your-domain.com`

For local testing, use a public HTTPS tunnel when Chapa needs to reach a callback URL.

## MySQL
Set:
DB_ENGINE=mysql
DB_NAME=automarket
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=127.0.0.1
DB_PORT=3306

Then run migrations.

## Vehicle image workflow
When creating a vehicle, upload separate photos for:
- Exterior Front
- Exterior Rear
- Left Side
- Right Side
- Interior Front
- Interior Rear
- Dashboard
- Engine
- Trunk
- Gallery

The vehicle page automatically organizes these into a visual gallery.

## Production checklist
- Set DEBUG=False
- Set a strong SECRET_KEY
- Configure ALLOWED_HOSTS
- Use MySQL/PostgreSQL in production
- Configure HTTPS
- Configure persistent media storage
- Configure email/SMS notifications
- Configure Chapa production credentials
- Run `python manage.py collectstatic`
- Put Django behind Gunicorn/Uvicorn + Nginx or a managed hosting service
