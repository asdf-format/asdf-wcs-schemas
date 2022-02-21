import asdf
import pytest
import yaml


@pytest.fixture(scope="session")
def manifest():
    return yaml.safe_load(
        asdf.get_config().resource_manager["asdf://asdf-format.org/astronomy/gwcs/manifests/gwcs-1.0.0"]
    )
