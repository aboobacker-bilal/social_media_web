from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from post.models import Post
from .serializers import PostSerializers


@api_view(['GET', 'POST'])
def get_post(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializers(posts, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PostSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def get_post_list(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'GET':
        serializer = PostSerializers(post, many=False)
        return Response(serializer.data)

    elif request.method == 'PUT':
        post.caption = request.data['caption']
        post.save()
        serializer = PostSerializers(post, many=False)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        post.delete()
        return Response('Post was deleted')
