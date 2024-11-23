from django.conf import settings

KEYTAB_SPN: str = getattr(settings, 'AUTH_KERBEROS_SPN', '')
UPN_SPLIT: bool = getattr(settings, 'AUTH_KERBEROS_UPN_SPLIT', True)
USERNAME_LOOKUP: str = getattr(settings, 'AUTH_KERBEROS_USERNAME_LOOKUP', '')
CREATE_UNKNOWN_USERS: bool = getattr(settings, 'AUTH_KERBEROS_CREATE_UNKNOWN_USERS', True)
