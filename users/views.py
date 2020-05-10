import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework import status
# Create your views here.
from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

import users.constants as user_constants
import users.validators as user_validators
from oauth import error_handling as err
from .serializers import UserCreateSerializer, UserProfileSerializer

logger = logging.getLogger(__name__)


class UserCreateView(CreateAPIView):
    """
    Class view for creating a new user
    """
    serializer_class = UserCreateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Function to create user by post request
        :param request:
        {
            "first_name": "<fname>",
            "last_name": "<lname>",
            "email": "<email>",
            "phone_number": "<ph>",
            "address": "<address>"
        }
        :param args:
        :param kwargs:
        :return: Response Instance
        """
        serializer = self.get_serializer(data=request.data)
        try:
            #: All the validations are done here
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": user_constants.USER_PROFILE_SAVED}, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error("Error inside post of UserCreateView. ERROR: {}". format(str(e)))
            raise err.ValidationError(*(err.convert_error(e), 400))


class UserProfileView(RetrieveAPIView):
    """
    Class based view to get the user profile details.
    """

    permission_classes = (IsAuthenticated, )
    serializer_class = UserProfileSerializer

    def post(self, request, *args, **kwargs):
        """
        Used POST instead of GET due to increased security reason.
        Post contains the uid
        :param request:
        {
            "uid": "<uid> - Unique ID for the user
            "first_name": "<fname>",
            "last_name": "<lname>",
            "email": "<email>",
            "phone_number": "<ph>",
            "address": "<address>"
        }
        :param args:
        :param kwargs:
        :return: Response Instance with a dict as follows
        {
        "message": <message"
        }
        """
        user_uid = request.data.get("uid", None)

        user_instance = user_validators.validate_user_exists_based_on_uid(user_uid)

        serializer = self.get_serializer(user_instance)

        response = Response(serializer.data, status=status.HTTP_200_OK)

        return response


class UserProfileUpdate(UpdateAPIView):
    """
    Class based view to update the user profile.
    """
    permission_classes = (IsAuthenticated, )
    serializer_class = UserProfileSerializer

    def update(self, request, *args, **kwargs):
        """
        Function to update user profile

        :param request: {
            "uid": "<uid> - Unique ID for the user ,
            "first_name": "First Name",
            "last_name": "Last Name",
            "email": "<useremailid>",
            "phone_number": <userphonenumber>,
            "address": "<useraddress>"
        }
        :param args:
        :param kwargs:
        :return: Response Instance with a dict as follows
        {
        "message": <message"
        }
        """

        partial = kwargs.pop('partial', False)
        user_instance_uid = request.data.get('uid', None)

        user_instance = user_validators.validate_user_exists_based_on_uid(user_instance_uid)
        request_user_instance = request.user

        serializer = self.get_serializer(user_instance, data=request.data, partial=partial)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            response = Response({
                "message": user_constants.USER_PROFILE_UPDATED
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error("Error inside update of UserProfileUpdate. ERROR: {}".format(str(e)))
            raise err.ValidationError(*(err.convert_error(e), 400))

        return response


class UserProfileDelete(DestroyAPIView):
    """
    Class based view to delete the user profile.
    """
    permission_classes = (IsAuthenticated, )
    serializer_class = UserProfileSerializer

    def delete(self, request, *args, **kwargs):
        """
        {
            "uid": "<uid> - Unique ID for the user ,

        }
        :param request:
        :param args:
        :param kwargs:
        :return: Response Instance with a message
        {
        "message" : ""
        }
        """

        user_instance_uid = request.data.get('uid', None)

        user_instance = user_validators.validate_user_exists_based_on_uid(user_instance_uid)

        try:
            user_instance.delete()
            response = Response({
                "message": user_constants.USER_PROFILE_DELETED
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error("Error inside delete of UserProfileDelete. ERROR: {}".format(str(e)))
            raise err.ValidationError(*(err.convert_error(e), 400))

        return response


