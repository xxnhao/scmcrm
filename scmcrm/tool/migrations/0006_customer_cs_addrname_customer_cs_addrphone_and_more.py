# Generated by Django 4.2.3 on 2023-08-31 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0005_alter_customer_update_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='cs_AddrName',
            field=models.CharField(default=None, max_length=50),
        ),
        migrations.AddField(
            model_name='customer',
            name='cs_AddrPhone',
            field=models.CharField(default=None, max_length=50),
        ),
        migrations.AddField(
            model_name='customer',
            name='cs_Address',
            field=models.CharField(default=None, max_length=200),
        ),
    ]
