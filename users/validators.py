import logging
import re

from oauth import error_handling as err

from users import constants as user_constants
from users.models import User

# Initialize logger
logger = logging.getLogger(__name__)


def validate_user_exists_based_on_uid(user_uid):
    """
    Function that returns User instance if a user exists with the passed uid, else raises error.

    :param user_uid: User uid

    :return: User Instance if the user does not exists else raise error
    """

    try:
        user_instance = User.objects.get(uid=user_uid)

    except Exception as e:
        logger.error('Error inside validate_user_exists_based_on_uid function. ERROR: {}'.format(str(e)))
        raise err.NotFound(user_constants.USER_NOT_FOUND, 404)

    return user_instance


def validate_user_exists_based_on_email(email):
    """
    FFunction that returns User instance if a user exists with the  passed email, else raises error.

    :param email: User email

    :return: User Instance if the user does not exists else raise error
    """

    try:
        user_instance = User.objects.get(email=email)

    except Exception as e:
        logger.error('Error inside validate_user_exists_based_on_email function. ERROR: {}'.format(str(e)))
        raise err.ValidationError(user_constants.USER_NOT_FOUND, 400)

    return user_instance


def validate_user_phone_number(phone_number):
    """
    Function to validate user phone number (check if there is any string).

    :param phone_number: phone number

    :return: Boolean true or raises error.
    """
    pattern = re.compile(r'[A-Za-z]')
    if not pattern.findall(phone_number):
        return True

    raise err.ValidationError(user_constants.ALPHABETS_NOT_ALLOWED_IN_PHONE_NUMBER, 400)

