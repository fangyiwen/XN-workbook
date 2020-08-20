# Generated by Django 3.0.4 on 2020-03-24 09:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_id', models.CharField(max_length=30, unique=True)),
                ('course_name', models.CharField(max_length=300, unique=True)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('course_instructor', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quiz_number', models.CharField(max_length=30, verbose_name='quiz No.')),
                ('quiz_id', models.CharField(default=models.CharField(max_length=30, verbose_name='quiz No.'), editable=False, max_length=30)),
                ('quiz_name', models.CharField(max_length=60)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('quiz_date', models.DateTimeField(verbose_name='the date of quiz')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workbook_app.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_number', models.CharField(max_length=30, verbose_name='question No.')),
                ('question_id', models.CharField(default=models.CharField(max_length=30, verbose_name='question No.'), editable=False, max_length=30)),
                ('question_text', models.CharField(max_length=300)),
                ('question_answer', models.CharField(max_length=30, verbose_name='Answer')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workbook_app.Quiz')),
            ],
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option_number', models.CharField(max_length=30, verbose_name='option No.')),
                ('option_text', models.CharField(max_length=300)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workbook_app.Question')),
            ],
        ),
    ]
