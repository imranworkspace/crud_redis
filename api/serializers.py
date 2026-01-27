from rest_framework import serializers

class StudentSerializers(serializers.Serializer):
    username = serializers.CharField(max_length=25)
    email = serializers.EmailField()