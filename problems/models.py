from django.contrib.auth.models import User
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

    def __str__(self):
        if self.id_category:
            return '{}. {}.'.format(self.id_theme, self.id_category)
        else:
            return '{}.'.format(self.id_theme)


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

    def __str__(self):
        return self.task

    def categories(self):
        return ThemeCategory.objects.filter(problemcategory__id_task=self)

    def dubles(self):
        return Problem.objects.filter(id_orig=self.id_orig).exclude(id=self.id)

    def type(self):
        return Type.objects.get(id=self.id_type)

    def syllabuses(self):
        sets = Set.objects.values_list('id_syllabus', flat=True).filter(settask__id_task=self)
        return Syllabus.objects.filter(id__in=sets).distinct('id')


class ProblemCategory(models.Model):
    id_task = models.ForeignKey(Problem, models.CASCADE, db_column='id_task')
    id_theme_cat = models.ForeignKey('ThemeCategory', models.CASCADE, db_column='id_theme_cat')

    class Meta:
        db_table = 'problem_category'


class Trajectory(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'trajectory'

    def __str__(self):
        return self.name

    def syllabuses(self):
        return Syllabus.objects.filter(id_trajectory=self.id)


class Syllabus(models.Model):
    id_trajectory = models.ForeignKey('Trajectory', models.CASCADE, db_column='id_trajectory', blank=True, null=True)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'syllabus'

    def __str__(self):
        return self.name

    def sets(self):
        return Set.objects.filter(id_syllabus=self.id).order_by('enum_set')


class SetCart(models.Model):
    id_syllabus = models.ForeignKey('Syllabus', models.CASCADE, db_column='id_syllabus', blank=True, null=True)
    name = models.CharField(max_length=63, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    enum_set = models.IntegerField()

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Set(SetCart):

    class Meta:
        db_table = 'set'

    def tasks(self):
        return SetTask.objects.filter(id_set=self.id).order_by('enum_task')


class SetCartTask(models.Model):
    id_task = models.ForeignKey(Problem, models.CASCADE, db_column='id_task')
    enum_task = models.IntegerField()
    criteries = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True


class SetTask(SetCartTask):
    id_set = models.ForeignKey(Set, models.CASCADE, db_column='id_set')

    class Meta:
        db_table = 'set_task'

    def comments(self):
        return Comments.objects.filter(id_set_task=self).order_by('date')


class Comments(models.Model):
    id_set_task = models.ForeignKey('SetTask', models.CASCADE, db_column='id_set_task')
    author = models.CharField(max_length=63)
    date = models.TimeField()
    description = models.TextField()

    class Meta:
        db_table = 'comments'

    def __str__(self):
        return self.description


class Cart(SetCart):
    user = models.OneToOneField(User, models.CASCADE)
    enum_set = models.IntegerField(blank=True, null=True)

    def tasks(self):
        return CartTask.objects.filter(id_set=self.id).order_by('enum_task')


class CartTask(SetCartTask):
    id_cart = models.ForeignKey(Cart, models.CASCADE, db_column='id_cart')
