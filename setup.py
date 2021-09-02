#!/usr/bin/env python
from setuptools import setup, find_packages


packages = find_packages(where="src")
packages.append("asdf_wcs_schemas.resources")

package_dir = {
    "": "src",
    "asdf_wcs_schemas.resources": "resources",
}

package_data = {
    "asdf_wcs_schemas.resources": [
        "manifests/*.yaml",
        "schemas/stsci.edu/gwcs/*.yaml"
    ],
}

setup(
    use_scm_version=True,
    packages=packages,
    package_dir=package_dir,
    package_data=package_data,
)
