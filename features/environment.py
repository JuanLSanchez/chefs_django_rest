import os

import django
from django.test.runner import DiscoverRunner
from rest_framework.test import APIClient

os.environ['DJANGO_SETTINGS_MODULE'] = 'chefs_django_rest.settings'


def before_all(context):
    django.setup()
    context.runner = DiscoverRunner()


def before_scenario(context, scenario):
    context.client = APIClient()
    load_fixtures(context, scenario)


def before_feature(context, feature):
    load_fixtures(context, feature)


def load_fixtures(context, feature):
    if not hasattr(context, 'fixtures'):
        context.fixtures = []
    for tag in feature.tags:
        if tag[:len('load_fixture/')] == 'load_fixture/':
            context.fixtures += [tag[len('load_fixture/'):]]