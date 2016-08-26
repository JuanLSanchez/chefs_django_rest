from behave import *
from django.contrib.auth.models import User
from rest_framework import status

use_step_matcher("parse")


# Load data ----------------------------------------------------------
@given("fixture '{fixture}'")
def load_fixture(context, fixture):
    context.fixtures = [fixture]


# Authentication ----------------------------------------------------------
@step("like any user")
def like_any_user(context):
    users = User.objects.all()
    if not users:
        raise ValueError("Users list empty!!")
    user = users[0]
    login_user(context, user)


# Creating request ----------------------------------------------------------
@when("making the get request to the url '{url}'")
def get_request(context, url):
    response = context.client.get(url, content_type='application/json', format='json')
    context.response = response


@when("making the post request to the url '{url}' with the body {body}")
def post_request(context, url, body):
    response = context.client.post(url, context.body[body], format='json')
    context.response = response


@when("making the put request to the url '{url}' with the attribute '{attribute}' and the body '{body}'")
def put_request(context, url, attribute, body):
    if not (hasattr(context, 'body') and body in context.body):
        raise ValueError("The body not contain the object %s" % body)
    if attribute not in context.body[body]:
        raise ValueError("The object not contain the attribute %s" % attribute)
    object_id = str(context.body[body][attribute])
    url_with_id = url + str(object_id) + '/'
    response = context.client.put(url_with_id, context.body[body],
                                  format='json')
    context.response = response


@when(
    "making the put request to the url '{url}' with the attribute "
    "as id '{attribute}' of '{body_id}' and the body '{body}'")
def put_request_with_other_id(context, url, attribute, body_id, body):
    if not (hasattr(context, 'body') and body_id in context.body):
        raise ValueError("The body not contain the object %s" % body_id)
    if not (hasattr(context, 'body') and body in context.body):
        raise ValueError("The body not contain the object %s" % body)
    if attribute not in context.body[body_id]:
        raise ValueError("The object not contain the attribute %s" % attribute)
    object_id = str(context.body[body_id][attribute])
    url_with_id = url + str(object_id) + '/'
    response = context.client.put(url_with_id, context.body[body],
                                  format='json')
    context.response = response


@when("making the delete request to the url '{url}'")
def step_impl(context, url):
    response = context.client.delete(url, format='json')
    context.response = response


@when("making the delete request with object, to the url '{url}' with the '{attribute}' of the object '{body}'")
def step_impl(context, url, attribute, body):
    if not (hasattr(context, 'body') and body in context.body):
        raise ValueError("The body not contain the object %s" % body)
    if attribute not in context.body[body]:
        raise ValueError("The object not contain the attribute %s" % attribute)
    response = context.client.delete(url + str(context.body[body][attribute]) + '/', format='json')
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
def check_status_is_403(context):
    check_status(context, status.HTTP_403_FORBIDDEN)


@then("status is 204 NOT CONTENT")
def step_impl(context):
    check_status(context, status.HTTP_204_NO_CONTENT)


# Modify object -------------------------------------------------------------------
@when("modify the string attribute '{attribute_name}' of the object body '{object_name}' by '{value}'")
def modify_attribute_value(context, attribute_name, object_name, value):
    if not (hasattr(context, 'body') and object_name in context.body):
        raise ValueError("The body not contain the object %s" % object_name)
    if attribute_name not in context.body[object_name]:
        raise ValueError("The object not contain the attribute %s" % attribute_name)
    context.body[object_name][attribute_name] = value


@when("modify the attribute '{attribute_name}' of the object body '{object_name}' "
      "by the attribute of object '{object_name_second}'")
def exchange_attribute_value(context, attribute_name, object_name, object_name_second):
    if not (hasattr(context, 'body') and object_name in context.body):
        raise ValueError("The body not contain the object %s" % object_name)
    if object_name_second not in context.body:
        raise ValueError("The body not contain the object %s" % object_name)
    if attribute_name not in context.body[object_name] or attribute_name not in context.body[object_name_second]:
        raise ValueError("The object not contain the attribute %s" % attribute_name)
    context.body[object_name][attribute_name] = context.body[object_name_second][attribute_name]


@when("modify the '{attribute}' id of the object body '{body}' by the principal id")
def step_impl(context, attribute, body):
    if not hasattr(context, 'user'):
        raise ValueError("Not found authenticated user")
    value = context.user.id
    modify_attribute_value(context, attribute, body, value)


# Check variables ---------------------------------------------------------------
@then("the '{variable1}' variable is equals to th '{variable2}' variable")
def step_impl(context, variable1, variable2):
    if not (hasattr(context, 'variable') and variable1 in context.variable):
        raise ValueError("Not contain the variable %s" % variable1)
    if variable2 not in context.variable:
        raise ValueError("Not contain the variable %s" % variable2)
    context.test.assertEqual(context.variable[variable1], context.variable[variable2])


# Check object ---------------------------------------------------------------------
@then("contain {key}")
def contain_key(context, key):
    if not hasattr(context.response, 'data'):
        raise ValueError("Not contain data")
    elif key not in context.response.data:
        raise ValueError("Not contain key: %s" % key)


@then("the '{key}' attribute is equal to '{value}'")
def compare_key_with_value(context, key, value):
    contain_key(context, key)
    context.test.assertEqual(context.response.data[key], value)


@then("the '{key}' attribute is equals to the '{attribute_name}' attribute of the '{object_name}' object")
def step_impl(context, key, attribute_name, object_name):
    if not (hasattr(context, 'body') and object_name in context.body):
        raise ValueError("The body not contain the object %s" % object_name)
    if attribute_name not in context.body[object_name]:
        raise ValueError("The object not contain the attribute %s" % attribute_name)
    context.test.assertEqual(context.response.data[key],
                             context.body[object_name][attribute_name])


@then("result size in page is {size:d}")
def compare_page_size(context, size):
    contain_key(context, 'results')
    context.test.assertEqual(len(context.response.data['results']), size)


@then("total result in page is {size:d}")
def compare_page_total_row(context, size):
    contain_key(context, 'count')
    context.test.assertEqual(context.response.data['count'], size)


# Auxiliary methods ------------------------------------------------------------------------
def add_to_variables(context, variable, value):
    if hasattr(context, 'variable'):
        context.variable[variable] = value
    else:
        context.variable = {variable: value}


def add_to_body(context, object_body, object_name):
    if hasattr(context, 'body'):
        context.body[object_name] = object_body
    else:
        context.body = {object_name: object_body}


def add_to_body_with_serializer(context, object_body, object_name, serializer):
    add_to_body(context, serializer(object_body).data, object_name)


def login_user(context, user):
    context.client.force_authenticate(user=user)
    context.user = user
