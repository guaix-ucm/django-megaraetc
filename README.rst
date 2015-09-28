==========
MEGARA ETC
==========

Run MEGARA ETC  as a Django APP

Quick start
-----------

1. Add "etc" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'etc',
    )

2. Include the polls URLconf in your project urls.py like this::

    url(r'^etc/', include('etc.urls')),

3. Run `python manage.py migrate` to create the etc models.


