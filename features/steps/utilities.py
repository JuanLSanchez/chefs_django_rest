from collections import OrderedDict

from behave import *
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination

use_step_matcher("parse")


# Load data ----------------------------------------------------------
@given("fixture '{fixture}'")
def load_fixture(context, fixture):
    context.fixtures = [fixture]


# Authentication ----------------------------------------------------------
@step("as any user")
def step_impl(context):
    users = User.objects.all()
    if not users:
        raise ValueError("Users list empty!!")
    context.client.force_authenticate(user=users[0])


# Creating request ----------------------------------------------------------
@when("making the get request to the url '{url}'")
def get_request(context, url):
    response = context.client.get(url, content_type='application/json', format='json')
    context.response = response


@when("making the post request to the url '{url}' with the body {body}")
def step_impl(context, url, body):
    response = context.client.post(url, context.body[body], format='json')
    context.response = response


# Check Status ----------------------------------------------------------
@then("status code is {status_code:d}")
def check_status(context, status_code):
    context.test.assertEqual(context.response.status_code, status_code)


@then("status is 200 OK")
def check_status_is_200(context):
    check_status(context, status.HTTP_200_OK)


@then("status is 201 CREATED")
def check_status_is_201(context):
    check_status(context, status.HTTP_201_CREATED)


@then("status is 403 FORBIDDEN")
def check_status_is_401(context):
    check_status(context, status.HTTP_403_FORBIDDEN)


# Check object ---------------------------------------------------------------------
@then("contain {key}")
def contain_key(context, key):
    if not hasattr(context.response, 'data'):
        raise ValueError("Not contain data")
    elif not key in context.response.data:
        raise ValueError("Not contain key: %s" % key)


@then('the "{key}" attribute is equal to "{value}"')
def compare_key_with_value(context, key, value):
    contain_key(context, key)
    context.test.assertEqual(context.response.data[key], value)


@then("result size in page is {size:d}")
def compare_page_size(context, size):
    contain_key(context, 'results')
    context.test.assertEqual(len(context.response.data['results']), size)


@then("total result in page is {size:d}")
def compare_page_total_row(context, size):
    contain_key(context, 'count')
    context.test.assertEqual(context.response.data['count'], size)

