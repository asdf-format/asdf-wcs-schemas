.. _asdf-wcs-schemas:

****************
ASDF WCS Schemas
****************

The ASDf WCS Schemas define a set of schemas for serializing WCS objects for the
:ref:`GWCS <gwcs:gwcs>` package.  These schemas are based upon the schemas in the
:ref:`ASDF Standard <asdf-standard:asdf-standard>` and are packaged for use by
the :ref:`asdf <asdf:asdf>` library.

.. note::
   This is only a schema package, to use these schemas to serialize WCS objects,
   one must install the :ref:`GWCS <gwcs:gwcs>` package.


Included Resources
==================

The following are listings of all the schemas provided by this package for ASDF.

.. note::
  Typically, schemas are used in ASDF via their tag, which can be found in the manifest.
  When usina a WCS in ASDF it is recommended that you use the tag instead of a direct
  reference to the schema. Moreover, when doing so make sure you are using the correct
  manifest version.

.. toctree::
  :maxdepth: 1

  wcs.rst
  frames.rst
  transforms.rst
  manifests.rst


Developer Resources
===================

.. toctree::
  :maxdepth: 1

  contributing.rst
  changes.rst
