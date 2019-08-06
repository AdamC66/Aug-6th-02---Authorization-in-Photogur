# Generated by Django 2.2.3 on 2019-07-26 18:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('photogur', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('message', models.TextField()),
                ('picture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='photogur.Picture')),
            ],
        ),
    ]
