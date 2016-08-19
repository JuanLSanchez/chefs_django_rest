from behave import *
from django.contrib.auth.models import User

from api.models import Recipe
from api.serializers import RecipeSerializer
from features.steps.utilities import login_user, add_to_body, add_to_body_with_serializer

use_step_matcher("parse")


@given("like a user with recipes")
def like_user_with_recipe(context):
    users = User.objects.all().exclude(recipes=None)
    if not users:
        raise ValueError("Users list empty!!")
    user = users[0]
    login_user(context, user)


@given("like a user without recipes")
def like_user_without_recipe(context):
    if not (hasattr(context, 'user') and context.user):
        users = User.objects.all().filter(recipes=None)
    if not users:
        raise ValueError("Users list empty!!")
    user = users[0]
    login_user(context, user)


@given("with any recipe of the user as '{id}'")
def with_any_user_recipe(context, id):
    if not (hasattr(context, 'user') and context.user):
        raise ValueError("Not initialize user")
    recipes = Recipe.objects.filter(owner=context.user)
    if not recipes:
        raise ValueError("User without recipes")
    add_to_body_with_serializer(context, recipes[0], id, RecipeSerializer)


@given("with the default recipe as '{id}'")
def with_default_recipe(context, id):
    recipe = {'name': 'Recipe', 'description': 'Description Recipe00'}
    add_to_body(context, recipe, id)


@given("with any recipe as '{id}'")
def step_impl(context, id):
    recipes = Recipe.objects.all()
    if not recipes:
        raise ValueError("Database without recipes")
    add_to_body_with_serializer(context, recipes[0], id, RecipeSerializer)


@step("with any recipe of other user as '{id}'")
def step_impl(context, id):
    if not (hasattr(context, 'user') and context.user):
        raise ValueError("Not initialize user")
    recipes = Recipe.objects.exclude(owner=context.user)
    if not recipes:
        raise ValueError("Not found recipes of other user")
    add_to_body_with_serializer(context, recipes[0], id, RecipeSerializer)