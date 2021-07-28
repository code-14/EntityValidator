from django.shortcuts import render
# from rest_framework import *
import traceback
from app1.validation.validate import *
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.


@api_view(['GET'])
def welcomePage(request):
    result = "Welcome ..this is homepage"
    response = Response(result, status=status.HTTP_200_OK)
    return response


@api_view(['GET', 'POST'])
def validate_finite_values_entity(request):
    if request.method == 'GET':
        return Response({"message": "This is validate_finite_values_entity api"})

    data = request.data
    try:
        result = wrapper_validate_finite_values_entity(data)
    except:
        error = "The request could not be understood by the server due to malformed syntax. The client SHOULD NOT repeat the request without modifications"
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    response = Response(result, status=status.HTTP_200_OK)
    return response


@api_view(['GET', 'POST'])
def validate_numeric_entity(request):
    if request.method == 'GET':
        return Response({"message": "This is validate_numeric_entity api"})
    data = request.data
    try:
        result = wrapper_validate_numeric_entity(data)
    except:
        error = "The request could not be understood by the server due to malformed syntax. The client SHOULD NOT repeat the request without modifications"
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    response = Response(result, status=status.HTTP_200_OK)
    return response


@api_view(['GET', 'POST'])
def entity_parse_and_validate(request):
    if request.method == 'GET':
        return Response({"message": "Validating entity"})

    data = request.data
    try:
        t = entity_parse_and_validate(data)
    except:
        error = "Bad request!!"
        traceback.print_exc()
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    response = Response(t, status=status.HTTP_200_OK)
    return response
