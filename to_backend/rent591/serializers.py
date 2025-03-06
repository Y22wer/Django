from rest_framework import serializers
from .models import Todo , House

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = '__all__'
        
class HouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = '__all__'