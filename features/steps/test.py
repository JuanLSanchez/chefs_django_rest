from behave import *

use_step_matcher("parse")


@given("{var} equals {number:d}")
def step_impl(context, var, number):
    if hasattr(context, 'var'):
        context.var[var] = number
    else:
        context.var = {var: number}


@when("sum {var1} and {var2}")
def step_impl(context, var1, var2):
    context.sum = context.var[var1] + context.var[var2]


@then("result sum equals {result:d}")
def step_impl(context, result):
    assert context.sum == result
