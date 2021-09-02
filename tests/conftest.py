import asdf
import pytest
import yaml


@pytest.fixture(scope="session")
def manifest():
    return yaml.safe_load(
        asdf.get_config().resource_manager["asdf://stsci.edu/schemas/gwcs/manifests/gwcs-schemas-1.0"]
    )
