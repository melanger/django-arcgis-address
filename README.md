# Django Address 

**Django models for storing and retrieving postal addresses.**

Based on [django-address](https://github.com/furious-luke/django-address) but uses ESRI ArcGIS instead of Google.

---

# Overview
Django Address is a set of models and methods for working with postal addresses.

# Requirements

* Python (3.9)
* Django (3.0) with a theme which includes jQuery (as django.jQuery) and the select2 library

# Installation

```bash
pip3 install git+https://github.com/melanger/django-arcgis-address.git
```

Then, add `address` to your `INSTALLED_APPS` list in `settings.py`:

```
INSTALLED_APPS = [
    # ... 
    'address',
    # ... 
]
```

You can either store your ESRI API key in an environment variable as `ARCGIS_SERVER_API_KEY` and `ARCGIS_CLIENT_API_KEY` or you can
 specify the key in `settings.py`. If you have an environment variable set it will override what you put in settings.py.
 
```
ARCGIS_SERVER_API_KEY = '}zIMqHDs"4CJs$l[G.+XHSJ)Wq[?mVgr'
ARCGIS_CLIENT_API_KEY = '}zIMqHDs"4CJs$l[G.+XHSJ)Wq[?mVgr'
```

# The Model

The rationale behind the model structure is centered on trying to make
it easy to enter addresses that may be poorly defined. The model field included
uses ArcGIS API to determine a proper address where possible. However if this isn't possible the
raw address is used and the user is responsible for breaking the address down
into components.

It's currently assumed any address is represent-able using four components:
country, state, locality and street address. In addition, country code, state
code, postal code, district and sublocality may be stored, if they exist.

There are six Django models used:

```
  Country
    name
    code

  State
    name
    code
    country -> Country

  District
    name
    state -> State

  Locality
    name
    postal_code
    state -> State
    district -> District

  Sublocality
    name
    locality -> Locality

  Address
    raw
    street_number
    route
    locality -> Locality
    sublocality -> Sublocality
```

# Address Field

To simplify storage and access of addresses, a subclass of `ForeignKey` named
`AddressField` has been created. It provides an easy method for setting new
addresses.

## ON_DELETE behavior of Address Field

By default, if you delete an Address that is related to another object, 
Django's [cascade behavior](https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.ForeignKey.on_delete) 
is used. This means the related object will also be deleted. You may also choose
to set `null=True` when defining an address field to have the address set
to Null instead of deleting the related object.
 
## Creation

It can be created using the same optional arguments as a ForeignKey field.
For example:

```python
  from address.models import AddressField

  class MyModel(models.Model):
    address1 = AddressField()
    address2 = AddressField(related_name='+', blank=True, null=True)
```

## Setting Values

Values can be set either by assigning an Address object:

```python
  addr = Address(...)
  addr.save()
  obj.address = addr
```

Or by supplying a dictionary of address components:

```python
  obj.address = {'street_number': '1', 'route': 'Somewhere Ave', ...}
```

The structure of the address components is as follows:

```python
  {
    'raw': '1 Somewhere Ave, Northcote, VIC 3070, AU',
    'street_number': '1',
    'route': 'Somewhere Ave',
    'locality': 'Northcote',
    'sublocality': 'Northcote pt',
    'postal_code': '3070',
    'state': 'Victoria',
    'state_code': 'VIC',
    'district': 'Dst',
    'country': 'Australia',
    'country_code': 'AU'
  }
```

All except the `raw` field can be omitted. In addition, a raw address may
be set directly:

```python
obj.address = 'Out the back of 1 Somewhere Ave, Northcote, Australia'
```

## Getting Values

When accessed, the address field simply returns an Address object. This way
all components may be accessed naturally through the object. For example:

```python
  route = obj.address.route
  state_name = obj.address.locality.state.name
```

## Forms

Included is a form field for simplifying address entry. [ArcGIS autosuggest](https://developers.arcgis.com/documentation/mapping-apis-and-services/search/autosuggest/) is performed in the browser and passed to the view. If the lookup fails the raw entered value is used.

## Partial Example

The model:

```python
from address.models import AddressField

class Person(models.Model):
  address = AddressField(on_delete=models.CASCADE)
```

The form:

```
from address.forms import AddressField

class PersonForm(forms.Form):
  address = AddressField()
```

The template:

```html
<head>
{{ form.media }} <!-- needed for JS lookup -->
</head>
<body>
  {{ form }}
</body>
```
