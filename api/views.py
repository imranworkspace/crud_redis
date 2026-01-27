from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.core.cache import cache

from .models import StudentModel
from .serializers import StudentSerializers

@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def crud(request, pk=None):

    # ---------- GET (List or Retrieve) ----------
    if request.method == 'GET':

        # 🔹 Cache key
        cache_key = f"student:{pk}" if pk else "student:list"

        # 🔹 Try Redis first
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)

        if pk:
            print('######################## hit db')
            student = get_object_or_404(StudentModel, pk=pk)
            serializer = StudentSerializers(student)
            data = serializer.data

        else:
            print('######################## hit db')
            students = StudentModel.objects.only('id', 'username', 'email')
            serializer = StudentSerializers(students, many=True)
            data = serializer.data

        # 🔹 Store in Redis (5 minutes)
        cache.set(cache_key, data, timeout=300)

        return Response(data, status=status.HTTP_200_OK)

    # ---------- POST (Create) ----------
    if request.method == 'POST':
        serializer = StudentSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()

            # 🔥 Invalidate list cache
            cache.delete("student:list")

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # ---------- PUT (Full Update) ----------
    if request.method == 'PUT':
        student = get_object_or_404(StudentModel, pk=pk)
        serializer = StudentSerializers(student, data=request.data)
        if serializer.is_valid():
            serializer.save()

            # 🔥 Invalidate caches
            cache.delete(f"student:{pk}")
            cache.delete("student:list")

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # ---------- PATCH (Partial Update) ----------
    if request.method == 'PATCH':
        student = get_object_or_404(StudentModel, pk=pk)
        serializer = StudentSerializers(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            # 🔥 Invalidate caches
            cache.delete(f"student:{pk}")
            cache.delete("student:list")

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # ---------- DELETE ----------
    if request.method == 'DELETE':
        student = get_object_or_404(StudentModel, pk=pk)
        student.delete()

        # 🔥 Invalidate caches
        cache.delete(f"student:{pk}")
        cache.delete("student:list")

        return Response(
            {"resp": "student deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )
