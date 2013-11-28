# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

class Ingredient(models.Model):
    name = models.CharField(max_length=64, blank=True , null=True)

class Recipe(models.Model):
    name = models.CharField(max_length=64, blank=True , null=True)
    ingredients = models.ManyToManyField(Ingredient)

    def evaluate(self, user):
        e = Evaluate.objects.filter(user=user, recipe=self)
        if e:
            return e[0].evaluate
        else:
            return None

class Evaluate(models.Model):
    user = models.ForeignKey(User)
    recipe = models.ForeignKey(Recipe)
    evaluate = models.CharField(max_length=64, blank=True , null=True)

