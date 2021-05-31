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
            "js/select2.min.js",
            "js/i18n/cs.js",
            "address/js/address.js",
        ]

        vendor = "vendor/jquery/"
        extra = "" if settings.DEBUG else ".min"
        jquery_paths = [
            "{}jquery{}.js".format(vendor, extra),
            "jquery.init.js",
        ]
        jquery_paths = ["admin/js/{}".format(path) for path in jquery_paths]
        js = jquery_paths + js

        css = {"all": ("css/select2.min.css", "address/css/address.css")}

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
        elems = [
            super(AddressWidget, self).render(
                name, escape(ad.get("raw", "")), attrs, **kwargs
            )
        ]

        return mark_safe(unicode("\n".join(elems)))

    def value_from_datadict(self, data, files, name):
        raw = data.get(name, "")
        return geocode(raw)
