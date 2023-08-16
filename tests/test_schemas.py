"""
Test features of the schemas not covered by the metaschema.
"""
from collections.abc import Mapping

import asdf
import pytest
import yaml

SCHEMA_URI_PREFIX = "http://stsci.edu/schemas/gwcs/"
METASCHEMA_URI = "http://stsci.edu/schemas/yaml-schema/draft-01"
SCHEMA_URIS = [u for u in asdf.get_config().resource_manager if u.startswith(SCHEMA_URI_PREFIX)]


@pytest.fixture(scope="session", params=SCHEMA_URIS)
def schema_content(request):
    return asdf.get_config().resource_manager[request.param]


@pytest.fixture(scope="session", params=SCHEMA_URIS)
def schema(request):
    return yaml.safe_load(asdf.get_config().resource_manager[request.param])


@pytest.fixture(scope="session")
def valid_tag_uris(manifest):
    uris = {t["tag_uri"] for t in manifest["tags"]}
    uris.update(
        [
            "tag:stsci.edu:asdf/time/time-1.1.0",
            "tag:stsci.edu:asdf/core/ndarray-1.0.0",
        ]
    )
    return uris


def test_required_properties(schema):
    assert schema["$schema"] == METASCHEMA_URI
    assert "id" in schema
    assert "title" in schema


def test_schema_style(schema_content):
    # xor used because windows is sometimes weird.

    assert schema_content.startswith(b"%YAML 1.1\n---\n") ^ schema_content.startswith(b"%YAML 1.1\r\n---\r\n")
    assert schema_content.endswith(b"\n...\n") ^ schema_content.endswith(b"\r\n...\r\n")
    assert b"\t" not in schema_content
    assert (not any(line != line.rstrip() for line in schema_content.split(b"\n"))) ^ (
        not any(line != line.rstrip() for line in schema_content.split(b"\r\n"))
    )


def test_property_order(schema, manifest):
    is_tag_schema = schema["id"] in {t["schema_uri"] for t in manifest["tags"]}

    if is_tag_schema:

        def callback(node):
            if isinstance(node, Mapping) and "propertyOrder" in node:
                assert node.get("type") == "object"
                property_names = set(node.get("properties", {}).keys())
                property_order_names = set(node["propertyOrder"])
                if property_order_names != property_names:
                    missing_list = ", ".join(property_order_names - property_names)
                    extra_list = ", ".join(property_names - property_order_names)
                    message = (
                        "propertyOrder does not match list of properties:\n\n"
                        "missing properties: " + missing_list + "\n"
                        "extra properties: " + extra_list
                    )
                    assert False, message

        asdf.treeutil.walk(schema, callback)
    else:

        def callback(node):
            if isinstance(node, Mapping):
                assert "propertyOrder" not in node, "Only schemas associated with a tag may specify propertyOrder"

        asdf.treeutil.walk(schema, callback)


def test_required(schema):
    def callback(node):
        if isinstance(node, Mapping) and "required" in node:
            assert node.get("type") in ["object", "string", None]
            property_names = set(node.get("properties", {}).keys())
            required_names = set(node["required"])
            if not required_names.issubset(property_names):
                missing_list = ", ".join(required_names - property_names)
                message = "required references names that do not exist: " + missing_list
                assert False, message

    asdf.treeutil.walk(schema, callback)
