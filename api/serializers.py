from rest_framework import serializers

from api.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    id = serializers.ReadOnlyField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'description', 'created', 'updated', 'owner')
