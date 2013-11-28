# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from django.contrib.auth.models import User
from models import *
import os
import uuid
import pickle


def index(request):
    return render_to_response('index.html', locals())


def ingredient(request):
    all_ingredients = Ingredient.objects.all()
    return render_to_response('ingredient.html', locals())

def recipe(request):
    all_recipes = Recipe.objects.all()
    return render_to_response('recipe.html', locals())


def recommend_ingredient(request):
    ingredients = request.REQUEST.get('ingredients', '')
    ingredients = ingredients[:-1]
    print ingredients
    recipes = Recipe.objects.all()[:10]

    if not request.user.is_authenticated():
        return HttpResponseRedirect("/")
    res = []
    for r in recipes:
        e = r.evaluate(request.user)
        res.append((r, e))
    return render_to_response('recommend.html', locals())


def recommend_recipe(request):
    recipe = request.REQUEST.get('recipe', '')
    recipe = recipe.replace(" ", "-")
    print recipe
    recipes = Recipe.objects.all()[:10]

    if not request.user.is_authenticated():
        return HttpResponseRedirect("/")
    res = []
    for r in recipes:
        e = r.evaluate(request.user)
        res.append((r, e))
    return render_to_response('recommend.html', locals())

def evaluate(request):
    user = request.user
    recipe_id = request.REQUEST.get('recipe_id', '')
    evaluate = request.REQUEST.get('evaluate', '')
    recipe = Recipe.objects.get(id=recipe_id)
    e = Evaluate()
    e.user = user
    e.recipe = recipe
    e.evaluate = evaluate
    e.save()

    return HttpResponse("I %s it" % evaluate)


def load_data(request):
    Ingredient.objects.all().delete()
    Recipe.objects.all().delete()

    ingredient_names = pickle.load(open("ingredients.p"))
    recipe_names = pickle.load(open("recipes.p"))
    ingredients_all_name = [i[28:] for i in ingredient_names]
    recipes_all_name = [n.split('/')[-1] for n in recipe_names]

    print len(ingredients_all_name) , len(recipes_all_name)

    for name in ingredients_all_name:
        ingredient = Ingredient()
        ingredient.name = name
        ingredient.save()

    for name in recipes_all_name:
        recipe = Recipe()
        recipe.name =  name
        recipe.save()

    return HttpResponse("OK!")



#====================auth system=========================================
def reg_page(request):
    return render_to_response('reg.html', locals())

def reg(request):
    username = request.REQUEST.get('username', '')
    password1 = request.REQUEST.get('password1', '')
    password2 = request.REQUEST.get('password2', '')
    if password1 != password2:
        return HttpResponse("<script>alert('Two passwords are not the same, Please try again.');top.location='/'</script>")
    if User.objects.filter(username = username):
        return HttpResponse("<script>alert('The user is already exist, Please try other username.');top.location='/'</script>")
    u = User()
    u.username = username
    u.set_password(password1)
    u.save()
    return HttpResponse("<script>alert('Successful registration!');top.location='/'</script>")

def login_page(request):
    return render_to_response('login.html', locals())

def login(request):
    username = request.REQUEST.get('username', '')
    password = request.REQUEST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        auth.login(request, user)
    else:
        return HttpResponse("<script>alert('The password is incorrect');top.location='/'</script>")
    return HttpResponseRedirect("/")

def logout(request):
    if request.user.is_authenticated():
        auth.logout(request)
    return HttpResponseRedirect("/")
#======================================================================
