# Generated by Django 3.2.7 on 2021-10-04 11:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0002_set_enum_set'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=63, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('enum_set', models.IntegerField()),
                ('id_syllabus', models.ForeignKey(blank=True, db_column='id_syllabus', null=True, on_delete=django.db.models.deletion.CASCADE, to='problems.syllabus')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CartTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enum_task', models.IntegerField()),
                ('criteries', models.TextField(blank=True, null=True)),
                ('id_cart', models.ForeignKey(db_column='id_set', on_delete=django.db.models.deletion.CASCADE, to='problems.cart')),
                ('id_task', models.ForeignKey(db_column='id_task', on_delete=django.db.models.deletion.CASCADE, to='problems.problem')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
