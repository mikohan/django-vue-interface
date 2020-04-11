# -*- coding: utf-8 -*-


from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from product.forms import KeyWordForm
import operator
import json
from django.core import serializers
from functools import reduce
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.db.models import Q
from product.models import Product, Units, CarModel, CarEngine, ProductImage, ProductVideos, Category
from brands.models import BrandsDict
from product.api.serializers import (ProductSerializer,
                                     UnitsSerializer,
                                     BrandsDictSerializer,
                                     CarModelSerializer,
                                     CarEngineSerializer,
                                     SessionSerializer,
                                     ImageSerializer,
                                     VideoSerializer,
                                     CarEngineSerializerSession,
                                     CarModelSerializerSession,
                                     CategorySerializer
                                     )
from django.http import Http404
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from .helpers import modify_input_for_multiple_files


class ProductList(APIView):

    
    def get(self, request, format=None):
        category_list = request.GET.get('category', None).split(',')
        print(category_list)
        snippets = Product.objects.filter(category__in=category_list).order_by('name')
        serializer = ProductSerializer(snippets, many=True)
        return Response(serializer.data)


class CategorizerSingleProduct(APIView):

    # Here is the logic find category for the string
    def cat(self, string):
        categories_qs = Category.objects.all().filter(id__gt=2000)
        string = string.lower()
        ready = list()

        for cat in categories_qs:
            minus = [x.minus.strip() for x in cat.to_category_minus.all()]
            plus = [x.plus.strip() for x in cat.to_category.all()]
            plus_single_list = []

            for p in plus:
                find = None
                single_list = p.split()
                plus_single_list.append(single_list)

            for sing_lst in plus_single_list:
                if all(plus_word in string for plus_word in sing_lst):
                    find = string
            if find:
                # print(minus)
                if any(minus_word in find for minus_word in minus):
                    pass
                else:
                    if (cat.id, cat.name) not in ready:
                        ready.append({'id': cat.id, 'name': cat.name})
                    #print(minus, plus)

        return ready

    def get(self, request, product_name):
        #product_name = request.GET.get('product_name')
        result = self.cat(product_name)
        serializer = CategorySerializer(result, many=True)
        print(result)
        return Response(serializer.data)


# Class to work with detailed product all methods exept
# POST post is right below there


class VideoViewSet(viewsets.ModelViewSet):
    serializer_class = VideoSerializer
    queryset = ProductVideos.objects.all()
    model = ProductVideos

    def get_queryset(self):
        if self.request.query_params.get('product_id'):
            product_id = self.request.query_params.get('product_id', None)
            queryset = self.model.objects.filter(product=product_id)
        else:
            queryset = self.model.objects.all()

        return queryset


class ImageViewSet(viewsets.ModelViewSet):
    # Here impemented very cool feature uploadeng multiple image trough serializer
    serializer_class = ImageSerializer
    queryset = ProductImage.objects.all().order_by('-created_date')

    def get_queryset(self):
        if self.request.query_params.get('product_id'):
            product_id = self.request.query_params.get('product_id', None)
            queryset = ProductImage.objects.filter(product=product_id)
        else:
            queryset = ProductImage.objects.all()

        return queryset

    def create(self, request, *args, **kwargs):
        product = request.data['product']

        # converts querydict to original dict
        images = dict((request.data).lists())['image']
        flag = 1
        arr = []
        for img_name in images:
            print(img_name)
            modified_data = modify_input_for_multiple_files(product, img_name)
            file_serializer = ImageSerializer(data=modified_data)
            if file_serializer.is_valid():
                file_serializer.save()
                arr.append(file_serializer.data)
            else:
                flag = 0

        if flag == 1:
            return Response(arr, status=status.HTTP_201_CREATED)
        else:
            return Response(arr, status=status.HTTP_400_BAD_REQUEST)


class DetailGet(APIView):
    def get(self, request, pk):
        product = Product.objects.get(id=pk)
        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        product = Product.objects.get(id=pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        product = Product.objects.get(id=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreateNewProduct(APIView):
    def post(self, request, format=None):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SelectFieldsUnitsView(APIView):
    def get(self, request):
        units_list = Units.objects.all()
        serializer = UnitsSerializer(units_list, many=True)
        return Response(serializer.data)


class SelectFieldsBrandsView(APIView):

    def get(self, request):
        units_list = BrandsDict.objects.all()
        serializer = BrandsDictSerializer(units_list, many=True)
        return Response(serializer.data)


class SelectFieldsModelsView(APIView):

    def get(self, request, pk):
        models_list = CarModel.objects.all()#filter(carmake=pk)
        serializer = CarModelSerializer(models_list, many=True)
        return Response(serializer.data)


class SelectNewProductModelsView(APIView):

    def get(self, request):
        models_list = CarModel.objects.all()
        serializer = CarModelSerializer(models_list, many=True)
        return Response(serializer.data)


class SelectFieldsEnginesView(APIView):

    def get(self, request):
        engine_list = CarEngine.objects.all()
        serializer = CarEngineSerializer(engine_list, many=True)
        return Response(serializer.data)

# Gettin session for set settings to user for create new product card


class SetSession(APIView):

    def get(self, request, *args, **kwargs):
        if request.session.get('car_model') is None:
            request.session['car_model'] = 1
            request.session['car_engine'] = 1

        qs = CarModel.objects.get(id=request.session.get('car_model'))
        e_qs = CarEngine.objects.get(id=request.session.get('car_engine'))
        data = {
            'car_model': qs,
            'car_engine': e_qs,
        }

        serializer = SessionSerializer(data)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):

        serializer = SessionSerializer(data=request.data)

        if serializer.is_valid():
            # print()
            qs = CarModel.objects.get(
                id=serializer.validated_data.get('car_model')['id'])
            e_qs = CarEngine.objects.get(
                id=serializer.validated_data.get('car_engine')['id'])
            print(qs.id)
            request.session['car_model'] = qs.id
            request.session['car_engine'] = e_qs.id
            data = {
                'car_model': qs,
                'car_engine': e_qs,
            }
            next_serializer = SessionSerializer(data)
            return Response(next_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class getPartCarModel(APIView):

    def get(self, request, *args, **kwargs):
        id_list = request.GET.get('pk').split(',')
        qs = CarModel.objects.filter(id__in=id_list)
        serializer = CarModelSerializerSession(qs, many=True)
        return Response(serializer.data)


class getPartCarEngine(APIView):

    def get(self, request, *args, **kwargs):
        qs = None
        if request.GET.get('pk') == 0:
            qs = CarEngine.objects.none()
        else:
            id_list = request.GET.get('pk').split(',')
            qs = CarEngine.objects.filter(id__in=id_list)
        serializer = CarEngineSerializerSession(qs, many=True)
        return Response(serializer.data)

