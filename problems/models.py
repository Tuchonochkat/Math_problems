# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Type(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1023, blank=True, null=True)

    class Meta:
        db_table = 'type'

    def __str__(self):
        return self.name

class Theme(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'theme'

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=63)

    class Meta:
        db_table = 'category'

    def __str__(self):
        return self.name

class ThemeCategory(models.Model):
    id_theme = models.ForeignKey(Theme, models.CASCADE, db_column='id_theme')
    id_category = models.ForeignKey(Category, models.CASCADE, db_column='id_category', blank=True, null=True)

    class Meta:
        db_table = 'theme_category'


class Problem(models.Model):
    id_google = models.IntegerField()
    task = models.TextField()
    solution = models.TextField(blank=True, null=True)
    img_task = models.CharField(max_length=255, blank=True, null=True)
    img_solution = models.CharField(max_length=255, blank=True, null=True)
    id_type = models.ForeignKey('Type', models.CASCADE, db_column='id_type', blank=True, null=True)
    id_orig = models.IntegerField(blank=True, null=True)
    date_using = models.DateField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'problem'


class ProblemCategory(models.Model):
    id_task = models.ForeignKey(Problem, models.CASCADE, db_column='id_task')
    id_theme_cat = models.ForeignKey('ThemeCategory', models.CASCADE, db_column='id_theme_cat')

    class Meta:
        db_table = 'problem_category'


class Trajectory(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'trajectory'


class Syllabus(models.Model):
    id_trajectory = models.ForeignKey('Trajectory', models.CASCADE, db_column='id_trajectory', blank=True, null=True)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'syllabus'


class Set(models.Model):
    id_syllabus = models.ForeignKey('Syllabus', models.CASCADE, db_column='id_syllabus', blank=True, null=True)
    name = models.CharField(max_length=63, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'set'


class SetTask(models.Model):
    id_set = models.ForeignKey(Set, models.CASCADE, db_column='id_set')
    id_task = models.ForeignKey(Problem, models.CASCADE, db_column='id_task')
    enum_task = models.IntegerField()
    criteries = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'set_task'


class Comments(models.Model):
    id_set_task = models.ForeignKey('SetTask', models.CASCADE, db_column='id_set_task')
    author = models.CharField(max_length=63)
    date = models.TimeField()
    description = models.TextField()

    class Meta:
        db_table = 'comments'