""" Models declaration """

from django.db import models


class User(models.Model):
    """ User model. The base for authentification. """

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=50)


class Category(models.Model):
    """ Product category model. Consider that there is only one category per product. """

    name = models.CharField(max_length=50)


class Brand(models.Model):
    """ Brand model. One brand per product. """

    name = models.CharField(max_length=50)


class Store(models.Model):
    """ Store model. One store per product. """

    name = models.CharField(max_length=50)


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


class Product(models.Model):
    """ Product model. This is the main model : it have link with all other models. """

    name = models.CharField(max_length=50)
    description = models.TextField(max_length=30)
    link = models.URLField()
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    brand = models.ForeignKey(Brand, on_delete=models.DO_NOTHING)
    store = models.ForeignKey(Store, on_delete=models.DO_NOTHING)
    nutrigrade = models.ForeignKey(NutriGrade, on_delete=models.DO_NOTHING)


class FavouriteProduct(models.Model):
    """ Favourite product model. Reference table between Product and User. """

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
