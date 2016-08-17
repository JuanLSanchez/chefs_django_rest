from behave import *

use_step_matcher("parse")


@step("with the default recipe")
def step_impl(context):
    recipe = {'name': 'Recipe', 'description': 'Description Recipe00'}
    if hasattr(context, 'body'):
        context.body['recipe'] = recipe
    else:
        context.body = {'recipe': recipe}
