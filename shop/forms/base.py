from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.forms import widgets
from django.utils.encoding import force_str
from django.utils.functional import cached_property
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _


class DialogFormMixin:
    required_css_class = 'djng-field-required'

    def __init__(self, *args, **kwargs):
        kwargs.pop('cart', None)  # cart object must be removed, otherwise underlying methods complain
        auto_name = self.form_name  ## .replace('_form', '')
        kwargs.setdefault('auto_id', '{}-%s'.format(auto_name))
        super().__init__(*args, **kwargs)

    def form_name(cls):
        return cls.__name__

    def clean(self):
        cleaned_data = dict(super().clean())
        cleaned_data.pop('plugin_id', None)
        if cleaned_data.pop('plugin_order', None) is None:
            msg = "Field 'plugin_order' is a hidden but required field in each form inheriting from DialogFormMixin"
            raise ValidationError(msg)
        return cleaned_data

    def get_response_data(self):
        """
        Hook to respond with an updated version of the form data. This response then shall
        override the forms content.
        """


class UniqueEmailValidationMixin:
    """
    A mixin added to forms which have to validate for the uniqueness of email addresses.
    """
    def clean_email(self):
        if not self.cleaned_data['email']:
            raise ValidationError(_("Please provide a valid e-mail address"))
        # check for uniqueness of email address
        if get_user_model().objects.filter(is_active=True, email=self.cleaned_data['email']).exists():
            msg = _("A customer with the e-mail address '{email}' already exists.\n"
                    "If you have used this address previously, try to reset the password.")
            raise ValidationError(msg.format(**self.cleaned_data))
        return self.cleaned_data['email']