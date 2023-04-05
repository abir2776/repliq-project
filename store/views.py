"""Create views for categories."""
from rest_framework.views import APIView
from rest_framework import  permissions
from rest_framework.response import Response
from rest_framework import status
from core import models
from . import serializers

class CategoryView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self,request):
        categories = models.Category.objects.all()
        serializer = serializers.CategorySerializer(categories,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = serializers.CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
