from django.db import models
from django.utils.translation import ugettext as _
import uuid

from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.


class User(models.Model):
    """
    Base model for User details
    """

    # Unique ID as the Primary Key instead of the default Integer Primary Key
    uid = models.UUIDField(db_index=True, primary_key=True, default=uuid.uuid4, editable=False,
                           verbose_name='unique id')

    #User Properties
    first_name = models.CharField(_('First Name'), max_length=50, default='', blank=True)
    last_name = models.CharField(_('Last Name'), max_length=50, default='', blank=True)
    email = models.EmailField(_('Email Address'), max_length=255, unique=True)
    phone_number = PhoneNumberField(_('Phone Number'), blank=True, null=True)
    address = models.CharField(_('Address'), max_length=150, default='', blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"