from django.utils.translation import gettext_lazy as _

class Messages(object):
    FIRST_NAME_REQUIRED = _("First Name is required")
    LAST_NAME_REQUIRED = _("Last Name is required")
    DOB_REQUIRED=_("Date of birth is required")
    GENDER_REQUIRED=_("Gender is required")
    INVALID_CREDENTIALS_ERROR = _("Unable to log in with provided credentials.")
    INACTIVE_ACCOUNT_ERROR = _("User account is disabled.")
    INVALID_TOKEN_ERROR = _("Invalid token for given user.")
    INVALID_UID_ERROR = _("Invalid user id or user doesn't exist.")
    STALE_TOKEN_ERROR = _("Stale token for given user.")
    PASSWORD_MISMATCH_ERROR = _("The two password fields didn't match.")
    USERNAME_MISMATCH_ERROR = _("The two {0} fields didn't match.")
    INVALID_PASSWORD_ERROR = _("Invalid password.")
    EMAIL_NOT_FOUND = _("User with given email does not exist.")
    CANNOT_CREATE_USER_ERROR = _("Unable to create account.")
    OTP_NOT_FOUND=_("OTP Not found")
    INVALID_OTP=_("Invalid OTP")
    USER_NOT_FOUND_ERROR=_("User not found")
    SUSPENDED_ACCOUNT=_("Your account has been suspended please contact administration")