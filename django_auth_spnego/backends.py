import base64
import binascii
from typing import TYPE_CHECKING, Optional

import gssapi
import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from . import settings as conf

if TYPE_CHECKING:
    from django.contrib.auth.base_user import AbstractBaseUser

logger = logging.getLogger(__name__)


class SpnegoBackendMixin:

    def get_user_from_username(self, *args, **kwargs):
        raise NotImplemented

    def authenticate(self, request, spnego=None, **kwargs) -> Optional['AbstractBaseUser']:
        if spnego is None:
            return super().authenticate(request, **kwargs)
        try:
            token = base64.b64decode(spnego)
            spn_name = gssapi.Name(
                conf.KEYTAB_SPN,
                gssapi.NameType.hostbased_service
            ) if conf.KEYTAB_SPN else None
            credentials = gssapi.creds.Credentials(usage='accept', name=spn_name)
            context = gssapi.SecurityContext(creds=credentials)
            response = context.step(token)
            if not context.complete:
                return None
            username = str(context.initiator_name)
            user = self.get_user_from_username(username)
            if not user: return
            user.gssresponse = base64.b64encode(response).decode('utf-8') \
                if response else None
            return user
        except gssapi.raw.misc.GSSError as e:
            logger.warning('GSSAPI Error: {e}', e, exc_info=settings.DEBUG)
            return None
        except (binascii.Error, TypeError) as e:
            logger.warning('Non-GSSAPI Error: %s', e, exc_info=settings.DEBUG)
            return None


class SpnegoModelBackend(SpnegoBackendMixin, ModelBackend):

    @classmethod
    def get_user_from_username(cls, username) -> Optional['AbstractBaseUser']:
        User = get_user_model()
        try:
            if conf.UPN_SPLIT:
                username = username.rsplit("@")[0]
            if conf.USERNAME_LOOKUP:
                lookup_field = conf.USERNAME_LOOKUP
            else:
                lookup_field = User.USERNAME_FIELD
            if conf.CREATE_UNKNOWN_USERS:
                method = User.objects.get_or_create
            else:
                method = User.objects.get
            user, _ = method(**{lookup_field + '__iexact': username.split("@")[0]})
            return user
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return None
