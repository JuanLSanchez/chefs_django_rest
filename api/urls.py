from rest_framework import routers

from api.views.recipe_views import RecipeViewSet

simple_router = routers.SimpleRouter()
simple_router.register(r'recipes', RecipeViewSet)

urlpatterns = []

urlpatterns += simple_router.urls
