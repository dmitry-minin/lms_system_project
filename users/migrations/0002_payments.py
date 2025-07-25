# Generated by Django 5.2.3 on 2025-06-26 18:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_date', models.DateField(auto_now_add=True, help_text='The date when the payment was made.', verbose_name='payment date')),
                ('amount', models.DecimalField(decimal_places=2, help_text='Enter the amount of the payment.', max_digits=10, verbose_name='amount')),
                ('payment_method', models.CharField(choices=[('cash', 'cash'), ('bank transfer', 'bank transfer')], help_text='Select the method of payment.', max_length=14, verbose_name='payment method')),
                ('course', models.ForeignKey(blank=True, help_text='Select the course for which the payment was made.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='payments', to='lms.course', verbose_name='course')),
                ('lesson', models.ForeignKey(blank=True, help_text='Select the lesson for which the payment was made. Optional.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='payments', to='lms.lesson', verbose_name='lesson')),
                ('user', models.ForeignKey(help_text='Select the user who made the payment.', on_delete=django.db.models.deletion.CASCADE, related_name='payments', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'payment',
                'verbose_name_plural': 'payments',
                'ordering': ['-payment_date'],
            },
        ),
    ]
