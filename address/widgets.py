import sys
import requests

from django import forms
from django.conf import settings
from django.utils.html import escape
from django.utils.safestring import mark_safe

from .models import Address

if sys.version > "3":
    long = int
    basestring = (str, bytes)
    unicode = str


class AddressWidget(forms.Select):
    choices = []
    components = [
        ("country", "Country"),
        ("country_code", "Country"),
        ("locality", "City"),
        ("sublocality", "Nbrhd"),
        ("postal_code", "Postal"),
        ("postal_town", "no_postal_town"),
        ("route", "StName"),
        ("street_number", "AddNum"),
        ("state", "Region"),  # kraj
        # TODO: ("region", "Subregion"), # okres
        ("state_code", "RegionAbbr"),
        ("formatted", "LongLabel"),
        ("latitude", "X"),
        ("longitude", "Y"),
    ]

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
        if not raw:
            return raw

        arcgis_params = {
            "address": raw,
            "outFields": ",".join([c[1] for c in self.components]),
            "f": "json",
            "token": settings.ARCGIS_SERVER_API_KEY,
        }
        r = requests.get(
            "https://geocode-api.arcgis.com/arcgis/rest/services/World/GeocodeServer/findAddressCandidates",
            params=arcgis_params,
        ).json()
        if not "candidates" in r or len(r["candidates"]) < 1:
            return raw
        # ad = dict([(c[0], data.get(name + "_" + c[0], "")) for c in self.components])
        ad = dict(
            [
                (c[0], r["candidates"][0]["attributes"].get(c[1], ""))
                for c in self.components
            ]
        )
        ad["raw"] = raw

        return ad
