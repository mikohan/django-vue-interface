from rest_framework import serializers
from .models import Post, Categories
from product.models import Category


class PartCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ('id', 'name')


class CategorySerializerOnly(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ('id', 'name', 'slug')


class BlogPostSerializer(serializers.ModelSerializer):

    categories = CategorySerializer(many=True, read_only=True)

    parts_category = PartCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'text', 'image', 'date',
                  'slug', 'author', 'categories', 'parts_category')
        depth = 1
