from setuptools import setup, find_packages

setup(
    name="django-arcgis-address",
    version="1.0.0",
    url="https://github.com/melanger/django-arcgis-address.git",
    author="melanger",
    author_email="brousek@ics.muni.cz",
    description="Django models for storing and retrieving postal addresses.",
    packages=find_packages(),
    install_requires=["setuptools"],
)
