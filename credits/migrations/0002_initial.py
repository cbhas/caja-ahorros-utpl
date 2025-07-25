# Generated by Django 5.2.3 on 2025-07-24 06:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('credits', '0001_initial'),
        ('wallets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='credit',
            name='wallet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='credits', to='wallets.wallet'),
        ),
        migrations.AddField(
            model_name='creditpayment',
            name='credit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='credits.credit'),
        ),
    ]
