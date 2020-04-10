# -*- coding: utf-8 -*-

from rest_framework import serializers
from product.models import (Product, ProductImage,
                            Category, Units, CarModel, CarMake, CarEngine,
                            Country, BrandsDict,
                            ProductVideos,
                            Category)



class CategorySerializer(serializers.Serializer):
    
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = ['id',
                  'image',
                  'product',
                  'img150',
                  'img245',
                  'img500',
                  'img800'
                  ]


class VideoSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductVideos
        fields = ['id', 'url', 'product', 'youtube_id']


class UnitsSerializer(serializers.ModelSerializer):
    id = serializers.ModelField(model_field=Units()._meta.get_field('id'))

    class Meta:
        model = Units
        fields = ('id', 'unit_name')


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class CarMakeSerializer(serializers.ModelSerializer):
    country = CountrySerializer()

    class Meta:
        model = CarMake
        fields = '__all__'


class CarModelSerializer(serializers.ModelSerializer):
    id = serializers.ModelField(model_field=CarModel()._meta.get_field('id'))
    
    carmake = CarMakeSerializer(
        instance=CarMake, required=False, read_only=True)

    class Meta:
        model = CarModel
        fields = ['id', 'carmake', 'name']


class CarEngineSerializer(serializers.ModelSerializer):

    class Meta:
        model = CarEngine
        fields = '__all__'


class CarEngineSerializerSession(serializers.ModelSerializer):
    #id = serializers.ModelField(model_field=CarEngine()._meta.get_field('id'))

    class Meta:
        model = CarEngine
        fields = '__all__'


class CarModelSerializerSession(serializers.ModelSerializer):
    #id = serializers.ModelField(model_field=CarModel()._meta.get_field('id'))

    class Meta:
        model = CarModel
        fields = '__all__' #['id', 'name']


class SessionSerializer(serializers.Serializer):
    car_model = CarModelSerializerSession(
        instance=CarModel)  # serializers.IntegerField()
    car_engine = CarEngineSerializerSession(
        instance=CarEngine)  # serializers.IntegerField()

    class Meta:
        fields = '__all__'


class BrandsDictSerializer(serializers.ModelSerializer):
    id = serializers.ModelField(model_field=BrandsDict()._meta.get_field('id'))

    class Meta:
        model = BrandsDict
        fields = ('id', 'brand')


class ProductSerializer(serializers.ModelSerializer):
    #unit = UnitsSerializer(instance=Units)
    #car_model = CarModelSerializer(instance=CarModel, required=True)
    # engine = CarEngineSerializer(instance=CarEngine, required=False)
    #car_make = CarMakeSerializer(instance=CarMake, required=True)

    class Meta:
        model = Product
        #fields = '__all__'
        fields = ['id',
                  'name',
                  'name2',
                  'cat_number',
                  # 'created_date',
                  # 'updated_date',
                  'category',
                  'slug',
                  'brand',
                  'car_model',
                  'unit',
                  'one_c_id',
                  'active',
                  'engine'
                  ]

        # represent full fields of serializer nested objects
        depth = 0

    #Create method
    def create(self, validated_data):
        #car models array
        car_model_data = validated_data.pop('car_model')
        car_model_list = [x.id for x in car_model_data]
        car_model_qs = CarModel.objects.filter(id__in=car_model_list)
        # engines array
        car_engine_data = validated_data.pop('engine')
        car_engine_list = [x.id for x in car_engine_data]
        car_engine_qs = CarEngine.objects.filter(id__in=car_engine_list)

        
        brand_qs = BrandsDict.objects.get(id=validated_data.get('brand').id)
        unit_qs = Units.objects.get(id=validated_data['unit'].id)
       

        product = Product.objects.create(
            name=validated_data['name'],
            name2=validated_data['name2'],
            cat_number=validated_data['cat_number'],
            brand=brand_qs,
            #car_model=car_model_qs,
            unit=unit_qs,
            one_c_id=validated_data['one_c_id'],
            active=validated_data['active']
        )

        product.save()
        for engine in car_engine_list:
            product.engine.add(CarEngine.objects.get(id=engine))

        for car in car_model_list:
            product.car_model.add(CarModel.objects.get(id=car))

        return product

    def update(self, instance, validated_data):

        # Менее Адский гемор по вложенной сериализации
        engine_data = validated_data.get('engine')
        try:
            engine_qs = CarEngine.objects.get(id=engine_data.id)
            instance.engine = engine_qs
        except:
            pass

        unit_data = validated_data.pop('unit')
        try:
            unit_qs = Units.objects.get(id=unit_data.id)
            instance.unit = unit_qs
        except:
            pass

        # Brand updating logic
        try:
            brand_qs = BrandsDict.objects.get(
                id=validated_data.get('brand').id)
            instance.brand = brand_qs
        except:
            pass

        # Car model update logic
        carmodel_data = validated_data.pop('car_model')
        car_model_list = [x.id for x in carmodel_data]
        car_model_qs = CarModel.objects.filter(model_product=instance.id)

        # Car Engine update logic
        car_engine_data = validated_data.pop('engine')
        car_engine_list = [_.id for _ in car_engine_data]
        car_engine_qs = CarEngine.objects.filter(car_related_engine=instance.id)

        instance.brand = validated_data.get('brand', instance.brand)
        instance.name = validated_data.get('name', instance.name)
        instance.name2 = validated_data.get('name2', instance.name2)
        instance.cat_number = validated_data.get(
            'cat_number', instance.cat_number)
        instance.slug = validated_data.get('slug', instance.slug)
        instance.one_c_id = validated_data.get('one_c_id', instance.one_c_id)
        instance.active = validated_data.get('active', instance.active)
        instance.save()
        
        
        for car in car_model_qs:
            instance.car_model.remove(car)
        for car_l in car_model_list:
            instance.car_model.add(CarModel.objects.get(id=car_l))

        #Car engine making references
        for engine in car_engine_qs:
            instance.engine.remove(engine)
        for eng in car_engine_list:
            instance.engine.add(CarEngine.objects.get(id=eng))

        return instance
