import json
from importlib import import_module

from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIRequestFactory
from social_django.models import UserSocialAuth
from .models import User
from .views import UserCreateView, UserProfileUpdate, UserProfileView, UserProfileDelete


# Create your tests here.
class BaseTestCase(TestCase):
    fixtures = ['test', 'initial_user']

    def setUp(self):
        """
        Function setting the default settings for all test cases.
        :return:
        """
        #: For request methods
        self.factory = APIRequestFactory()
        self.domain_url = 'localhost'
        #: For counting the no. of tests run
        self.TestCases = 1

    #: Decorator function which counts the number of tests run. Since to maintain the data created on each test function
    #: instead of starting with test_fnname function name is modified to check_fnname and a test_unit() method is
    # maintained for each class which will call the test function in order.The data created will be destroyed only after
    # executing test_unit().
    #: Django returning "no of tests run " will be based on this test function. So inorder to count the actual number of
    #: test functions ran , created a decorator. So if any test function fails we can easily detect which one has failed
    class Decorator:
        @classmethod
        def increment_test_cases(cls, func):
            def inner(self, *args, **kwargs):
                print('\r>> TestCase -{} : '.format(self.TestCases), end='')
                self.TestCases += 1
                return func(self, *args, **kwargs)

            return inner

    def check_token_api(self, token=None):
        """
        Test function to get the git hub access token . It will load the token from the initial_user fixture
        :param token:
        :return:
        """
        #: Get the User object from fixture
        user = UserSocialAuth.objects.first()
        return user.tokens

    def test_unit(self):
        self.setUp()
        self.check_token_api()


class UserAPITest(BaseTestCase):
    """
    Testing of APIs related to the user.
    """

    #: Sample user data object
    test_contact_data = {
        "uid": "eeea602a-27b2-4c4f-8e08-a615274dc51d",
        "first_name": "Ashida",
        "last_name": "Khader",
        "email": "ashidakhader@gmail.com",
        "phone_number": "+918281984991",
        "address": "ilford"

    }
    #: set the session
    engine = import_module(settings.SESSION_ENGINE)
    session_key = None

    @BaseTestCase.Decorator.increment_test_cases
    def check_user_create_api(self):
        """
        Test function to check the user creation api.
        :return: Test Result
        """
        """
        Check the creation of user object

        :return: Test Result
        """
        token = self.check_token_api()
        request = self.factory.post(reverse('user_create'),  data=self.test_contact_data,
                                    HTTP_AUTHORIZATION='Bearer github ' + token, format='json')
        request.session = self.engine.SessionStore(self.session_key)
        response = UserCreateView.as_view()(request)
        response.render()
        self.assertEqual(response.status_code, 201, 'Could not create a new user with valid details.')

    @BaseTestCase.Decorator.increment_test_cases
    def check_profile_retrieve_api(self, user_uid):
        """
        Test user retrieve api
        :param user_uid:
        :return:
        """
        token = self.check_token_api()
        request = self.factory.post(reverse('user_detail'), data={"user_uid": user_uid},
                                    HTTP_AUTHORIZATION='Bearer github ' + token, format='json')
        request.session = self.engine.SessionStore(self.session_key)
        response = UserProfileView.as_view()(request)
        response.render()
        self.assertEqual(response.status_code, 200, 'Could not get the user details.')

    @BaseTestCase.Decorator.increment_test_cases
    def check_profile_update_api(self, user_uid):
        """
        Test user updation api
        :param user_uid:
        :return:
        """
        token = self.check_token_api()
        data = self.test_contact_data
        data["uid"] = user_uid
        request = self.factory.put(reverse('user_update'), data=data,
                                    HTTP_AUTHORIZATION='Bearer github ' + token, format='json')
        request.session = self.engine.SessionStore(self.session_key)
        response = UserProfileUpdate.as_view()(request)
        response.render()
        self.assertEqual(response.status_code, 200, 'Could not update user with valid details.')

    @BaseTestCase.Decorator.increment_test_cases
    def check_user_profile_delete_api(self, user_uid):
        """
        Test user deletion api
        :param user_uid:
        :return:
        """
        token = self.check_token_api()
        request = self.factory.delete(reverse('user_update'), data={'uid' : user_uid},
                                    HTTP_AUTHORIZATION='Bearer github ' + token, format='json')
        request.session = self.engine.SessionStore(self.session_key)
        response = UserProfileDelete.as_view()(request)
        response.render()
        self.assertEqual(response.status_code, 200, 'Could not delete a the user with valid details.')

    def test_unit(self):
        super().test_unit()
        self.check_user_create_api()
        user_instance = User.objects.all().first()
        self.check_profile_update_api(user_instance.uid)
        self.check_profile_retrieve_api(user_instance.uid)
        self.check_user_profile_delete_api(user_instance.uid)