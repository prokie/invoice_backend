# Generated by Django 4.0.4 on 2022-08-29 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0018_alter_customer_social_security_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]