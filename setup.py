from setuptools import setup, find_packages

setup(
    name="django-arcgis-address",
    url="https://github.com/melanger/django-arcgis-address.git",
    author="melanger",
    author_email="pavelbrousek@melanger.cz",
    description="Django models for storing and retrieving postal addresses.",
    packages=find_packages(),
    install_requires=["setuptools"],
)
