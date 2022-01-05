import sys

from django import forms
from django.conf import settings
from django.utils.html import escape
from django.utils.safestring import mark_safe

from .models import Address
from .utils import geocode

if sys.version > "3":
    long = int
    basestring = (str, bytes)
    unicode = str


class AddressWidget(forms.Select):
    choices = []

    class Media:
        """Media defined as a dynamic property instead of an inner class."""

        js = [
            "admin/js/vendor/jquery/jquery.min.js",
            "admin/js/vendor/select2/select2.full.min.js",
            "admin/js/vendor/select2/i18n/cs.js",
            "admin/js/jquery.init.js",
            "address/js/address.js",
        ]

        css = {
            "all": [
                "admin/css/vendor/select2/select2.min.css",
                "address/css/address.css",
            ]
        }

    def __init__(self, *args, **kwargs):
        attrs = kwargs.get("attrs", {})
        classes = attrs.get("class", "")
        classes += (" " if classes else "") + "address"
        attrs["class"] = classes
        kwargs["attrs"] = attrs
        super(AddressWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, **kwargs):

        # Can accept None, a dictionary of values or an Address object.
        if value in (None, ""):
            ad = {}
        elif isinstance(value, dict):
            ad = value
        elif isinstance(value, (int, long)):
            ad = Address.objects.get(pk=value)
            ad = ad.as_dict()
        else:
            ad = value.as_dict()

        # Generate the elements. We should create a visible field for the raw.
        attrs["data-select2-default-value"] = ad.get("raw", "")
        attrs["data-select2-api-key"] = settings.ARCGIS_CLIENT_API_KEY
        attrs["data-select2-filter-categories"] = (
            ",".join(settings.ARCGIS_ADDRESS_CATEGORIES)
            if hasattr(settings, "ARCGIS_ADDRESS_CATEGORIES")
            else "Address"
        )
        elems = [
            super(AddressWidget, self).render(
                name, escape(ad.get("raw", "")), attrs, **kwargs
            )
        ]

        return mark_safe(unicode("\n".join(elems)))

    def value_from_datadict(self, data, files, name):
        raw = data.get(name, "")
        return geocode(raw)
