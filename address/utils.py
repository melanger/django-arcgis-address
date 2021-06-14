import requests
from django.conf import settings

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
