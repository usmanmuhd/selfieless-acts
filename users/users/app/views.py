from . import models
import base64
from django.conf.urls.static import static
import os
from dateutil.parser import parse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.status import *
import json

count_requests = [0]


@api_view(['GET', 'POST'])
def ListAll_Add_User(request):
	global count_requests
	count_requests[0] += 1
	data = request.data

	#to list all users
	if request.method == "GET":
		print("\nListAllUser :", data, "\n")

		li = []
		for i in models.user.objects.all():
			li.append(i.username)

		if len(li) == 0:
			return Response({}, status=HTTP_204_NO_CONTENT)

		return Response(li, status=HTTP_200_OK)

	#to add a new user
	if request.method == "POST":
		print("\nAddUser :", data, "\n")

		if type(data['password']) != str or len(data['password']) != 40 or len(data['username']) == 0:
			return Response({}, status=HTTP_400_BAD_REQUEST)

		try:
			#to check if it is in hexdigest
			int(data['password'], 16)
			c = models.user.objects.create(username=data['username'], password=data['password'])
			return Response({}, status=HTTP_201_CREATED)

		except Exception as e:
			print("Exception in add user :", e)
			return Response({}, status=HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def RemoveUser(request, username):
	global count_requests
	count_requests[0] += 1
	data = request.data
	print("\nRemoveUser :", data, "\n")

	try:
		models.user.objects.get(pk = username).delete()
		return Response({}, status=HTTP_200_OK)

	except Exception as e:
		print("Exception in remove user :", e)
		return Response({}, status=HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
def count(request):
	global count_requests
	print("\ncount request received", request.data, '\n')

	if request.method == 'GET':
		return Response(count_requests, status=HTTP_200_OK)

	if request.method == 'DELETE':
		count_requests = [0]
		return Response({}, status=HTTP_200_OK)
