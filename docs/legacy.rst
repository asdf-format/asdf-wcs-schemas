.. _legacy:

WCS Legacy
==========

As part of the move from ``asdf-standard`` to this schema package, the schemas were
refactored to work better with ``gwcs``. As a consequence, this left a set of legacy
WCS schemas.

Manifest
--------

.. asdf-autoschemas::
   :schema_root: ../resources
   :standard_prefix: manifests/wcs

   wcs-1.0.0
   wcs-1.1.0
   wcs-1.2.0
   wcs-1.3.0

Schemas
-------

.. asdf-autoschemas::
   :standard_prefix: wcs

   celestial_frame-1.0.0
   celestial_frame-1.1.0
   composite_frame-1.0.0
   composite_frame-1.1.0
   frame-1.0.0
   frame-1.1.0
   icrs_coord-1.1.0
   spectral_frame-1.0.0
   spectral_frame-1.1.0
   step-1.0.0
   step-1.1.0
   step-1.2.0
   wcs-1.0.0
   wcs-1.1.0
   wcs-1.2.0
