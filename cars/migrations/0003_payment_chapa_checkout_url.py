from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cars", "0002_alter_vehicleimage_options_alter_sale_reference"),
    ]

    operations = [
        migrations.AddField(
            model_name="payment",
            name="chapa_checkout_url",
            field=models.URLField(blank=True),
        ),
    ]