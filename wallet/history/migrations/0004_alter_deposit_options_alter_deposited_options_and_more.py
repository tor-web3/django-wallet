# Generated by Django 4.0.4 on 2022-05-28 10:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wallet', '0009_remove_state_address_remove_state_rpc_delete_rpc_and_more'),
        ('history', '0003_deposit_deposit_alter_deposit_counterparty'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='deposit',
            options={'ordering': ['-created_time'], 'verbose_name': 'Temp Deposit', 'verbose_name_plural': 'Temp Deposit'},
        ),
        migrations.AlterModelOptions(
            name='deposited',
            options={'ordering': ['-created_time'], 'verbose_name': 'Deposited', 'verbose_name_plural': 'Deposited'},
        ),
        migrations.CreateModel(
            name='Withdraw',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(editable=False, max_length=64, verbose_name='History UUID')),
                ('txid', models.CharField(blank=True, default=None, editable=False, max_length=256, null=True, unique=True, verbose_name='TXID')),
                ('counterparty_address', models.CharField(max_length=128, verbose_name='CounterParty Address')),
                ('amount', models.DecimalField(decimal_places=8, max_digits=32, verbose_name='Amount')),
                ('fee', models.DecimalField(decimal_places=8, default=0, max_digits=32, verbose_name='Fee')),
                ('memo', models.CharField(blank=True, default='', help_text='Label/Tag/Memo', max_length=128, null=True, verbose_name='Memo')),
                ('status', models.CharField(blank=True, choices=[('SUBMITTED', 'submitted'), ('AUDITED', 'audited'), ('REJECT', 'reject'), ('WITHDRAWING', 'withdrawing'), ('WITHDRAWN', 'withdrawn'), ('ERROR', 'error')], default='SUBMITTED', editable=False, max_length=32, null=True, verbose_name='Status')),
                ('error_info', models.CharField(blank=True, default='', editable=False, max_length=255, null=True, verbose_name='Error Info')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='Created Time')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='Updated Time')),
                ('finished_time', models.DateTimeField(blank=True, default=None, editable=False, null=True, verbose_name='Finished Time')),
                ('block_time', models.DateTimeField(blank=True, default=None, editable=False, null=True, verbose_name='Block Time')),
                ('counterparty', models.ForeignKey(blank=True, default=None, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='wallet_history_withdraw', to=settings.AUTH_USER_MODEL, verbose_name='Internal CounterParty ID')),
                ('token', models.ForeignKey(default=None, editable=False, on_delete=django.db.models.deletion.CASCADE, to='wallet.token')),
            ],
        ),
    ]
