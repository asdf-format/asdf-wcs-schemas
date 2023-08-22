import asdf
import pytest
import yaml


@pytest.fixture(scope="session", params=["1.0.0", "1.1.0"])
def manifest(request):
    return yaml.safe_load(
        asdf.get_config().resource_manager[f"asdf://asdf-format.org/astronomy/gwcs/manifests/gwcs-{request.param}"]
    )
