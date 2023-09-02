# Generated by Django 4.0.4 on 2022-08-30 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0020_alter_customer_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='address',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='phone',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]