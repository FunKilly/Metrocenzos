# Generated by Django 3.0.4 on 2020-07-11 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('citizens', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='citizen',
            name='place_of_resident',
            field=models.CharField(choices=[('alexeyevskaya', 'Alexeyevskaya'), ('kievskaya', 'Kievskaya'), ('paveletskaya', 'Paveletskaya'), ('kremlin', 'Kremlin'), ('polis', 'polis'), ('rizhskaya', 'Rizhskaya'), ('sevastopolskaya', 'Sevastopolskaya'), ('smolenskaya', 'Smolenskaya'), ('depot', 'Depot'), ('lubyanka', 'Lubyanka'), ('unknown', 'Unknown')], max_length=50),
        ),
    ]