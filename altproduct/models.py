""" Models declaration """

from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    """ Product category model. Consider that there is only one category per product. """

    name = models.CharField(max_length=50)
    alternative = models.BooleanField(default=None)

    def __str__(self):
        return self.name


class Brand(models.Model):
    """ Brand model. One brand per product. """

    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Store(models.Model):
    """ Store model. One store per product. """

    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class NutriGrade(models.Model):
    """ Nutrigrade model. Enum type. """

    NUTRIGRADE_CHOICES = (
        ('a', 'A'),
        ('b', 'B'),
        ('c', 'C'),
        ('d', 'D'),
        ('e', 'E'),
    )

    nutrigrade = models.CharField(max_length=1, choices=NUTRIGRADE_CHOICES)

    def __str__(self):
        return self.nutrigrade


class Product(models.Model):
    """ Product model. This is the main model : it has link with all other models. """

    name = models.CharField(max_length=200)
    description = models.TextField(max_length=200)
    link = models.URLField()
    image = models.URLField()
    nutrition_image = models.URLField()
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    brand = models.ForeignKey(Brand, on_delete=models.DO_NOTHING)
    store = models.ForeignKey(Store, on_delete=models.DO_NOTHING)
    nutrigrade = models.ForeignKey(NutriGrade, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


class FavouriteProduct(models.Model):
    """ Favourite product model. Reference table between Product and User. """

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)