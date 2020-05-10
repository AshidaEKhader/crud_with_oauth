import logging

from rest_framework import serializers

from users import constants as user_constants, validators as user_validators
from users.models import User

logger = logging.getLogger(__name__)


class UserCreateSerializer(serializers.Serializer):
    """
    Custom serializer to create a new user
    """

    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True, max_length=50)
    last_name = serializers.CharField(required=True, max_length=50)
    phone_number = serializers.CharField(max_length=20)
    address = serializers.CharField(max_length=150)

    def validate(self, data):
        """
        Custom validation to check
        :param data: POST data
        :return: Validated data
        """
        first_name = data.get('first_name', None)
        last_name = data.get('last_name', None)

        if not first_name:
            raise serializers.ValidationError({"message": user_constants.FIRST_NAME_NOT_FOUND_IN_REQUEST})

        if not last_name:
            raise serializers.ValidationError({"message": user_constants.LAST_NAME_NOT_FOUND_IN_REQUEST})

        # Check if the user already exists with the same email
        user = User.objects.filter(email=data["email"]).first()
        if user:
            raise serializers.ValidationError(user_constants.USER_ALREADY_REGISTERED_WITH_EMAIL.format(data["email"]))

        phone_number = data["phone_number"]
        user_validators.validate_user_phone_number(phone_number)

        return data

    def save(self):
        """
        Method used to save the user instance.
        :return: None
        """

        email = self.validated_data['email']
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        phone_number = self.validated_data['phone_number']
        address = self.validated_data.get('address', '')

        # Create the user with the first_name,email,last_name, etc...
        user = User(email=email, first_name=first_name, last_name=last_name, \
                    phone_number=phone_number, address=address)

        user.save()


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Model serializer for Serializing User Instances
    """
    def validate(self, data):
        """
        Function to validate the passed values
        :param data:
        :return:
        """
        user_instance_uid = self.context.get('request',{}).data.get('uid', None)
        phone_number = data["phone_number"]
        #: Validate the phone number
        user_validators.validate_user_phone_number(phone_number)
        #: Validate the user uid passed
        user_validators.validate_user_exists_based_on_uid(user_instance_uid)

        return data

    def update(self, instance, validated_data):
        """
        Overriding the default update function to update the user's first_name, last_name, ph_number, etc..
        :param instance: User Instance
        :param validated_data:
        :return: updated User Instance
        """

        request_data = self.context.get('request',{})

        instance.first_name = validated_data["first_name"]
        instance.last_name = validated_data["last_name"]
        instance.phone_number = validated_data["phone_number"]
        instance.address = validated_data["address"]

        # Update the user instance
        instance.save()

        # Return the updated user instance
        return instance

    class Meta:
        model = User
        fields = ( 'uid', 'first_name', 'last_name', 'email', 'phone_number', 'address')
        read_only_fields = ('email', ) #: As email can not be updated after registering.



