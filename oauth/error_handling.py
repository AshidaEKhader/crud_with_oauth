from rest_framework import exceptions


class APIException(exceptions.APIException):
    """
    Exception class that caught by renderer and produce pretty output.

    It also has ``error_code`` attribute that may be set by other app otherwise it'll be ``-1``
    """

    def __init__(self, detail=None, error_code=-1, kw=None):
        if isinstance(kw, dict):
            detail = detail % kw
        super(APIException, self).__init__(detail=detail)
        self.error_code = error_code
        self.message = detail


class ValidationError(APIException):
    """
    Exception class for all kind of validation errors
    """
    status_code = 400

class PermissionDenied(APIException):
    """
    Exception class for permission denied errors
    """
    status_code = 403

class NotFound(APIException):
    """
    Exception class for missing resource
    """
    status_code = 404

class UserLocked(APIException):
    """
    Exception class for Locked state
    """
    status_code = 423


def formulate_error(error_message):
    """
    Convert the error message of string form to the form
    {
        "key": [ "message"]
    }
    :param error_message: Error message in string
    :return: a dict with a key and the value as a list which contains the error message
    """
    error_message = convert_error(error_message)
    return error_message


def convert_error(error_message):
    """
    Function to convert the errors from serializer to feasible format.

    :param error_message: The error message from serializer.
    :return: The converted error message
    """
    try:
        # If the error have detail. Errors raised by serializer validation and validation errors of other type have
        # error detail.
        if error_message.detail:
            if error_message.default_code == 'error':
                # The errors raised by utility functions or validator functions using validation error
                # is raised using this.
                return error_message.detail
            # Errors with code invalid are handled using the following code.
            if error_message.default_code == 'invalid':
                custom_error_message = ''
                for key in error_message.detail:
                    if error_message.detail[key][0].code == 'required':
                        key = str(key).replace("_", " ").capitalize()
                        custom_error_message += key + ' is a required field.'
                        return custom_error_message
                    elif error_message.detail[key][0].code == 'null':
                        key = str(key).replace("_", " ").capitalize()
                        custom_error_message += key + ' should not be null.'
                        return custom_error_message
                    elif error_message.detail[key][0].code == 'invalid_phone_number' or error_message.detail[key][0].code == 'invalid' or error_message.detail[key][0].code == 400 or error_message.detail[key][0].code == 'unique':
                        return error_message.detail
                    elif error_message.detail[key][0].code == 'blank':
                        key = str(key).replace("_", " ").capitalize()
                        custom_error_message += key + ' should not be blank.'
                        return custom_error_message
                    elif error_message.detail[key][0].code == 'max_length':
                        key = str(key).replace("_", " ").capitalize()
                        custom_error_message += key + ' field data is too long.'
                        return custom_error_message
                    else:
                        # This message will be displayed when validation errors not handled above occurs.
                        return "The data entered is invalid. Please enter valid data."
            return "Something isn't right with the information you entered. Please check, and try again."

    except:
        # For error messages which does not have ErrorDetail. Eg: Attribute error
        return "Something went wrong and we could not complete the requested action. Please try again."