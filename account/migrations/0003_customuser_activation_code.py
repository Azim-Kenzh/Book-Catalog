# Generated by Django 4.2.2 on 2024-03-13 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_customuser_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='activation_code',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]