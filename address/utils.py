import requests
from django.conf import settings

components = [
    ("country", "Country"),
    ("country_code", "Country"),
    ("locality", "City"),
    ("sublocality", "Nbrhd"),
    ("postal_code", "Postal"),
    ("route", "StName"),
    ("street_number", "AddNum"),
    ("state", "Region"),
    ("district", "Subregion"),
    ("state_code", "RegionAbbr"),
    ("formatted", "LongLabel"),
    ("longitude", "X"),
    ("latitude", "Y"),
]


def geocode(raw):
    if not raw:
        return raw
    arcgis_params = {
        "address": raw,
        "outFields": ",".join([c[1] for c in components]),
        "f": "json",
        "token": settings.ARCGIS_SERVER_API_KEY,
    }

    if settings.ARCGIS_ADDRESS_CATEGORIES:
        arcgis_params["category"] = ",".join(settings.ARCGIS_ADDRESS_CATEGORIES)

    r = requests.get(
        "https://geocode-api.arcgis.com/arcgis/rest/services/World/GeocodeServer/findAddressCandidates",
        params=arcgis_params,
    ).json()
    if not "candidates" in r or len(r["candidates"]) < 1:
        return raw
    # ad = dict([(c[0], data.get(name + "_" + c[0], "")) for c in components])
    ad = dict(
        [(c[0], r["candidates"][0]["attributes"].get(c[1], "")) for c in components]
    )
    ad["raw"] = raw
    return ad
