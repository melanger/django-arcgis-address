# [1.1.0](https://github.com/melanger/django-arcgis-address/compare/v1.0.1...v1.1.0) (2022-01-05)


### Features

* custom category filtering ([5993cfb](https://github.com/melanger/django-arcgis-address/commit/5993cfb070c97ba29df519efb68a64d2bf7cce93)), closes [#11](https://github.com/melanger/django-arcgis-address/issues/11)

## [1.0.1](https://github.com/melanger/django-arcgis-address/compare/v1.0.0...v1.0.1) (2021-09-24)


### Bug Fixes

* release to pypi ([1a68e15](https://github.com/melanger/django-arcgis-address/commit/1a68e15f848e37a14c95fd27ce72762559cb5182))

# 1.0.0 (2021-09-23)


### Bug Fixes

* fix typo ([be9fa83](https://github.com/melanger/django-arcgis-address/commit/be9fa83c84176f2a902a23f28fb19348b3ce649a))
* jQuery first and global ([5c24b39](https://github.com/melanger/django-arcgis-address/commit/5c24b3919364a468bbaf6063a0dab0f610345e51))
* load jQuery and select2 from Django ([79b7bc0](https://github.com/melanger/django-arcgis-address/commit/79b7bc00dec525caf912ad78079a14833910a797))
* remove select2 library ([a9d5e19](https://github.com/melanger/django-arcgis-address/commit/a9d5e19873a99bcc8fdc3f1a2f8c7980bc40f027))
* switch latitude and longitude ([319389e](https://github.com/melanger/django-arcgis-address/commit/319389e8e7fd34a67042fde4a55d66d75e5095a6))
* use namespaced django's jQuery ([7ef5dca](https://github.com/melanger/django-arcgis-address/commit/7ef5dca9cb55bd38c1a6f7eab5ede55e60ff04f2))


### Features

* add District and Sublocality address parts ([5c2aad2](https://github.com/melanger/django-arcgis-address/commit/5c2aad259740423ba00dc9b3f1a350de369b2fec))
* arcGIS autocomplete ([986b56d](https://github.com/melanger/django-arcgis-address/commit/986b56d3e35eef920b0a49d7566ec859de62fb7d))
* first commit ([aa6f5cc](https://github.com/melanger/django-arcgis-address/commit/aa6f5ccd818f356345cd479b2e080264217e0181))


### BREAKING CHANGES

* removed select2 library and the loading of jQuery from Django
* removed Google related stuff, removed support for Django < 1.9
