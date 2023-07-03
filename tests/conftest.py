import asdf
import pytest
import yaml

MANIFESTS = [
    "asdf://asdf-format.org/astronomy/gwcs/manifests/gwcs-1.0.0",
    "asdf://asdf-format.org/astronomy/gwcs/manifests/gwcs-1.1.0",
]


@pytest.fixture(scope="session", params=MANIFESTS)
def manifest(request):
    return yaml.safe_load(asdf.get_config().resource_manager[request.param])
