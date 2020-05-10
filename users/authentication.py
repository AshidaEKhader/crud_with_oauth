# Create your views here.
import uuid

import requests
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from django.shortcuts import redirect

import users.constants as user_constants
from oauth import error_handling as err


@api_view(('GET', ))
@renderer_classes((JSONRenderer, ))
def callback_view(request):
    """
    Git hub call back url associated method. It will call the api to get access token
    :param request:
    :return: Response of the structure
    {"message":"access_token=dd255294179ad256fd292af42dab765e019ffb93&scope=user&token_type=bearer"}
    """

    #: The request will contain code and state as its query param
    access_code = request.GET['code']
    state = request.GET['state']
    payload = {}

    #: setting the credentials to call the GITHUB API ENDPOINT
    payload['client_id'] = settings.CLIENT_ID
    payload['client_secret'] = settings.CLIENT_SECRET
    payload['code'] = access_code
    payload['state'] = state
    github_response = requests.post(settings.GITHUB_API_ENDPOINT,
                                    data=payload)

    if github_response.status_code == 200:
        response =  Response({
            "message": github_response.text
        }, status=status.HTTP_200_OK)
        return response


@api_view(('GET',))
@renderer_classes((JSONRenderer,))
def login_view(request):
    """
    Function based view for login function. It will redirect to github login page.
    :param request:
    :return:
    """
    try:
        user_name = request.GET['user']
    except Exception as e:
        raise err.ValidationError(user_constants.USERNAME_REQUIRED)

    #: A random string representing state is required .
    state = uuid.uuid4()
    redirect_url = settings.GITHUB_API_LOGIN_ENDPOINT + 'client_id=' + settings.CLIENT_ID + '&scope=user&login=' + \
                   user_name +"&state="+str(state)
    return redirect(redirect_url)

